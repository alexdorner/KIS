# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import getdate, get_time, flt
from frappe.model.mapper import get_mapped_doc
from frappe import _
import datetime

class PatientAppointment(Document):

	def set_appointment_datetime(self):
		self.appointment_datetime = "%s %s" % (self.appointment_date, self.appointment_time or "00:00:00")




@frappe.whitelist()
def cancel_appointment(appointment_id):
	appointment = frappe.get_doc('Patient Appointment', appointment_id)


	msg = _('Appointment Cancelled.')


	frappe.msgprint(msg)


@frappe.whitelist()
def make_encounter(source_name, target_doc=None):
	doc = get_mapped_doc('Patient Appointment', source_name, {
		'Patient Appointment': {
			'doctype': 'Patient Encounter',
			'field_map': [
				['appointment', 'name'],
				['patient', 'patient'],
				['practitioner', 'practitioner'],
				['medical_department', 'department'],
				['patient_mobile', 'patient_mobile'],

				['company', 'company']
			]
		}
	}, target_doc)
	return doc





