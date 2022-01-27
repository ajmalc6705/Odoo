from odoo import models, api
from datetime import datetime
from odoo.tools.misc import xlwt


class ClaimWizard(models.TransientModel):
    _inherit = 'dental.claim.wizard'

    @api.multi
    def generate_mednet_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold_red = xlwt.easyxf("pattern: pattern solid, fore-colour dark_purple;"
                               "align: wrap on, horiz center, vert center;font: bold on;"
                               "borders: left medium, right medium, top medium, bottom medium;"
                               "font: name Verdana, color white;", num_format_str='#,##0.00')
        bold = xlwt.easyxf("pattern: pattern solid, fore-colour grey25;"
                           "align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color black;", num_format_str='#,##0.00')
        bold_right = xlwt.easyxf("pattern: pattern solid, fore-colour grey25;"
                                 "align: wrap on, horiz right, vert center;font: bold on;"
                                 "borders: left medium, right medium, top medium, bottom medium;"
                                 "font: name Verdana, color black;", num_format_str='#,##0.00')
        bold_nocolor = xlwt.easyxf("pattern: pattern solid, fore-colour white;"
                                   "align: wrap on, horiz center, vert center;font: bold on;"
                                   "borders: left medium, right medium, top medium, bottom medium;"
                                   "font: name Verdana, color black;", num_format_str='#,##0.00')
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        r = 0
        worksheet.write_merge(0, 0, 0, 10, 'STATEMENT OF ACCOUNT', bold_red)
        worksheet.row(r).height_mismatch = True
        worksheet.row(r).height = 200 * 3
        worksheet.write_merge(2, 2, 0, 5, 'Provider Name: ' + self.company_id.name, bold_nocolor)
        worksheet.write_merge(2, 2, 6, 10, 'Billing Month: ', bold_nocolor)
        worksheet.write_merge(3, 3, 0, 5, 'Provider Code: E16', bold_nocolor)
        worksheet.write_merge(3, 3, 6, 10, 'Claim Type: DENTAL', bold_nocolor)
        c = 0
        r = 5
        data_list = []
        output_header = ['SN', 'FILE NO.', 'Mednet Card No', 'Patient Name', 'Service Date', 'Invoice No',
                         'Gross Amount', 'Discount', 'Co-Payment/ Deductible', 'Net Amount', 'Dr. No.']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 6
            c += 1
        inv_data = self.env['account.invoice'].search \
            ([('date_invoice', '>=', self.from_date), ('date_invoice', '<=', self.to_date),
              ('patient', '!=', False), ('insurance_company', '=', self.company.id),
              ('state', 'in', ('open', 'paid')),
              ('company_id', '=', self.company_id.id)])
        #         data = []
        sl_no = 0
        gross_total = 0
        disc_total = 0
        coshare_total = 0
        ins_amt_total = 0
        inv_len = 0
        for inv in inv_data:
            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1
            if inv.appt_id and count:
                apt = inv.appt_id
                inv_len += 1
                for line in inv.invoice_line_ids:
                    data = []
                    sl_no += 1
                    data.append(str(sl_no))
                    data.append(inv.patient.patient_id)
                    if inv.insurance_card.insurance_id_no:
                        data.append(inv.insurance_card.insurance_id_no)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    if apt.appointment_sdate:
                        apt_date = datetime.strptime(apt.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                        apt_date = apt_date.strftime('%d/%m/%Y')
                        data.append(apt_date)
                    else:
                        data.append(' ')
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    gross = line.price_unit * line.quantity
                    if inv.is_special_case:
                        if inv.share_based_on == 'Global':
                            disc = 0
                            copay = 0
                        else:
                            disc = gross - line.after_treatment_grp_disc
                            copay = line.patient_share
                    else:
                        disc = (gross * line.discount_amt) / 100
                        copay = line.price_initial_case_3_copay
                    data.append(gross)
                    data.append(disc)
                    data.append(copay)
                    ins_amt = gross - disc - copay
                    data.append(ins_amt)
                    gross_total += gross
                    disc_total += disc
                    coshare_total += copay
                    ins_amt_total += ins_amt
                    dr_no = ''
                    for dr in inv.dentist.doctor_insurance_ids:
                        if dr.ins_company_id.id == self.company.id:
                            dr_no = dr.doctor_no
                    data.append(dr_no)
                    data_list.append(data)

        r += 1
        for data in data_list:
            c = 0
            for item in data:
                if c == 3:
                    worksheet.write(r, c, item, normal_left)
                elif c in (6, 7, 8, 9):
                    worksheet.write(r, c, item, normal_right)
                else:
                    worksheet.write(r, c, item, normal)
                c += 1
            r += 1
        c = 0
        total_list = ['TOTAL CLAIMS :', str(int(inv_len)), '', '', '', 'TOTAL', gross_total, disc_total, coshare_total,
                      ins_amt_total, '']
        for item in total_list:
            if c in (6, 7, 8, 9):
                worksheet.write(r, c, item, bold_right)
            else:
                worksheet.write(r, c, item, bold)
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 4
            c += 1

    @api.multi
    def generate_nextcare_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold_black = xlwt.easyxf("align: horiz center, vert center;font: bold on;"
                                 "font: name Verdana, color black;", num_format_str='#,##0.00')
        bold = xlwt.easyxf("align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color red;", num_format_str='#,##0.00')
        bold_right = xlwt.easyxf("align: wrap on, horiz right, vert center;font: bold on;"
                                 "borders: left medium, right medium, top medium, bottom medium;"
                                 "font: name Verdana, color red;", num_format_str='#,##0.00')
        worksheet.write_merge(0, 0, 0, 11, 'DETAILED STATEMENT OF ACCOUNT', bold_black)
        worksheet.row(0).height_mismatch = True
        worksheet.row(0).height = 200 * 4
        r = 2
        c = 0
        from_date = (datetime.strptime(self.from_date, '%Y-%m-%d'))
        from_date = from_date.strftime('%d/%m/%Y %H:%M:%S').split(' ')[0]
        to_date = (datetime.strptime(self.to_date, '%Y-%m-%d'))
        to_date = to_date.strftime('%d/%m/%Y %H:%M:%S').split(' ')[0]
        output_header = ['Period From:', from_date, 'Period To:', to_date]
        for item in output_header:
            worksheet.write(r, c, item, bold_black)
            c += 2
        r += 1
        c = 0
        output_header = ['Insurance Company:', self.company.name,
                         'Report Date:', datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                         ]
        for item in output_header:
            worksheet.write(r, c, item, bold_black)
            c += 2
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        r += 2
        c = 0
        data_list = []
        output_header = ['SN', 'DATE OF SERVICE', 'INVOICE NO.', 'ASOAP #', 'APPROVAL CODE', 'NAME', 'CARD NO.',
                         'GROSS AMOUNT', 'DISCOUNT', 'COLLECTED AMOUNT', 'NET CLAIMED AMOUNT', 'DR. NO.']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 4
            c += 1
        inv_data = self.env['account.invoice'].search([('date_invoice', '>=', self.from_date),
                                                       ('date_invoice', '<=', self.to_date), ('patient', '!=', False),
                                                       ('insurance_company', '=', self.company.id),
                                                       ('state', 'in', ('open', 'paid')),
                                                       ('company_id', '=', self.company_id.id)])
        sl_no = 0
        gross_total = 0
        disc_total = 0
        coshare_total = 0
        ins_amt_total = 0
        for inv in inv_data:
            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1
            if count:
                for line in inv.invoice_line_ids:
                    if line.apply_insurance:
                        data = []
                        sl_no += 1
                        data.append(str(int(sl_no)))
                        apt = inv.appt_id
                        if apt.appointment_sdate:
                            apt_date = datetime.strptime(inv.appt_id.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                            apt_date = apt_date.strftime('%d/%b/%Y')
                            data.append(apt_date)
                        else:
                            data.append(' ')
                        if inv.insurance_invoice:
                            data.append(inv.insurance_invoice.number)
                        else:
                            data.append('')
                        data.append('')
                        data.append(inv.pre_approval_code or '')
                        data.append(inv.patient.name.name)
                        data.append(inv.insurance_card.number or '')
                        gross = line.price_unit * line.quantity
                        if inv.is_special_case:
                            if inv.share_based_on == 'Global':
                                disc = 0
                                copay = 0
                            else:
                                disc = gross - line.after_treatment_grp_disc
                                copay = line.patient_share
                        else:
                            disc = (gross * line.discount_amt) / 100
                            copay = line.price_initial_case_3_copay
                        data.append(gross)
                        data.append(disc)
                        data.append(copay)
                        ins_amt = gross - disc - copay
                        data.append(ins_amt)
                        gross_total += gross
                        disc_total += disc
                        coshare_total += copay
                        ins_amt_total += ins_amt
                        dr_no = ''
                        for dr in inv.dentist.doctor_insurance_ids:
                            if dr.ins_company_id.id == self.company.id:
                                dr_no = dr.doctor_no
                        data.append(dr_no)
                        data_list.append(data)
        r += 1
        for data in data_list:
            c = 0
            for item in data:
                if c in (4, 5, 6):
                    worksheet.write(r, c, item, normal_left)
                elif c in (7, 8, 9, 10):
                    worksheet.write(r, c, item, normal_right)
                else:
                    worksheet.write(r, c, item, normal)
                c += 1
            r += 1
        c = 0
        total_list = ['TOTAL', '', '', '', '', '', '', gross_total, disc_total, coshare_total,
                      ins_amt_total, '']
        for item in total_list:
            if c == 0:
                worksheet.write(r, c, item, bold)
            else:
                worksheet.write(r, c, item, bold_right)
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 4
            c += 1

    @api.multi
    def generate_qlm_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold = xlwt.easyxf("pattern: pattern solid, fore-colour white;"
                           "align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color red;", num_format_str='#,##0.00')
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        r = 0
        c = 0

        data_list = []
        output_header = ['QLM Visit No./ Barcode No.', 'Member ID (MEM)', 'Patient Name', 'Benefit',
                         'Service Type (I/O)', 'Service Date', 'Invoice No.', 'Pre-Approval Code', 'Primary Diag Code',
                         'Primary Diag Description', '2nd Diag Code', 'Provider Treat Code',
                         'Provider Treat Description', 'Quantity', 'Gross Claim Amt', 'Discount', 'Ded/Co-payment',
                         'Co-insurance', 'Net Payable Amount', 'Treating Physician', 'Physician License No.',
                         'Clinic/Specialty', 'Provider File No.', 'Qatar ID', '3rd Diag Code', '4th Diag Code',
                         '5th Diag Code', 'Service Category', 'Sub Benefit', 'Inpatient Type (M/S)',
                         'Inpatient Admission Date', 'First Reported Date', 'Tooth No', 'LMP Date',
                         'Nature of Conception', 'CPT Code', 'Duration (for pharmacy)', 'Dosage (for pharmacy)',
                         'Investigation Result', 'Chief Compliant']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 5
            c += 1
        inv_data = self.env['account.invoice'].search(
            [('date_invoice', '>=', self.from_date), ('date_invoice', '<=', self.to_date),
             ('patient', '!=', False), ('insurance_company', '=', self.company.id),
             ('state', 'in', ('open', 'paid')),
             ('company_id', '=', self.company_id.id)])
        for inv in inv_data:
            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1
            if inv.appt_id and count:
                apt = inv.appt_id
                for line in inv.invoice_line_ids:
                    data = []
                    data.append(inv.appt_id.name)
                    if inv.insurance_card.insurance_id_no:
                        data.append(inv.insurance_card.insurance_id_no)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    data.append('D')
                    data.append('O')
                    if apt.appointment_sdate:
                        apt_date = datetime.strptime(apt.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                        apt_date = apt_date.strftime('%d/%b/%Y')
                        data.append(apt_date)
                    else:
                        data.append('')
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    if inv.pre_approval_code:
                        data.append(inv.pre_approval_code)
                    else:
                        data.append('')
                    data.append(line.diagnosis_id.code or '')
                    data.append(line.diagnosis_id.description or '')
                    data.append('')
                    data.append(line.product_id.default_code or '')
                    data.append(line.product_id.name or '')
                    data.append(str(int(line.quantity)))
                    gross = line.price_unit * line.quantity
                    if inv.is_special_case:
                        if inv.share_based_on == 'Global':
                            disc = 0
                            copay = 0
                        else:
                            disc = gross - line.after_treatment_grp_disc
                            copay = line.patient_share
                    else:
                        disc = (gross * line.discount_amt) / 100
                        copay = line.price_initial_case_3_copay
                    data.append(gross)
                    data.append(disc)
                    data.append(copay)
                    data.append('')
                    ins_amount = gross - disc - copay
                    data.append(ins_amount)
                    if inv.dentist:
                        data.append(inv.dentist.name.name)
                    else:
                        data.append('')
                    if inv.dentist.code:
                        data.append(inv.dentist.code)
                    else:
                        data.append('')
                    if inv.dentist.speciality:
                        data.append(inv.dentist.speciality.name)
                    else:
                        data.append('')
                    data.append(inv.patient.patient_id)
                    data.append(inv.patient.qid)
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    tooth = ''
                    for i in line.teeth_code_rel:
                        tooth = tooth + i.name_get()[0][1] + ', '
                    data.append(tooth)
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    complaint = ''
                    for i in inv.appt_id.finding_ids:
                        if i.complaint:
                            complaint += i.complaint + ' '
                    data.append(complaint)
                    data_list.append(data)

        r += 1
        for data in data_list:
            c = 0
            for item in data:
                if c in (2, 9, 12, 19, 39):
                    worksheet.write(r, c, item, normal_left)
                elif c in (14, 15, 16, 17, 18):
                    worksheet.write(r, c, item, normal_right)
                else:
                    worksheet.write(r, c, item, normal)
                c += 1
            r += 1

    @api.multi
    def generate_alkoot_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold = xlwt.easyxf("align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color red;")
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        r = 0
        c = 0

        data_list = []
        output_header = ['', 'INVOICE NO.', 'MEMBER NAME', 'MEMBER ID', 'PreApproval No.',
                         'DATE OF TREATMENT /ADMISSION', 'DATE OF DISCHARGE', 'SYSTEM OF MEDICINE', 'BENEFIT TYPE',
                         'ENCOUNTER TYPE', 'CLINICIAN ID', 'CLINICIAN NAME', 'SYMPTOMS', 'PRINCIPAL ICD CODE',
                         'ICD DESCRIPTION', 'SECONDARY ICD CODE 1', 'SECONDARY ICD CODE 2', 'SECONDARY ICD CODE 3',
                         'SECONDARY ICD CODE 4', 'SECONDARY ICD CODE 5', 'FIRST  INCIDENT DATE', 'FIRST REPORTED DATE',
                         'SERVICE DATE', 'Activity Type', 'INTERNAL  SERVICE CODE', 'SERVICE DESCRIPTION',
                         'CPT CODE', 'AMOUNT CLAIMED (GROSS AMOUNT)', 'QUANTITY', 'Tooth Number (For Dental Only)',
                         'Date of LMP (For Maternity Only)', 'Nature Of Conception(For Maternity Only)',
                         'OBSERVATION', 'Event Reference Number']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 6
            c += 1
        inv_data = self.env['account.invoice'].search \
            ([('date_invoice', '>=', self.from_date), ('date_invoice', '<=', self.to_date),
              ('patient', '!=', False), ('insurance_company', '=', self.company.id),
              ('state', 'in', ('open', 'paid')),
              ('company_id', '=', self.company_id.id)])
        #         data = []
        sl_no = 0
        for inv in inv_data:
            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1

            if inv.appt_id and count:
                sl_no += 1
                apt = inv.appt_id
                for line in inv.invoice_line_ids:
                    data = []
                    data.append(str(sl_no))
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    if inv.insurance_card.insurance_id_no:
                        data.append(inv.insurance_card.insurance_id_no)
                    else:
                        data.append('')
                    if inv.pre_approval_code:
                        data.append(inv.pre_approval_code)
                    else:
                        data.append('')
                    if apt.appointment_sdate:
                        apt_date = datetime.strptime(apt.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                        apt_date = apt_date.strftime('%d/%m/%Y')
                        data.append(apt_date)
                        data.append(apt_date)
                    else:
                        data.append(' ')
                        data.append(' ')
                    # data.append(' ')
                    data.append('Allopathy')
                    if apt.benefit_type:
                        data.append(apt.benefit_type)
                    else:
                        data.append('')
                    data.append('OP No-Emergency')
                    data.append(inv.dentist.code or '')
                    if inv.dentist:
                        data.append(inv.dentist.name.name)
                    else:
                        data.append('')
                    finding = ''
                    for i in inv.appt_id.finding_ids:
                        if i.finding:
                            finding += i.finding + ' '
                    data.append(finding)
                    if line.diagnosis_id:
                        data.append(line.diagnosis_id.code)
                        data.append(line.diagnosis_id.description)
                    else:
                        data.append('')
                        data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    data.append('')
                    if apt.appointment_sdate:
                        apt_date = datetime.strptime(apt.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                        apt_date = apt_date.strftime('%d/%m/%Y')
                        data.append(apt_date)
                    else:
                        data.append(' ')
                    data.append('Activity')
                    data.append(line.product_id.default_code or '')
                    data.append(line.product_id.name or '')
                    data.append('')
                    data.append(line.price_unit)
                    data.append(str(int(line.quantity)))
                    tooth = ''
                    for i in line.teeth_code_rel:
                        tooth = tooth + i.name_get()[0][1] + ', '
                    data.append(tooth)
                    data.append('')
                    data.append('')
                    data.append('OBSERVATION')
                    data.append('')
                    data_list.append(data)

        r += 1
        for data in data_list:
            c = 0
            for item in data:
                if c in (2, 8, 9, 11, 12, 14, 23, 25, 32):
                    worksheet.write(r, c, item, normal_left)
                elif c == 27:
                    worksheet.write(r, c, item, normal_right)
                else:
                    worksheet.write(r, c, item, normal)
                c += 1
            r += 1

    @api.multi
    def generate_axa_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold = xlwt.easyxf("pattern: pattern solid, fore-colour light_green;"
                           "align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color black;")
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        r = 0
        c = 0

        data_list = []
        output_header = ['SERIAL NO.', 'POLICY NO', 'INSURED CODE', 'INSURED NAME', 'GENDER',
                         'DATE OF BIRTH', 'HOSPITAL CODE', 'CLAIM DATE', 'CLAIM FORM NO',
                         'APPROVAL CODE', 'SYMPTOMS', 'DIAGNOSIS-ICD', 'DIAGNOSIS DESCRIPTION',
                         'FIRST INCIDENT DATE', 'FIRST REPORTED DATE', 'MAIN TREATMENT CODE',
                         'SUBCOVER', 'DOCTOR', 'LIC. NO.', 'REFERRAL', 'REFERRAL PROVIDER',
                         'SERVICE DATE', 'SERVICE CODE', 'SERVICE DESCRIPTION', 'GROSS', 'DISCOUNT',
                         'BILL NO.', 'TOOTH NUMBER', 'INPATIENT START DATE', 'INPATIENT END DATE',
                         'CLAIM COMMENTS', 'OPERATION COMMENTS']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 6
            c += 1
        inv_data = self.env['account.invoice'].search \
            ([('date_invoice', '>=', self.from_date), ('date_invoice', '<=', self.to_date),
              ('patient', '!=', False), ('insurance_company', '=', self.company.id),
              ('state', 'in', ('open', 'paid')),
              ('company_id', '=', self.company_id.id)])
        #         data = []
        sl_no = 0
        for inv in inv_data:

            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1
            if inv.appt_id and count:
                sl_no += 1
                apt = inv.appt_id
                for line in inv.invoice_line_ids:
                    data = []
                    data.append(str(sl_no))
                    data.append(inv.insurance_card.number or '')
                    if inv.insurance_card.insurance_id_no:
                        data.append(inv.insurance_card.insurance_id_no)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    if inv.patient.sex:
                        if inv.patient.sex == 'm':
                            data.append('MALE')
                        else:
                            data.append('FEMALE')
                    else:
                        data.append('')
                    if inv.patient.dob:
                        data.append(inv.patient.dob)
                    else:
                        data.append('')
                    data.append('2236')
                    date_inv = ''
                    if inv.date_invoice:
                        date_inv = (datetime.strptime(inv.date_invoice, '%Y-%m-%d'))
                        date_inv = date_inv.strftime('%d/%m/%Y %H:%M:%S').split(' ')[0]
                    data.append(date_inv)
                    if inv.claim_form_num:
                        data.append(inv.claim_form_num)
                    else:
                        data.append('')
                    if inv.pre_approval_code:
                        data.append(inv.pre_approval_code)
                    else:
                        data.append('')
                    finding = ''
                    for i in inv.appt_id.finding_ids:
                        if i.finding:
                            finding += i.finding + ' '
                    data.append(finding)
                    if line.diagnosis_id:
                        data.append(line.diagnosis_id.code)
                        data.append(line.diagnosis_id.description)
                    else:
                        data.append('')
                        data.append('')
                    data.append('')
                    data.append('')
                    data.append('DENTAL')
                    data.append('')
                    if inv.dentist:
                        data.append(inv.dentist.name.name)
                    else:
                        data.append('')
                    if inv.dentist.code:
                        data.append(inv.dentist.code)
                    else:
                        data.append('')
                    data.append('')
                    if apt.referral_dr_id:
                        data.append(apt.referral_dr_id.name)
                    else:
                        data.append('')
                    if apt.appointment_sdate:
                        apt_date = datetime.strptime(apt.appointment_sdate, '%Y-%m-%d %H:%M:%S').date()
                        apt_date = apt_date.strftime('%d/%m/%Y')
                        data.append(apt_date)
                    else:
                        data.append('')
                    data.append(line.product_id.default_code or '')
                    data.append(line.product_id.name or '')
                    gross = line.price_unit * line.quantity
                    if inv.is_special_case:
                        if inv.share_based_on == 'Global':
                            disc = 0
                            copay = 0
                        else:
                            disc = gross - line.after_treatment_grp_disc
                            copay = line.patient_share
                    else:
                        disc = (gross * line.discount_amt) / 100
                        copay = line.price_initial_case_3_copay
                    data.append(gross)
                    data.append(disc)
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    tooth = ''
                    for i in line.teeth_code_rel:
                        tooth = tooth + i.name_get()[0][1] + ', '
                    data.append(tooth)
                    data.append('')
                    data.append('')
                    if copay:
                        copay = str(copay)
                    else:
                        copay = 'NIL'
                    claim = 'APPROVED AMOUNT ' + str(gross - disc) + '/ ' + 'COINSURANCE- ' + copay
                    data.append(claim)
                    data.append('')
                    data_list.append(data)
        r += 1
        for data in data_list:
            c = 0
            for item in data:
                if c in (3, 10, 11, 12, 17, 18, 23, 30):
                    worksheet.write(r, c, item, normal_left)
                elif c in (24, 25, 26):
                    worksheet.write(r, c, item, normal_right)
                else:
                    worksheet.write(r, c, item, normal)
                c += 1
            r += 1

    @api.multi
    def generate_globemed_report(self, workbook):
        worksheet = workbook.add_sheet('Claim Report')
        bold = xlwt.easyxf("pattern: pattern solid, fore-colour grey25;"
                           "align: wrap on, horiz center, vert center;font: bold on;"
                           "borders: left medium, right medium, top medium, bottom medium;"
                           "font: name Verdana, color black;", num_format_str='#,##0.00')
        bold_right = xlwt.easyxf("pattern: pattern solid, fore-colour grey25;"
                                 "align: wrap on, horiz right, vert center;font: bold on;"
                                 "borders: left medium, right medium, top medium, bottom medium;"
                                 "font: name Verdana, color black;", num_format_str='#,##0.00')
        bold_grey = xlwt.easyxf("pattern: pattern solid, fore-colour light_turquoise;"
                                "align: horiz center, vert center;font: bold on;"
                                "borders: top medium, bottom medium;"
                                "font: name Verdana, color black;", num_format_str='#,##0.00')
        normal = xlwt.easyxf("align: horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        normal_left = xlwt.easyxf("align: horiz left, vert center;"
                                  "borders: left thin, right thin, top thin, bottom thin;"
                                  "font: name Verdana;", num_format_str='#,##0.00')
        normal_right = xlwt.easyxf("align: horiz right, vert center;"
                                   "borders: left thin, right thin, top thin, bottom thin;"
                                   "font: name Verdana;", num_format_str='#,##0.00')
        r = 0
        c = 0
        output_header = ['S/N', 'Invoice / Bill Date', 'Invoice No.', 'File No.', 'Insurance Card #', 'Patient Name',
                         'Bill Amount / Gross Amount', 'Discount', 'Excess / Patient Paid', 'Net Claim', 'Doctor No.']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            col = worksheet.col(c)
            col.width = 900 * 6
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 6
            c += 1
        inv_data = self.env['account.invoice'].search \
            ([('date_invoice', '>=', self.from_date), ('date_invoice', '<=', self.to_date),
              ('patient', '!=', False), ('insurance_company', '=', self.company.id),
              ('state', 'in', ('open', 'paid')),
              ('company_id', '=', self.company_id.id)])
        gross_grand = 0
        disc_grand = 0
        coshare_grand = 0
        ins_amt_grand = 0
        no_sub = []
        sub_insurars = self.company.sub_insurar_ids
        for sub in sub_insurars:
            gross_total = 0
            disc_total = 0
            coshare_total = 0
            ins_amt_total = 0
            sl_no = 0
            c = 0
            r += 1
            data = [sub.name, '', '', '', '', '', '', '', '', '', '']
            for dat in data:
                worksheet.write(r, c, dat, bold_grey)
                c += 1
            r += 1
            for inv in inv_data:
                c = 0
                count = 0
                if inv.insurance_invoice:
                    if inv.insurance_invoice.state in ('open', 'paid'):
                        count = 1
                if inv.appt_id and count and sub.id == inv.insurance_card.sub_insurar_id.id:
                    sl_no += 1
                    apt = inv.appt_id
                    data = []
                    data.append(str(sl_no))
                    date_inv = ''
                    if inv.date_invoice:
                        date_inv = datetime.strptime(inv.date_invoice, '%Y-%m-%d')
                        date_inv = date_inv.strftime('%d/%b/%Y')
                    data.append(date_inv)
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    data.append(inv.patient.patient_id)
                    if inv.insurance_card.number:
                        data.append(inv.insurance_card.number)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    gross = 0
                    disc = 0
                    coshare = inv.amount_total
                    for line in inv.invoice_line_ids:
                        gross += line.quantity * line.price_unit
                    if inv.is_special_case:
                        if inv.share_based_on == 'Global':
                            disc = gross - inv.after_treatment_grp_disc
                        else:
                            for line in inv.invoice_line_ids:
                                disc += (line.quantity * line.price_unit) - line.after_treatment_grp_disc
                    else:
                        disc = inv.treatment_group_disc_total
                    ins_amt = gross - disc - coshare
                    data.append(gross)
                    data.append(disc)
                    data.append(coshare)
                    data.append(ins_amt)
                    gross_total += gross
                    disc_total += disc
                    coshare_total += coshare
                    ins_amt_total += ins_amt
                    dr_no = ''
                    for dr in inv.dentist.doctor_insurance_ids:
                        if dr.ins_company_id.id == self.company.id:
                            dr_no = dr.doctor_no
                    data.append(dr_no)
                    for dat in data:
                        if c in (4, 5):
                            worksheet.write(r, c, dat, normal_left)
                        elif c in (6, 7, 8, 9):
                            worksheet.write(r, c, dat, normal_right)
                        else:
                            worksheet.write(r, c, dat, normal)
                        c += 1
            r += 1
            gross_grand += gross_total
            disc_grand += disc_total
            coshare_grand += coshare_total
            ins_amt_grand += ins_amt_total
            data = ['TOTAL:', '', '', '', '', '', gross_total, disc_total, coshare_total, ins_amt_total, '']
            for dat in data:
                if c == 1:
                    worksheet.write(r, c, dat, bold)
                else:
                    worksheet.write(r, c, dat, bold_right)
                c += 1
        c = 0
        r += 1
        data = ['Undefined Subinsurar', '', '', '', '', '', '', '', '', '', '']
        for dat in data:
            worksheet.write(r, c, dat, bold_grey)
            c += 1
        r += 1
        gross_total = 0
        disc_total = 0
        coshare_total = 0
        ins_amt_total = 0
        sl_no = 0
        for inv in inv_data:
            count = 0
            if inv.insurance_invoice:
                if inv.insurance_invoice.state in ('open', 'paid'):
                    count = 1
            if count and inv.insurance_card.sub_insurar_id.id == False:
                no_sub.append(inv)
                if inv.appt_id:
                    sl_no += 1
                    data = []
                    data.append(str(sl_no))
                    date_inv = ''
                    if inv.date_invoice:
                        date_inv = datetime.strptime(inv.date_invoice, '%Y-%m-%d')
                        date_inv = date_inv.strftime('%d/%b/%Y')
                    data.append(date_inv)
                    if inv.insurance_invoice:
                        data.append(inv.insurance_invoice.number)
                    else:
                        data.append('')
                    data.append(inv.patient.patient_id)
                    if inv.insurance_card.number:
                        data.append(inv.insurance_card.number)
                    else:
                        data.append('')
                    data.append(inv.patient.name.name)
                    gross = 0
                    disc = 0
                    coshare = inv.amount_total
                    for line in inv.invoice_line_ids:
                        gross += line.quantity * line.price_unit
                    if inv.is_special_case:
                        if inv.share_based_on == 'Global':
                            disc = gross - inv.after_treatment_grp_disc
                        else:
                            for line in inv.invoice_line_ids:
                                disc += (line.quantity * line.price_unit) - line.after_treatment_grp_disc
                    else:
                        disc = inv.treatment_group_disc_total
                    ins_amt = gross - disc - coshare
                    data.append(gross)
                    data.append(disc)
                    data.append(coshare)
                    data.append(ins_amt)
                    gross_total += gross
                    disc_total += disc
                    coshare_total += coshare
                    ins_amt_total += ins_amt
                    dr_no = ''
                    for dr in inv.dentist.doctor_insurance_ids:
                        if dr.ins_company_id.id == self.company.id:
                            dr_no = dr.doctor_no
                    data.append(dr_no)
                    r += 1
                    c = 0
                    for dat in data:
                        if c in (4, 5):
                            worksheet.write(r, c, dat, normal_left)
                        elif c in (6, 7, 8, 9):
                            worksheet.write(r, c, dat, normal_right)
                        else:
                            worksheet.write(r, c, dat, normal)
                        c += 1
        r += 1
        c = 0
        gross_grand += gross_total
        disc_grand += disc_total
        coshare_grand += coshare_total
        ins_amt_grand += ins_amt_total
        data = ['TOTAL:', '', '', '', '', '', gross_total, disc_total, coshare_total, ins_amt_total, '']
        for dat in data:
            if c == 1:
                worksheet.write(r, c, dat, bold)
            else:
                worksheet.write(r, c, dat, bold_right)
            c += 1
        r += 1
        c = 0
        data = ['TOTAL:', '', '', '', '', '', gross_grand, disc_grand, coshare_grand, ins_amt_grand, '']
        for dat in data:
            if c == 1:
                worksheet.write(r, c, dat, bold)
            else:
                worksheet.write(r, c, dat, bold_right)
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 3
            c += 1
