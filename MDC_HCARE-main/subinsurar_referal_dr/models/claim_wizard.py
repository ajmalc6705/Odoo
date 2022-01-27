from odoo import models, fields, api
from datetime import datetime
from odoo.tools.misc import xlwt


class ClaimWizard(models.TransientModel):
    _inherit = 'dental.claim.wizard'

    @api.multi
    def generate_allianz_coverletter(self, workbook):
        worksheet = workbook.add_sheet('COVER LETTER')
        bold = xlwt.easyxf("pattern: pattern solid, fore-colour white;"
                           "align: wrap off, horiz left, vert center;font: bold on;"
                           "font: name Verdana, height 230, color black;", num_format_str='#,##0.00')
        bold_title = xlwt.easyxf("pattern: pattern solid, fore-colour white;"
                                  "align: wrap on, horiz center, vert center;font: bold on;"
                                  "borders: left medium, right medium, top medium, bottom medium;"
                                  "font: name Verdana, height 280, color black;", num_format_str='#,##0.00')
        bold_border = xlwt.easyxf("pattern: pattern solid, fore-colour light_green;"
                                  "align: wrap on, horiz center, vert center;font: bold on;"
                                  "borders: left medium, right medium, top medium, bottom medium;"
                                  "font: name Verdana, height 180, color black;", num_format_str='#,##0.00')
        normal = xlwt.easyxf("align: wrap on, horiz center, vert center;"
                             "borders: left thin, right thin, top thin, bottom thin;"
                             "font: name Verdana;", num_format_str='#,##0.00')
        c = 0
        r = 3
        to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
        to_date = to_date.strftime('%B - %Y')
        todayy = fields.Date.context_today(self)
        todayy = datetime.strptime(todayy, '%Y-%m-%d')
        todayy = todayy.strftime('%d-%b-%Y')
        worksheet.write_merge(r, r, c, 4, todayy, bold)
        r += 1
        worksheet.write_merge(r, r, c, 4, 'Ref No.:', bold)
        r += 1
        worksheet.write_merge(r, r, c, 4, 'To, ', bold)
        r += 1
        worksheet.write_merge(r, r, c, 4, 'The Manager', bold)
        r += 1
        worksheet.write_merge(r, r, c, 4, self.company.name, bold)
        r += 1
        if self.company.street or self.company.street2:
            street = self.company.street
            if self.company.street2:
                if street == '':
                    street = self.company.street2
                else:
                    street = street + ', ' + self.company.street2
            worksheet.write_merge(r, r, c, 4, street, bold)
            r += 1

        if self.company.city or self.company.zip:
            zip = self.company.city
            if self.company.zip:
                if zip == '':
                    zip = self.company.zip
                else:
                    zip = zip + ', ' + self.company.zip
            worksheet.write_merge(r, r, c, 4, zip, bold)
            r += 1
        if self.company.phone or self.company.mobile:
            mobile = 'Phone : ' + self.company.phone
            if self.company.zip:
                if mobile == '':
                    mobile = self.company.mobile
                else:
                    mobile = mobile + ', ' + self.company.mobile
            worksheet.write_merge(r, r, c, 4, mobile, bold)
            r += 1
        if self.company.state_id or self.company.country_id:
            state = ''
            if self.company.country_id:
                state = self.company.country_id.name
            if self.company.state_id:
                if state == '':
                    state = self.company.state_id.name
                else:
                    state = state + ', ' + self.company.state_id.name
            worksheet.write_merge(r, r, c, 4, state, bold)
            r += 1

        email = ''
        if self.company.email:
            email = self.company.email
        worksheet.write_merge(r, r + 2, c, 4, 'Email :' + email, bold)
        r += 5
        c = 0
        worksheet.write(r, c, 'Dear Sir,', bold)
        r += 2
        worksheet.write_merge(r, r + 2, c, 8, 'Sub: Medical Bills of ' + self.company.name + ' ' + to_date, bold_title)
        worksheet.row(r).height_mismatch = True
        worksheet.row(r).height = 200 * 2
        r += 4
        output_header = ['SN', 'Policy Holder', 'No of Claims', 'No. of Invoices', 'Net Amount']
        for item in output_header:
            if c in (1, 6):
                worksheet.write_merge(r, r, c, c+2, item, bold_border)
                c += 3
            else:
                worksheet.write(r, c, item, bold_border)
                c += 1
            worksheet.row(r).height_mismatch = True
            worksheet.row(r).height = 200 * 5

        r += 1
        inv_data = self.env['account.invoice'].search([('date_invoice', '>=', self.from_date),
                                                       ('date_invoice', '<=', self.to_date),
                                                       ('patient', '!=', False),
                                                       ('insurance_company', '=', self.company.id),
                                                       ('state', 'in', ('open', 'paid')),
                                                       ('company_id', '=', self.company_id.id)])
        subinsurars = {}
        sum = 0
        claims = 0
        for inv in inv_data:
            amt = 0
            if inv.insurance_invoice and inv.insurance_invoice.state in ('open', 'paid'):
                amt = inv.insurance_invoice.amount_total
            if inv.insurance_card.sub_insurar_id:
                if inv.insurance_card.sub_insurar_id not in list(subinsurars.keys()):
                    subinsurars[inv.insurance_card.sub_insurar_id] = {'invs': [inv],
                                                                      'count': 1,
                                                                      'amt': amt}
                else:
                    amt += subinsurars[inv.insurance_card.sub_insurar_id]['amt']
                    count = subinsurars[inv.insurance_card.sub_insurar_id]['count'] + 1
                    subinsurars[inv.insurance_card.sub_insurar_id] = {'invs': [inv],
                                                                      'count': count,
                                                                      'amt': amt}
            else:
                if 'Undefined' not in list(subinsurars.keys()):
                    subinsurars['Undefined'] = {'invs': [inv],
                                                'count': 1,
                                                'amt': amt}
                else:
                    amount = subinsurars['Undefined']['amt']
                    amt += amount
                    count = subinsurars['Undefined']['count'] + 1
                    subinsurars['Undefined'] = {'invs': [inv],
                                                'count': count,
                                                'amt': amt}
        sl_no = 1
        for sub, value in subinsurars.items():
            c = 0
            if sub != 'Undefined':
                sub = sub.name
            claims += value['count']
            sum += value['amt']
            worksheet.write(r, c, str(int(sl_no)), normal)
            sl_no += 1
            c += 1
            worksheet.write_merge(r, r, c, c+2, sub, normal)
            c += 3
            worksheet.write(r, c, str(int(value['count'])), normal)
            c += 1
            worksheet.write(r, c, str(int(value['count'])), normal)
            c += 1
            worksheet.write_merge(r, r, c, c+2, value['amt'], normal)
            c += 3
            r += 1

        c = 0
        worksheet.write_merge(r, r, c, c+3, 'TOTAL : ', bold_border)
        c += 4
        worksheet.write(r, c, str(int(claims)), bold_border)
        c += 1
        worksheet.write(r, c, str(int(claims)), bold_border)
        c += 1
        worksheet.write_merge(r, r, c, c+2, sum, bold_border)
        c = 0
        r += 2
        worksheet.write(r, c, 'Prepared by:', bold)
        worksheet.write(r, 7, 'Noted By:', bold)
        r += 2
        worksheet.write(r, c, 'Insurance Coordinator', bold)
        worksheet.write(r, 7, 'MANAGEMENT', bold)
        r += 1
        worksheet.write(r, c, self.company_id.name, bold)
        worksheet.write(r, 7, self.company_id.name, bold)
        r += 1
        worksheet.write(r, c, self.company_id.email, bold)
        r += 1
