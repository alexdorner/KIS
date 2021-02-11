# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest
import frappe
from kis.KIS.doctype.patient_appointment.test_patient_appointment import create_patient

class TestPatient(unittest.TestCase):
	def test_customer_created(self):
		frappe.db.sql("""delete from `tabPatient`""")
		frappe.db.set_value('kis Settings', None, 'link_customer_to_patient', 1)
		patient = create_patient()
		self.assertTrue(frappe.db.get_value('Patient', patient, 'customer'))

	def test_patient_registration(self):
		frappe.db.sql("""delete from `tabPatient`""")
		settings = frappe.get_single('kis Settings')
		settings.save()

		patient = create_patient()
		patient = frappe.get_doc('Patient', patient)


