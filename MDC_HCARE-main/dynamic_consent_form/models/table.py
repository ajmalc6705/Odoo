# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class Model(models.Model):
	_inherit = 'ir.model'
	
	consent_table = fields.Boolean('Is machine related?')

	@api.model
	def create(self, vals):
		return super(Model, self).create(vals) 
	
	@api.multi
	def update_consent_view(self):
		for rec in self:
			for view in rec.view_ids.filtered(lambda r: r.type=='tree'):
				arch_view ="""<tree editable="bottom">"""
				for field in rec.field_id.filtered(lambda r: r.visible_in_consent_tree):
					arch_view += """<field name='""" + field.name+"""'/>"""
				arch_view += """</tree>"""
				view.arch_base = arch_view
				
