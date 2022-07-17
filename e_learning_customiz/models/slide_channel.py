from odoo import models, Command, fields, api, _
from odoo.exceptions import ValidationError

class SlidChannelPartnerInher(models.Model):
    _inherit = 'slide.channel.partner'


