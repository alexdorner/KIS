# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document



class PatientAppointment(Document):
	pass
#def set_appointment_datetime(self):
#self.appointment_datetime = "%s %s" % (self.appointment_date, self.appointment_time or "00:00:00")




#@frappe.whitelist()
#def cancel_appointment(appointment_id):
#	appointment = frappe.get_doc('Patient Appointment', appointment_id)
#	return appointment

#	msg = _('Appointment Cancelled.')

#	frappe.msgprint(msg)







