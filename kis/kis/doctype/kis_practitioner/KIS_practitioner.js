// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('KIS Practitioner', {
	setup: function(frm) {
		frm.set_query('account', 'accounts', function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					'root_type': 'Income',
					'company': d.company,
					'is_group': 0
				}
			};
		});
	},
	refresh: function(frm) {
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'KIS Practitioner'};

		if (!frm.is_new()) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}

		frm.set_query('service_unit', 'practitioner_schedules', function(){
			return {
				filters: {
					'is_group': false,
					'allow_appointments': true
				}
			};
		});


	}
});



frappe.ui.form.on('KIS Practitioner', 'user_id',function(frm) {
	if (frm.doc.user_id) {
		frappe.call({
			'method': 'frappe.client.get',
			args: {
				doctype: 'User',
				name: frm.doc.user_id
			},
			callback: function (data) {



				if (!frm.doc.first_name || frm.doc.first_name != data.message.first_name)
					frappe.model.set_value(frm.doctype,frm.docname, 'first_name', data.message.first_name);

				if (!frm.doc.last_name || frm.doc.last_name != data.message.last_name)
					frappe.model.set_value(frm.doctype,frm.docname, 'last_name', data.message.last_name);
				if (!frm.doc.mobile_phone || frm.doc.mobile_phone != data.message.mobile_no)
					frappe.model.set_value(frm.doctype,frm.docname, 'mobile_phone', data.message.mobile_no);
			}
		});
	}
});

frappe.tour['KIS Practitioner'] = [

	{
		fieldname: 'practitioner_schedules',
		title: __('Practitioner Schedules'),
		description: __('Set the Practitioner Schedule you just created. This will be used while booking appointments.')
	}

];

