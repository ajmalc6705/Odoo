# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: ALKIDHMA
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

from odoo import models, fields, api
from lxml import etree
import json


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    grade_id = fields.Many2one("hr.grade.grade", "Grade")
    rank_id = fields.Many2one("hr.rank.rank", "Rank")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(HrEmployee, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                                      toolbar=toolbar,
                                                                      submenu=submenu)
        doc = etree.XML(result['arch'])
        if self.env.user.has_group('aks_employee_grade_master.group_access_of_grade_rank'):
            if doc.xpath("//field[@name='grade_id']"):
                node = doc.xpath("//field[@name='grade_id']")[0]
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = False
                node.set("modifiers", json.dumps(modifiers))
            if doc.xpath("//field[@name='rank_id']"):
                node = doc.xpath("//field[@name='rank_id']")[0]
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = False
                node.set("modifiers", json.dumps(modifiers))

        result['arch'] = etree.tostring(doc, encoding='unicode')
        return result

    @api.onchange("grade_id")
    def onchange_grade(self):
        res = {}
        if self.grade_id:
            self.rank_id = False
            res["domain"] = {"rank_id": [("id", "in", self.grade_id.rank_ids.ids)]}
        return res
