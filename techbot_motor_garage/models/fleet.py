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
import logging
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _rec_name = 'driver_id'

    sale_order_count = fields.Integer(compute='_compute_sale_count', string='Sales')
    #
    def _compute_sale_count(self):
        """
        Override original method to
        """
        # sale_obj = self.env['sale.order']
        # for partner in self:
        #     partner.sale_count = sale_obj.search_count([('partner_id', '=', partner.id)])
        #     _logger.info("partner.sale_count %s", partner.sale_count)

    def get_partner_sales(self):
        """
        Return an action that display fleet records related for the given partners.
        """
    #     sale_obj = self.env['sale.order']
    #     sale_ids = sale_obj.search([('partner_id', '=', self.id)]).mapped('id')
    #     sale_ids
    #     return {
    #         'domain': [('id', 'in', sale_ids)],
    #         'name': _('Sales'),
    #         'view_type': 'list',
    #         'view_mode': 'list,form',
    #         'res_model': 'sale.order',
    #         'view_id': False,
    #         'context': {'default_partner_id': self.id},
    #         'type': 'ir.actions.act_window'
    #     }

    mobile = fields.Char(string="Telephone")
    email = fields.Char(string="Email ID")

    @api.onchange('driver_id')
    def onchange_driver_id_techbot_motor_garage(self):
        """Methode to Change Email and Mobile number Based on Driver"""
        for rec in self:
            rec.mobile = rec.email = False
            if rec.driver_id:
                rec.email = rec.driver_id.email
                rec.mobile = rec.driver_id.mobile

    vehicle_reg_date = fields.Date(string='Date of Reg', help='Vehicle registration date')
    service_advisor_id = fields.Many2one('res.users', string="Advisor", copy=False, default=lambda self: self.env.uid)
    road_test_id = fields.Many2one('res.users', string="Diagnostic Road Test conducted by ", copy=False)
    service_contract = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Service Contract")

    # ******************** Position Vehicle Check ( Vehicle on floor ) : Interior Field details ******************
    inst_cluster_light = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                          string="Instrument Cluster Lights")
    int_light = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Interior Light")
    steering_wheel = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                      string="Steering Wheel/Play")
    ac_system = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                 string="Heating/ AC System Blower")
    safety_belt = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                   string="Safety Belts and Locks")
    parking_brake = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                     string='Parking Break System')
    sliding_roof = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Sliding Roof")
    vanity_mirror = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Vanity Mirror")
    door_handle = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Door Handle")
    seat = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Seats")
    shift_level = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Shift Level")
    inner_door_panel = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                        string="Inner Door Panel Trim")
    side_mirror = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                   string="Side Mirror Function")
    floor_mate = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                  string="Floor Mate")
    navigation_dvd = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                      string="Navigation DVD")
    roller_blind = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Roller Blind")

    # ******
    # Page : Interior and Exterior Position Vehicle Check ( Vehicle on floor ) : Exterior Field details ******
    wiper_blade = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                   string="Wiper Blades / Rubbers")
    exterior_light = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                      string="Exterior Light System Control Function")
    head_light = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                  string="Head Lights / Glass")
    wind_shield = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                   string="Windshield & Window Glasses Oil")
    rear_light = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                  string="Rear Lights / Glasses")

    # **************
    # Position Vehicle Check ( Vehicle on floor ) Engine Compartment Field details ****************

    visual_leaks = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Visual Leaks")
    engine_oil = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Engine Oil")
    power_steering_oil = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                          string="Power Steering Oil Level")
    break_fluid_oil = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                       string="Break Fluid Level")
    coolant_fluid_oil = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                         string="Coolant Fluid Level")
    wind_shield_fluid_oil = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                             string="WindShield Washing Fluid")
    v_belt = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="V Belt")

    # *************
    # Vehicle Check ( Vehicle on floor ) : "Vehicle Check ( Vehicle Completely Lifted Up)"  ************
    engine_leakage = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                      string="Engine Leakage")
    steering_rack = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                     string="Steering Rack/ Box")
    suspension = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                  string="Suspension/ Axle Mounting/ Tie Rods")
    break_line = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                  string="Brake Lines and Hoses")
    gear_box = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                string="Gear Box Leakage")
    propeller_shaft = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                       string="Propeller Shaft/ Flexible Coupling")
    exhaust_system = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                      string="Exhaust System")
    rear_axis = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                 string="Rear Axis Leakage")
    fuel_tank = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                 string="Fuel Tank and Lines")

    # *************
    # Vehicle Check ( Vehicle on floor ) : "Vehicle Check ( Vehicle Half Lifted Up)" ****************
    rims = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Rims/ Tyres")
    brake_pad_front_axle = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                            string="Brake Pads and Discs Front Axle")
    brake_pad_near_axle = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')],
                                           string="Brake Pads and Discs Near Axle")
    airmatic_abc = fields.Selection([('ok', 'OK'), ('advice', 'Advise'), ('urgent', 'Urgent')], string="Airmatic ABC")

    # ***************
    # Body and Pain Check  ******************************
    file_name_left = fields.Char("File Name for Car left side View")
    left_image = fields.Binary("Left Side View", help="Select image here")

    file_name_right = fields.Char("File Name for Car Right side View")
    right_image = fields.Binary("Right side View", help="Select image here")

    file_name_top = fields.Char("File Name for Car Top View")
    top_image = fields.Binary("Top View", help="Select image here")

    file_name_front = fields.Char("File Name for Car Front side View")
    front_image = fields.Binary("Front View", help="Select image here")

    file_name_back = fields.Char("File Name for Car Back side View")
    back_image = fields.Binary("Back View", help="Select image here")

    tyre_depth_fl = fields.Integer('Tyre Depth FL')
    tyre_depth_fr = fields.Integer('Tyre Depth FR')
    tyre_depth_rl = fields.Integer('Tyre Depth RL')
    tyre_depth_rr = fields.Integer('Tyre Depth RR')

    brake_pad_thi_fl = fields.Integer('Brake Pad Thickness FL')
    brake_pad_thi_fr = fields.Integer('Brake Pad Thickness FR')
    brake_pad_thi_rl = fields.Integer('Brake Pad Thickness RL')
    brake_pad_thi_rr = fields.Integer('Brake Pad Thickness RR')

    wheel_rim_cond_l = fields.Integer('Wheel Rim Condition L')
    wheel_rim_cond_r = fields.Integer('Wheel Rim Condition R')

    regi_card = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Registration Card Available")
    serv_booklet = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string="Service Booklet/ Digital Service Booklet Available")
    spare_tyre_pres = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Spare Tyre Present")
    warning_triangle = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Warning Triangle Available")

    first_aid = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="First AID Kit Present")
    tool_kit = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Tool Kit Present")
    jack_present = fields.Selection([('yes', 'Yes'), ('no', 'No')], string=" Jack Present")
    keep_removed_parts = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Keep Removed Parts")
    others_note = fields.Char(string="Others", required=False, )

    insurance_company_id = fields.Many2one('res.partner', string='Insurance Company')
    insurance_claim_no = fields.Char(string='Insurance Claim Number')

    description = fields.Text('Description')

    def job_card_quotation_button_fun(self):
        """ Method to Create Job Card"""
        fleet_obj = self.env['fleet.vehicle']
        vehicle_ids = fleet_obj.search([('driver_id', '=', self.id)]).mapped('id')
        return {
            'name': 'Job Card Creation',
            'domain': [('id', 'in', vehicle_ids)],
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'kanban,tree,form',
            'context': {'default_partner_id': self.driver_id.id,
                        'default_insurance_company_id': self.insurance_company_id.id,
                        'default_claim_no': self.insurance_claim_no,
                        'default_vehicle_model': self.model_id.id,
                        'default_vehicle_no_plate': self.license_plate,
                        'default_vin_sn': self.vin_sn,
                        'default_vehicle_reg_date': self.vehicle_reg_date,
                        'default_vehicle_km': self.odometer,
                        'default_car_left_image': self.left_image,
                        'default_car_right_image': self.right_image,
                        'default_diagnostic_test_id': self.road_test_id.id,
                        "default_service_contract": self.service_contract
                        },
            'target': 'new',
        }

    def sale_quotation_button_fun(self):
        """ Method to Create Sale Quotation"""
        fleet_obj = self.env['fleet.vehicle']
        vehicle_ids = fleet_obj.search([('driver_id', '=', self.id)]).mapped('id')
        return {
            'name': 'Sale Quotation',
            'domain': [('id', 'in', vehicle_ids)],
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'kanban,tree,form',
            'context': {'default_partner_id': self.driver_id.id,
                        'default_insurance_company_id': self.insurance_company_id.id,
                        'default_claim_no': self.insurance_claim_no,
                        'default_vehicle_model': self.model_id.id,
                        'default_vehicle_no_plate': self.license_plate,
                        'default_vin_sn': self.vin_sn,
                        'default_vehicle_reg_date': self.vehicle_reg_date,
                        'default_vehicle_km': self.odometer,
                        'default_diagnostic_test': self.road_test_id.id,
                        "default_service_contract": self.service_contract

                        },
            'target': 'new',
        }

    def action_email_send_button_fun(self):
        """ Method to Send mail to customer"""
        self.ensure_one()
        template = self.env.ref("techbot_motor_garage.fleet_email_template", False)
        # print("ee= ", template)
        compose_form = self.env.ref("mail.email_compose_message_wizard_form", False)
        ctx = dict(
            default_model="fleet.vehicle",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
        )
        return {
            "name": _("Send Vehicle Check By Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }



