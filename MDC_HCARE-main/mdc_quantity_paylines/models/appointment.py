# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)


class MedicalAppointment(models.Model):
    _inherit = 'medical.appointment'

    @api.multi
    def get_appt_payment_quantity(self, treatment_id):
        _logger.info('nnnnnnnnnnnnnnnnnn..........................:mdc_quantity_paylines')
        return treatment_id.qty