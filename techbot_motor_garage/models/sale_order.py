# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

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
from odoo import api, fields, models, api, _
from odoo.exceptions import ValidationError,Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mobile = fields.Char(string="Telephone", required=False)
    email = fields.Char(string="Email ID", required=False)
    # Vehicle Identification Number Serial Number (vin_sn)/ Chase No
    vin_sn = fields.Char(string="VIN", required=False)
    # date_order = fields.Datetime(string='In Date', required=True, readonly=True, index=True,
    #                              states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
    #                              default=fields.Datetime.now)

    out_date = fields.Datetime(string="Out Date", copy=False, required=False)
    vehicle_model = fields.Many2one('fleet.vehicle.model', string='Model', readonly=True)
    vehicle_reg_date = fields.Char(string='Date of Reg')
    vehicle_km = fields.Float(string='KM')
    vehicle_no_plate = fields.Char(string='Plate No')
    service_contract = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Service Contract")
    # service_contract_yes = fields.Boolean(string='Yes')
    # service_contract_no = fields.Boolean(string='No')
    diagnostic_test_id = fields.Many2one('res.users', string="Diagnostic Road Test conducted by ", copy=False)
    fuel = fields.Char()
    claim_no = fields.Char(string="Clim no", required=False)
    insurance_company_id = fields.Many2one('res.partner', string="Insurance Company", required=False)

    # GET DRIVER NAME AND MOBILE NUMBER AND EMAILS
    @api.onchange('partner_id')
    def onchange_partner_id_techbot_motor_garage_sale(self):
        for rec in self:
            rec.mobile = rec.email = False
            if rec.partner_id:
                rec.mobile = rec.partner_id.mobile
                rec.email = rec.partner_id.email

    digital_signature = fields.Binary(string="Digital Signature", copy=False)

    # def submit_for_approval(self):
    #     for rec in self:
    #         rec.state = 'waiting_for_approval'
    #         self.send_notification_to_salespersons(rec)
    #
    # def action_approve_button(self):
    #     for rec in self:
    #         if not rec.digital_signature:
    #             raise ValidationError(_("Please Add Digital Signature in Approval Signature Page"))
    #         rec.state = 'approved'

    def print_quotation_jc(self):
        """  Method to call JC PDF report       """
        action = self.env["ir.actions.actions"]._for_xml_id("techbot_motor_garage.action_report_saleorder")
        return action
