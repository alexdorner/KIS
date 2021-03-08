# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class Patient(Document):

	pass

	#def validate(self):
	#	self.set_mobile()


	#def automobile(self):
	#	patient_mobile_by = frappe.db.get_single_value('kis Settings', 'patient_mobile_by')
	#	if patient_mobile_by == 'Patient Mobile':
	#		self.mobile = self.get_patient_mobile()


	#def get_patient_mobile(self):

	#	mobile = self.patient_mobile
	#	if frappe.db.get_value('Patient', mobile):
	#		count = frappe.db.sql("""select ifnull(MAX(CAST(SUBSTRING_INDEX(mobile, ' ', -1) AS UNSIGNED)), 0) from tabPatient
	#			 where mobile like %s""", "%{0} - %".format(mobile), as_list=1)[0][0]
	#		count = cint(count) + 1
	#		return "{0} - {1}".format(mobile, cstr(count))

	#	return mobile



#@frappe.whitelist()
#def get_patient_detail(patient):
#	patient_dict = frappe.db.sql("""select * from tabPatient where mobile=%s""", (patient), as_dict=1)
#	if not patient_dict:
#		frappe.throw(_('Patient not found'))


