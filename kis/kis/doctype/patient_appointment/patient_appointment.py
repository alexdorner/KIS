# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import datetime

from kis.kis.doctype.patient import patient


class PatientAppointment(Document):

	def set_appointment_datetime(self):
		self.appointment_datetime = "%s %s" % (self.appointment_date, self.appointment_time or "00:00:00")

@frappe.whitelist()
def delete_appointment(self):
	today = datetime.date.today()
	appointment = frappe.get_doc('Patient Appointment')
	return appointment

	if self.appointment_date < date.today:

		msg = _('Appointment NOT bookable.')

		frappe.msgprint(msg)


@frappe.whitelist()
def cancel_appointment(appointment_id):
	appointment = frappe.get_doc('Patient Appointment', appointment_id)
	return appointment

	msg = _('Appointment Cancelled.')

	frappe.msgprint(msg)







