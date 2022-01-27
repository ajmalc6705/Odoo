# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons import decimal_precision as dp


class MedicalTeethTreatment(models.Model):
    _inherit = "medical.teeth.treatment"

    def _get_treatment_dom_id(self):
        if self.appt_id.insurance_id:
            doc_ids = []
            for coverage_treatmts in self.appt_id.insurance_id.company_id.treatment_ids:
                doc_ids.append(coverage_treatmts.id)
            for non_coverage_treatmts in self.appt_id.insurance_id.company_id.non_coverage_treatment_ids:
                doc_ids.append(non_coverage_treatmts.id)
            for consultation_treatmts in self.appt_id.insurance_id.company_id.consultation_treatment_ids:
                doc_ids.append(consultation_treatmts.id)
            domain = [('id', 'in', doc_ids), ('is_treatment', '=', True),
                      ('company_id', '=', self.appt_id.company_id.id)]
        else:
            domain = [('is_treatment', '=', True), ('is_clinic_treatment', '=', True),
                      ('company_id', '=', self.appt_id.company_id.id)]
        return domain

    @api.onchange('description')
    def onchange_treatment_ids(self):
        domain = self._get_treatment_dom_id()
        return {
            'domain': {'description': domain}
        }

    def _get_tooth_id(self):
        domain_company = []
        if self.child:
            domain_company = [('child', '=', True)]
        else:
            domain_company = [('child', '=', False)]
        return domain_company

    patient_id = fields.Many2one('medical.patient', 'Patient Details', readonly=False)
    child = fields.Boolean('Child')
    teeth_id = fields.Many2one('teeth.code', 'Tooth', readonly=False)
    description = fields.Many2one('product.product', 'Description', readonly=False, required=True,
                                  domain=_get_treatment_dom_id)
    detail_description = fields.Text('Surface', readonly=False)
    state = fields.Selection(
        [('planned', 'Planned'), ('condition', 'Condition'), ('completed', 'Completed'), ('in_progress', 'In Progress'),
         ('invoiced', 'Invoiced'), ('initial_examination', 'Initial Examination')], 'Status', default='planned',
        readonly=True)
    dentist = fields.Many2one('medical.physician', 'Doctor')
    appt_id = fields.Many2one('medical.appointment', 'Appointment ID', required=True)
    teeth_code_rel = fields.Many2many('teeth.code', 'teeth_code_medical_teeth_treatment_rel', 'operation', 'teeth', domain=_get_tooth_id)
    diagnosis_id = fields.Many2one('diagnosis', 'Diagnosis')
    diagnosis_description = fields.Text('Notes')
    treatment_invoice = fields.Many2one("treatment.invoice")
    amt_paid_by_patient = fields.Float('Co-payment(%)', default=100, readonly=True, compute='_onchange_amt')
    amt_to_be_patient = fields.Float('Payment by Patient', compute='_onchange_amt')
    tree_control = fields.Boolean('Control')
    treatment_plan_number = fields.Char(string='T No.', compute='_compute_t_no',store = True)
    discount_fixed_percent = fields.Selection([('Fixed', 'Fixed'), ('Percent', 'Percent')],
                                              string='Disc Fixed/Percent', default=False, track_visibility='always')
    discount = fields.Float(string='Disc (%)', digits=dp.get_precision('Discount'), default=0.0,
                            track_visibility='always')
    discount_value = fields.Float(string='Disc Amt', track_visibility='always')

    @api.multi
    @api.model
    @api.depends('description')
    def _compute_t_no(self):
        for rec in self:
            if rec.appt_id.seq_treatment_number:
                rec.treatment_plan_number = rec.appt_id.seq_treatment_number

    @api.onchange('child')
    def onchange_child(self):
        get_tooth_id = self._get_tooth_id()
        return {
            'domain': {'teeth_code_rel': get_tooth_id}
        }

    @api.onchange('teeth_code_rel')
    def _onchange_tooth(self):
        for rcd in self:
            if rcd.teeth_code_rel:
                count = 0
                multi_tooth = 0
                teeth = False
                surface = ""
                for teeth_code in rcd.teeth_code_rel:
                    if not multi_tooth:
                        if teeth_code.name == 'Upper Jaw':
                            teeth = teeth_code.id
                            multi_tooth = 1
                            surface = 'Upper_Jaw'
                        elif teeth_code.name == 'Lower Jaw':
                            teeth = teeth_code.id
                            multi_tooth = 1
                            surface = 'Lower_Jaw'
                        elif teeth_code.name == 'Full Mouth':
                            teeth = teeth_code.id
                            multi_tooth = 1
                            surface = 'Full_mouth'
                        elif teeth_code.name == 'No Tooth':
                            teeth = teeth_code.id
                            multi_tooth = 1
                            surface = 'No_tooth'
                        else:
                            pass

                if multi_tooth:
                    rcd.teeth_code_rel = [(6, 0, [teeth])]
                else:
                    for i in rcd.teeth_code_rel:
                        count += 1
                        teeth_name = ""
                        teeth_obj = self.env['chart.selection'].search([])
                        teeth_chart_selection = teeth_obj[-1]
                        if teeth_chart_selection.type == 'palmer':
                            teeth_name = str(i.palmer_name)
                        elif teeth_chart_selection.type == 'iso':
                            teeth_name = str(i.iso)
                        else:
                            teeth_name = str(i.name)
                        # teeth_name = str(i.display_name)
                        if rcd.child:
                            if count == 1:
                                teeth = i.id
                                surface = 'chcap_' + teeth_name
                            else:
                                surface = surface + ',chcap_' + teeth_name
                        else:
                            if count == 1:
                                teeth = i.id
                                surface = 'toothcap_' + teeth_name
                            else:
                                surface = surface + ',toothcap_' + teeth_name
                rcd.update({'detail_description': surface})
                if count == 1:
                    rcd.teeth_id = teeth
                else:
                    rcd.teeth_id = teeth
            else:
                rcd.teeth_id = False
                rcd.detail_description = ""

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('planned', 'initial_examination'):
                raise ValidationError(_('You can delete only the record with planned status.'))
        return super(MedicalTeethTreatment, self).unlink()

    @api.multi
    def action_go_back(self):
        for result in self:
            invoiced_treatments = self.env['treatment.invoice'].search([('treatment_id', '=', result.id)])
            if invoiced_treatments:
                for i in invoiced_treatments:
                    if result.state == 'in_progress':
                        if i.appointment_id.state in ['done', 'visit_closed']:
                            raise ValidationError(_("You can't do this as the invoice is already generated."
                                                    " Try reopen appointment %s" % i.appointment_id.name))
                        i.unlink()
                        result.inv_status = 'draft'
                        result.state = 'planned'
                    else:
                        result.state = 'in_progress'
            else:
                if result.state == 'in_progress':
                    result.state = 'planned'
                else:
                    result.state = 'in_progress'
            result.appt_id.create_patient_appt_attach_treatment_plan()

    @api.multi
    def action_proceed(self):
        for result in self:
            if result.state == 'planned':
                result.write({'state': 'in_progress'})
            else:
                result.write({'state': 'completed'})
            if result.inv_status != "invoiced":
                invoiced_treatments = self.env['treatment.invoice'].search([('treatment_id', '=', result.id)])
                if invoiced_treatments:
                    pass
                else:
                    if result.patient_id:
                        if result.appt_id.state in ['checkin', 'ready']:
                            result.inv_status = "invoiced"
                            qty = 1
                            if result.description.apply_quantity_on_payment_lines:
                                qty = len(result.teeth_code_rel)
                            if qty == 0:
                                qty = 1
                            amt_lst_price = result.unit_price * qty
                            unit_price_here = result.unit_price
                            if not unit_price_here:
                                unit_price_here = result.description.lst_price
                            if not amt_lst_price:
                                amt_lst_price = result.description.lst_price  * qty
                            discount_value = 0
                            if result.discount_fixed_percent == 'Fixed':
                                if result.discount_value:
                                    discount_value = result.discount_value
                            if result.discount_fixed_percent == 'Percent':
                                if result.discount:
                                    discount_value = (result.discount * amt_lst_price) / 100
                            amt_lst_price -= discount_value
                            vals = {'appointment_id': result.appt_id.id,
                                    'treatment_id': result.id,
                                    'description': result.description.id,
                                    'teeth_code_rel': [[6, 0, result.teeth_code_rel.ids]],
                                    'diagnosis_id': result.diagnosis_id.id,
                                    'note': result.detail_description,
                                    'amount': amt_lst_price,
                                    'discount_fixed_percent': result.discount_fixed_percent,
                                    'discount': result.discount,
                                    'discount_value': result.discount_value,
                                    'unit_price': unit_price_here,
                                    'actual_amount': result.actual_amount,
                                    }
                            inv_id = self.env['treatment.invoice'].create(vals)
                        else:
                            dom = [('state', 'in', ['checkin', 'ready']),
                                   ('patient', '=', result.patient_id.id)]
                            app_id = self.env['medical.appointment'].search(dom)
                            appt_id = False
                            if app_id:
                                appt_id = app_id[-1]
                            if appt_id:
                                result.inv_status = "invoiced"
                                # old_appt_id = result.appt_id
                                # old_appt_id.create_patient_appt_attach_treatment_plan()
                                result.appt_id = appt_id.id
                                vals = {'appointment_id': appt_id.id,
                                        'treatment_id': result.id,
                                        'description': result.description.id,
                                        'teeth_code_rel': [[6, 0, result.teeth_code_rel.ids]],
                                        'diagnosis_id': result.diagnosis_id.id,
                                        'note': result.detail_description,
                                        'amount': result.amount,
                                        'discount_fixed_percent': result.discount_fixed_percent,
                                        'discount': result.discount,
                                        'discount_value': result.discount_value,
                                        'unit_price': result.unit_price,
                                        'actual_amount': result.actual_amount,
                                        }
                                inv_id = self.env['treatment.invoice'].create(vals)
            else:
                if result.patient_id and result.appt_id.state not in ['checkin', 'ready']:
                    dom = [('state', 'in', ['checkin', 'ready']),
                           ('patient', '=', result.patient_id.id)]
                    app_id = self.env['medical.appointment'].search(dom)
                    appt_id = False
                    if app_id:
                        appt_id = app_id[-1]
                    if appt_id:
                        # old_appt_id = result.appt_id
                        # old_appt_id.create_patient_appt_attach_treatment_plan()
                        result.appt_id = appt_id.id
            result.appt_id.create_patient_appt_attach_treatment_plan()

    @api.model
    def create(self, vals):
        result = super(MedicalTeethTreatment, self).create(vals)
        if result.detail_description and len(result.detail_description) > 1:
            if result.detail_description[:2] == 'ch':
                result.child = True
        if result.initial:
            result.state = "initial_examination"

        if result.tree_control and not result.teeth_code_rel:
            raise ValidationError(_('Please enter Tooth number properly..'))
        return result

    @api.model
    def write(self, vals):
        if 'appt_id' in list(vals.keys()):
            flag = 0
            for i in self.appt_ids:
                if i.id == vals['appt_id']:
                    flag = 1
            if not flag:
                vals['appt_ids'] = [(4, vals['appt_id'])]
        if 'teeth_code_rel' in list(vals.keys()) and vals['teeth_code_rel'] == [[6, False, []]] and self.tree_control:
            raise ValidationError(_('Please enter Tooth number properly..'))
        if 'detail_description' in list(vals.keys()) and len(vals['detail_description']) > 1:
            if vals['detail_description'][:2] == 'ch':
                vals['child'] = True
        if 'initial' in list(vals.keys()):
            if vals['initial']:
                vals['state'] = "initial_examination"
            else:
                vals['state'] = 'planned'

        result = super(MedicalTeethTreatment, self).write(vals)
        # for i in self:
        #     if not i.teeth_code_rel:
        #         raise ValidationError(_('Please enter Tooth number properly..'))
        return result


    def print_treatment_plan(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Print Treatment Plan'),
            'view_mode': 'form',
            'res_model': 'treatment.plan.wizard',
            'context': {'default_appt_id': self[-1].appt_id.id,'operation_ids':self.ids},
        }
