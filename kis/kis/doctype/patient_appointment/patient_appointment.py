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

	def booked_appointment(self):
		appointment = frappe.get_doc('Patient Appointment')

		if self.ID == None:
			return appointment
		else:

			msg = _('Appointment NOT bookable.')

			frappe.msgprint(msg)

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

	msg = _('Appointment {0} Cancelled.')

	frappe.msgprint(msg)

@frappe.whitelist()
def get_availability_data(ID,appointment):

	appointment = frappe.get_doc('Patient Appointment', ID)

	if ID.null == 0:
		return appointment
	else:
		return None


def validate_overlaps(self):

	overlaps = frappe.db.sql("""
	select
		appointment, ID, appointment_time, duration
	from
		`tabPatient Appointment`
	where
		appointment_date=%s and Appointment!=%s and ID=%s) and
		(appointment_time=%s))
	""", (self.appointment_date, self.Appointment, self.ID,
		  self.appointment_time))

	if overlaps:
		overlapping_details = _('Appointment overlaps with ')
		overlapping_details += "<b><a href='/app/Form/Patient Appointment/{0}'>{0}</a></b><br>".format(
			overlaps[0][0])
		overlapping_details += _(
			'{0} has appointment scheduled at {2} having {3} minute(s) duration.').format(
			overlaps[0][1], overlaps[0][2], overlaps[0][3], overlaps[0][4])
		frappe.throw(overlapping_details, title=_('Appointments Overlapping'))


