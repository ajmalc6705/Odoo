# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: Al Kidhma Group
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class HrFlightTicket(models.Model):
    _name = 'hr.flight.ticket'

    @api.depends('employee_ticket_details_ids.ticket_price_total')
    def _amount_all(self):
        total_amount = 0.0
        for record in self:
            for line in record.employee_ticket_details_ids:
                total_amount += line.ticket_rate
            record.update({
                'total_ticket_fare': total_amount,
            })
        return total_amount

    name = fields.Char()
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    ticket_type = fields.Selection([('one', 'One Way'), ('round', 'Round Trip')], string='Ticket Type', default='round')
    air_lines_partner_id = fields.Many2one('res.partner', string="Air Line Agency", required=True)
    depart_from = fields.Char(string='Departure', required=True)
    destination = fields.Char(string='Destination', required=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_return = fields.Date(string='Return Date')
    ticket_class = fields.Selection([('economy', 'Economy'),
                                     ('premium_economy', 'Premium Economy'),
                                     ('business', 'Business'),
                                     ('first_class', 'First Class')], string='Class')
    currency_id = fields.Many2one('res.currency', store=True, string='Currency', readonly=True)
    total_ticket_fare = fields.Monetary(string='Total Ticket Fare', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    flight_details = fields.Text(string='Flight Details')
    return_flight_details = fields.Text(string='Return Flight Details')
    state = fields.Selection([('booked', 'Booked'), ('confirmed', 'Confirmed'), ('started', 'Started'),
                              ('completed', 'Completed'), ('canceled', 'Canceled')], string='Status', default='booked')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id)

    flight_ticket_expense_account = fields.Many2one('account.account', string='Travel Expense Account')
    flight_ticket_expense_journal = fields.Many2one('account.journal', string='Travel Expense Journal',
                                                    domain=[('type', '=', 'purchase')])
    employee_ticket_details_ids = fields.One2many('hr.flight.ticket.line', 'ticket_id', string="Family Ticket Details")

    @api.multi
    def name_get(self):
        res = []
        for ticket in self:
            res.append((ticket.id, _("Flight ticket for %s on %s to %s") % (
                ticket.employee_id.name, ticket.date_start, ticket.destination)))
        return res

    @api.constrains('date_start', 'date_return')
    def check_valid_date(self):
        if self.filtered(lambda c: c.date_return and c.date_start > c.date_return):
            raise ValidationError(_('Flight travelling start date must be less than flight return date.'))

    def confirm_ticket(self):
        if not self.employee_ticket_details_ids:
            raise UserError(_('Please Add Family Member'))

        line = [m.family_member.id for m in self.employee_ticket_details_ids]
        if len(line) != len(set(line)):
            raise UserError(_('Can not Take multiple ticket for the same Family Member'))

        if len(self.employee_ticket_details_ids) > 3:
            minor_count = 0
            visa_det = self.env['hr.employee.visa.details.line'].search([('hr_employee_id', '=', self.employee_id.id)])
            for rec in self.employee_ticket_details_ids:
                if rec.family_member.id in [vsa_member.family_member.id for vsa_member in visa_det]:
                    member_visa_detail = self.env['hr.employee.visa.details.line'].search([('hr_employee_id', '=', self.employee_id.id), ('family_member', '=', rec.family_member.id)])
                    created_date = datetime.strptime(rec.create_date, '%Y-%m-%d %H:%M:%S').date()
                    dob = datetime.strptime(member_visa_detail.date_of_birth, '%Y-%m-%d').date()
                    year_difference = relativedelta(created_date, dob).years
                    if year_difference < 18:
                        minor_count += 1
            if minor_count > 3:
                raise UserError(_('Can not Take ticket for more than 3 Children'))

        if self.total_ticket_fare <= 0:
            raise UserError(_('Please add ticket fare.'))

        if self.total_ticket_fare > self.employee_id.grade_id.ticket_limit:
            raise UserError(_('Ticket fare is Greater than Your Ticket Limit'))

        inv_obj = self.env['account.invoice'].sudo()

        if not self.flight_ticket_expense_account:
            raise UserError(_('Please select expense account for the flight tickets.'))

        if not self.flight_ticket_expense_journal:
            raise UserError(_('Please select Journal for the flight tickets.'))

        if not self.air_lines_partner_id.property_payment_term_id:
            date_due = fields.Date.context_today(self)
        else:
            pterm = self.air_lines_partner_id.property_payment_term_id
            pterm_list = \
                pterm.with_context(currency_id=self.env.user.company_id.id).compute(value=1, date_ref=fields.Date.context_today(self))[0]
            date_due = max(line[0] for line in pterm_list)
        inv_data = {
            'name': '',
            'origin': 'Flight Ticket',
            'type': 'in_invoice',
            'journal_id': self.flight_ticket_expense_journal.id,
            'payment_term_id': self.air_lines_partner_id.property_payment_term_id.id,
            'date_due': date_due,
            'reference': False,
            'partner_id': self.air_lines_partner_id.id,
            'account_id': self.air_lines_partner_id.property_account_payable_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Flight Ticket',
                'price_unit': self.total_ticket_fare,
                'quantity': 1.0,
                'account_id': self.flight_ticket_expense_account.id,
            })],
        }
        inv_id = inv_obj.create(inv_data)
        inv_id.action_invoice_open()
        self.write({'state': 'confirmed', 'invoice_id': inv_id.id})

    def cancel_ticket(self):
        if self.state == 'booked':
            self.write({'state': 'canceled'})
        elif self.state == 'confirmed':
            if self.invoice_id and self.invoice_id.state == 'paid':
                self.write({'state': 'canceled'})
            if self.invoice_id and self.invoice_id.state == 'open':
                self.invoice_id.action_invoice_cancel()
                self.write({'state': 'canceled'})

    @api.multi
    def action_view_invoice(self):
        return {
            'name': _('Flight Ticket Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.invoice_supplier_form').id,
            'res_model': 'account.invoice',
            'context': "{'type':'in_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_id.id,
        }

    # @api.model
    # def create(self, vals):
    #     if vals.get('employee_ticket_details_ids'):
    #         line = [m[2]['family_member'] for m in vals.get('employee_ticket_details_ids')]
    #         if len(line) != len(set(line)):
    #             raise UserError(_('Can not Take multiple ticket for the same Family Member'))
    #
    #         if len(vals.get('employee_ticket_details_ids')) > 3:
    #             miner_count = 0
    #             visa_det = self.env['hr.employee.visa.details.line'].search([('hr_employee_id', '=', vals['employee_id'])])
    #
    #             for vsa_d in visa_det:
    #                 if vsa_d.family_member.id in line:
    #                     dob = datetime.datetime.strptime(vsa_d.date_of_birth, '%Y-%m-%d').date()
    #                     year_diff = relativedelta(datetime.date.today(), dob).years
    #                     if year_diff < 18:
    #                         miner_count += 1
    #             if miner_count > 3:
    #                 raise UserError(_('Can not Take ticket for more than 3 Children'))
    #     return super(HrFlightTicket, self).create(vals)
    #
    # def write(self, vals):
    #     result = super(HrFlightTicket, self).write(vals)
    #     if vals.get('employee_ticket_details_ids'):
    #         line = [m.family_member.id for m in self.employee_ticket_details_ids]
    #         if len(line) != len(set(line)):
    #             raise UserError(_('Can not Take multiple ticket for the same Family Member'))
    #
    #         if len(self.employee_ticket_details_ids) > 3:
    #             miner_count = 0
    #             visa_det = self.env['hr.employee.visa.details.line'].search([('hr_employee_id', '=', self.employee_id.id)])
    #             for vsa_d in visa_det:
    #                 if vsa_d.family_member.id in line:
    #                     dob = datetime.datetime.strptime(vsa_d.date_of_birth, '%Y-%m-%d').date()
    #                     print("dob = ", dob)
    #                     print("tday = ", datetime.date.today())
    #                     year_diff = relativedelta(datetime.date.today(), dob).years
    #                     print("year_diff = ", year_diff)
    #                     print("_"*30, "\n")
    #                     if year_diff < 18:
    #                         miner_count += 1
    #             if miner_count > 3:
    #                 raise UserError(_('Can not Take ticket for more than 3 Children'))
    #     return result


class HrFlightTicketMembersLine(models.Model):
    _name = 'hr.flight.ticket.line'

    @api.depends('ticket_rate')
    def _compute_amount(self):
        price = 0
        for line in self:
            price += line.ticket_rate
            line.update({
                'ticket_price_total': price,
            })

    ticket_id = fields.Many2one('hr.flight.ticket', string="Ticket Details")
    currency_id = fields.Many2one('res.currency', store=True, string='Currency', readonly=True)
    employee_id = fields.Many2one(related='ticket_id.employee_id', string="Employee", store=True)
    family_member = fields.Many2one('res.partner', string='Family Member', required=True)
    ticket_details = fields.Char(string="Ticket Details")
    ticket_rate = fields.Float(string="Ticket Fare")
    ticket_price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.onchange("employee_id")
    def onchange_employee(self):
        res = {}
        if self.ticket_id.employee_id:
            self.family_member = False
            res["domain"] = {"family_member": [("id", "in", [m.family_member.id for m in self.employee_id.employee_visa_details_ids])]}
        return res
