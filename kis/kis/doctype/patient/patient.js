// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient',
{
	refresh: function (frm) {


		if (frappe.defaults.get_default('patient_mobile_by') != 'Naming Series') {
			frm.toggle_display('naming_series', false);
		} else {
			kis.toggle_naming_series();
		}



	}



})



