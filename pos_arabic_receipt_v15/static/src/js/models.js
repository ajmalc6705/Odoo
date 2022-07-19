odoo.define("pos_arabic_receipt_v15.models", function (require) {
"use strict";

var models = require('point_of_sale.models');
//console.log("=====models====================>>>>>>>>>>>>>>>.");

models.load_fields('res.company', ['street','street2','city','state_id','vat']);
models.load_fields('product.product',['name','name_arabic']);

})