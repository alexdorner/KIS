// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient', {
	refresh: function (frm) {


		if (frappe.defaults.get_default('patient_mobile_by') != 'Naming Series') {
			frm.toggle_display('naming_series', false);
		} else {
			erpnext.toggle_naming_series();
		}


		if (!frm.doc.__islocal && frappe.user.has_role('Physician')) {

			frm.add_custom_button(__('Patient Encounter'), function () {
				create_encounter(frm);
			}, 'Create');
			frm.toggle_enable(['customer'], 0);
		}
	},


	let: create_encounter = function (frm) {
		if (!frm.doc.name) {
			frappe.throw(__('Please save the patient first'));
		}
		frappe.route_options = {
			'patient': frm.doc.name,
		};
		frappe.new_doc('Patient Encounter');

	},
})



