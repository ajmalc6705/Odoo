# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: Al Kidhma Group
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


class EmployeeRelation(models.Model):
    _inherit = 'aks.employee.relation'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class VisaDetailsLine(models.Model):
    _inherit = 'hr.employee.visa.details.line'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class VisaType(models.Model):
    _inherit = 'aks.visa.type'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class RestrictEmployeeSalary(models.Model):
    _inherit = 'restrict.employee.salary'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DbBackup(models.Model):
    _inherit = 'db.backup'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class AppointmentStateColor(models.Model):
    _inherit = 'appointment.state.color'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class AppointmentHistory(models.Model):
    _inherit = 'appointment.history'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalHospitalOperatingRoom(models.Model):
    _inherit = 'medical.hospital.oprating.room'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class CalenderConfig(models.Model):
    _inherit = 'calender.config'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class WorkingTime(models.Model):
    _inherit = 'working.time'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ConsentDetailsCategory(models.Model):
    _inherit = 'consent.details.category'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ConsentDetails(models.Model):
    _inherit = 'consent.details'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ConsentDashboard(models.Model):
    _inherit = 'consent.dashboard'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class SelectionFieldValues(models.Model):
    _inherit = 'selection.field.values'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class BooleanFieldValues(models.Model):
    _inherit = 'boolean.field.values'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DocumentType(models.Model):
    _inherit = 'document.type'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class EmployeeDocument(models.Model):
    _inherit = 'employee.document'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class EmployeeExpiryAlert(models.Model):
    _inherit = 'employee.expiry.alert'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


# class HrAllowance(models.Model):
#     _inherit = 'hr.allowance'
#
#     company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


# class AllowanceContract(models.Model):
#     _inherit = 'allowance.contract'
#
#     company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class TerminationDetails(models.Model):
    _inherit = 'termination.details'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class LabRequest(models.Model):
    _inherit = 'lab.request'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class TeethTreatment(models.Model):
    _inherit = 'medical.teeth.treatment'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalAppointment(models.Model):
    _inherit = 'medical.appointment'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalPhysician(models.Model):
    _inherit = 'medical.physician'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalInsurance(models.Model):
    _inherit = 'medical.insurance'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class TeethTreatment(models.Model):
    _inherit = 'medical.teeth.treatment'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ChartSelection(models.Model):
    _inherit = 'chart.selection'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ComplaintFinding(models.Model):
    _inherit = 'complaint.finding'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class Complaints(models.Model):
    _inherit = 'complaints'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ConsentConsent(models.Model):
    _inherit = 'consent.consent'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalDashboard(models.Model):
    _inherit = 'medical.dashboard'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ComplaintFindingDepartment(models.Model):
    _inherit = 'complaints.findings.department'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DiagnosisDiagnosis(models.Model):
    _inherit = 'diagnosis'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class FindingsFindings(models.Model):
    _inherit = 'findings'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalSpeciality(models.Model):
    _inherit = 'medical.speciality'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DoseUnit(models.Model):
    _inherit = 'medical.dose.unit'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DrugForm(models.Model):
    _inherit = 'medical.drug.form'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicationDosage(models.Model):
    _inherit = 'medical.medication.dosage'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PatientNationality(models.Model):
    _inherit = 'patient.nationality'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PrimaryDiagnosis(models.Model):
    _inherit = 'primary.diagnosis'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class MedicalOccupation(models.Model):
    _inherit = 'medical.occupation'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class OperatingSummery(models.Model):
    _inherit = 'operation.summary'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PatientComplaintWizard(models.Model):
    _inherit = 'patient.complaint.wizard'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PatientComplaint(models.Model):
    _inherit = 'patient.complaint'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PatientFeedback(models.Model):
    _inherit = 'patient.feedback'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PatientSurvey(models.Model):
    _inherit = 'patient.survey'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PolicyHolder(models.Model):
    _inherit = 'policy.holder'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PrescriptionLine(models.Model):
    _inherit = 'prescription.line'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PrescriptionAdditionalLine(models.Model):
    _inherit = 'prescription.additional.line'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class PrescriptionAdditional(models.Model):
    _inherit = 'prescription.additional'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class Procedure(models.Model):
    _inherit = 'procedure'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ReferralDoctor(models.Model):
    _inherit = 'referral.dr'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class TeethCode(models.Model):
    _inherit = 'teeth.code'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class ProductConsumables(models.Model):
    _inherit = 'product.consumables'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class AppointmentConsumables(models.Model):
    _inherit = 'appt.consumables'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class CommissionSlab(models.Model):
    _inherit = 'commission.slab'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class DoctorInsurance(models.Model):
    _inherit = 'doctor.insurance'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


class SubInsurance(models.Model):
    _inherit = 'sub.insurar'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
