// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('KIS Service Unit', {
	onload: function(frm) {
		frm.list_route = 'Tree/KIS Service Unit';

		// get query select kis service unit
		frm.fields_dict['parent_kis_service_unit'].get_query = function(doc) {
			return{
				filters:[
					['KIS Service Unit', 'is_group', '=', 1],
					['KIS Service Unit', 'name', '!=', doc.kis_service_unit_name]
				]
			};
		};
	},
	refresh: function(frm) {
		frm.trigger('set_root_readonly');
		frm.set_df_property('service_unit_type', 'reqd', 1);
		frm.add_custom_button(__('KIS Service Unit Tree'), function() {
			frappe.set_route('Tree', 'KIS Service Unit');
		});
	},
	set_root_readonly: function(frm) {
		// read-only for root kis service unit
		frm.set_intro('');
		if (!frm.doc.parent_healthcare_service_unit) {
			frm.set_read_only();
			frm.set_intro(__('This is a root kis service unit and cannot be edited.'), true);
		}
	},
	allow_appointments: function(frm) {
		if (!frm.doc.allow_appointments) {
			frm.set_value('overlap_appointments', false);
		}
	},
	is_group: function(frm) {
		if (frm.doc.is_group == 1) {
			frm.set_value('allow_appointments', false);
			frm.set_df_property('service_unit_type', 'reqd', 0);
		}
		else {
			frm.set_df_property('service_unit_type', 'reqd', 1);
		}
	}
});
