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

from odoo import models, fields


class HrRank(models.Model):
    _name = 'hr.rank.rank'
    _description = 'Rank of Employee'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    salary_range = fields.Text(string="Salary Range")
    grade_id = fields.Many2one("hr.grade.grade", string="Grade")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id)


class HrGrade(models.Model):
    _name = 'hr.grade.grade'
    _description = 'Grade of Employee'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    rank_ids = fields.One2many("hr.rank.rank", "grade_id", string="Ranks")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id)
