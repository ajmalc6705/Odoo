from odoo import api, fields, models
from datetime import datetime, timedelta


class ServiceConsumablesWizard(models.TransientModel):
    _name = "service.consumable.report"

    def _get_doctor_id(self):
        domain = []
        if self.department_ids:
            domain += [('department_id', 'in', self.department_ids.ids)]
        doc_ids = None
        group_dental_doc_menu = self.env.user.has_group('pragtech_dental_management.group_dental_doc_menu')
        group_dental_user_menu = self.env.user.has_group('pragtech_dental_management.group_dental_user_menu')
        group_dental_mng_menu = self.env.user.has_group('pragtech_dental_management.group_dental_mng_menu')
        if (group_dental_doc_menu and not group_dental_user_menu and not group_dental_mng_menu):
            partner_ids = self.env['res.partner'].search([('user_id', '=', self.env.user.id), ('is_doctor', '=', True),
                                                          ('company_id', '=', self.company_id.id)]).ids
            if partner_ids:
                doc_ids = self.env['medical.physician'].search([('name', 'in', partner_ids),
                                                                ('company_id', '=', self.company_id.id)]).ids
            domain += [('id', 'in', doc_ids)]
        return domain

    is_only_doctor = fields.Boolean()
    date_from = fields.Date("From", required=True, default=fields.Date.context_today)
    date_to = fields.Date("To", required=True, default=fields.Date.context_today)
    department_ids = fields.Many2many(comodel_name="medical.department",  string="Departments")
    doctor_ids = fields.Many2many('medical.physician', string="Doctors", domain=_get_doctor_id)

    @api.onchange('department_ids')
    def onchange_department_ids(self):
        return {
            'domain': {
                'doctor_ids': self._get_doctor_id()
            }
        }

    @api.model
    def default_get(self, fields):
        res = super(ServiceConsumablesWizard, self).default_get(fields)
        res['is_only_doctor'] = False
        self._get_doctor_id()
        doc_ids = None
        group_dental_doc_menu = self.env.user.has_group('pragtech_dental_management.group_dental_doc_menu')
        group_dental_user_menu = self.env.user.has_group('pragtech_dental_management.group_dental_user_menu')
        group_dental_mng_menu = self.env.user.has_group('pragtech_dental_management.group_dental_mng_menu')
        if group_dental_doc_menu and not group_dental_user_menu and not group_dental_mng_menu:
            res['is_only_doctor'] = True
            dom_partner = [('user_id', '=', self.env.user.id), ('is_doctor', '=', True)]
            partner_ids = [x.id for x in self.env['res.partner'].search(dom_partner)]
            if partner_ids:
                doc_ids = [x.id for x in self.env['medical.physician'].search([('name', 'in', partner_ids)])]
        if doc_ids:
            res['doctor_ids'] = doc_ids[0]
        return res

    @api.multi
    def button_patient_top(self):
        dom_dpmt_id_list = []
        dom_dpmt_name_list = ''
        for dpmt in self.department_ids:
            dom_dpmt_id_list.append(dpmt.id)
            if dom_dpmt_name_list:
                dom_dpmt_name_list += ", "
            dom_dpmt_name_list += dpmt.name
        dom_doc_id_list = []
        dom_doc_name_list = ''
        for doc in self.doctor_ids:
            dom_doc_id_list.append(doc.id)
            if dom_doc_name_list:
                dom_doc_name_list += ", "
            dom_doc_name_list += doc.name.name
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'department_ids': dom_dpmt_id_list,
            'dom_dpmt_name_list': dom_dpmt_name_list,
            'doctor_ids': dom_doc_id_list,
            'dom_doc_name_list': dom_doc_name_list,
                }
        return self.env.ref('service_consumable.report_service_consumables_pdf').report_action(self, data=data)


class ReportServiceConsumables(models.AbstractModel):
    _name = 'report.service_consumable.report_service_consumables'

    @api.model
    def get_request_details_moving(self, date_from=False, date_to=False, doctor_ids=False, department_ids=False):

        dom = [('appointment_sdate', '>=', date_from),
               ('appointment_edate', '<=', date_to),
               ('delivery_id', '!=', False),
               # ('state', 'in', ['visit_closed', 'done'])
               ]
        department_ids_name = ''
        if department_ids:
            dom.append(('doctor.department_id', 'in', department_ids))
            department_ids_name = department_ids
        if doctor_ids:
            dom.append(('doctor', 'in', doctor_ids))
        medical_appt = self.env['medical.appointment'].search(dom, order="appointment_sdate asc")
        return {
            'date_from': date_from,
            'date_to': date_to,
            'doctor_ids': doctor_ids,
            'medical_appt': medical_appt,
            'department_ids': department_ids_name,
        }

    @api.multi
    def get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(self.get_request_details_moving(data['date_from'], data['date_to'], data['doctor_ids'],
                                                    data['department_ids']))
        return data
