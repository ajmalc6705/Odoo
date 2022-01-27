# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from ast import literal_eval


class HrContract(models.Model):
    _inherit = 'hr.contract'

    overtime_hourly_rate_holiday = fields.Float('Overtime Hourly rate(Holiday)', compute='get_ot_rate')
    overtime_hourly_rate_working_day = fields.Float('Overtime Hourly rate(Working day)', compute='get_ot_rate')

    @api.multi
    @api.model
    def get_ot_rate(self):
        conf_obj = self.env['ir.config_parameter'].sudo()
        for rec in self:
            overtime_hourly_rate_holiday = literal_eval(conf_obj.get_param('hr_attendance_overtime.overtime_hourly_rate_holiday',
                                                                           default='False'))
            overtime_hourly_rate_working_day = literal_eval(conf_obj.get_param('hr_attendance_overtime.overtime_hourly_rate_working_day',
                                                                           default='False'))
            rec.overtime_hourly_rate_holiday = overtime_hourly_rate_holiday
            rec.overtime_hourly_rate_working_day = overtime_hourly_rate_working_day