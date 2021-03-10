// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Appointment', {

    setup: function (frm) {
        frm.custom_make_buttons = {
            'Patient': 'Patient'

        };
    },

    onload: function (frm) {
        if (frm.is_new()) {
            frm.set_value('appointment_time', null);
            frm.disable_save();
        }
    }

},

	function show_availability() {
		let ID = '';
		let d = new frappe.ui.Dialog({
			title: __('Available Appointment'),
			fields: [
				{ fieldtype: 'Link', options: 'Medical Department', reqd: 1, fieldname: 'department', label: 'Medical Department'},
				{ fieldtype: 'Column Break'},
				{ fieldtype: 'Link', options: 'Patient', reqd: 1, fieldname: 'ID', label: 'Patient'},
				{ fieldtype: 'Column Break'},
				{ fieldtype: 'Date', reqd: 1, fieldname: 'appointment_date', label: 'Date'},


			],
			primary_action_label: __('Book'),
			primary_action: function() {
				frm.set_value('appointment_time', appointment_time);
				if (!frm.doc.duration) {
					frm.set_value('duration', duration);
				}
				frm.set_value('company', d.get_value('company'));
				frm.set_value('department', d.get_value('department'));
				frm.set_value('appointment_date', d.get_value('appointment_date'));
				if (service_unit) {
					frm.set_value('service_unit', service_unit);
				}
				d.hide();
				frm.enable_save();
				frm.save();
			}
		});

		d.set_values({
			'department': frm.doc.department,
			'patient': frm.doc.patient,
			'appointment_date': frm.doc.appointment_date
		});

});

