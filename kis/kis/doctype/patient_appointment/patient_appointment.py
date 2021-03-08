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
	return appointment

	msg = _('Appointment Cancelled.')

	frappe.msgprint(msg)







