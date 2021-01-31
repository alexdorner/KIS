# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import frappe, json
from frappe.utils.make_random import get_random
import datetime
from erpnext.demo.setup.setup_data import import_json
from frappe.utils import getdate

def setup_data():
	frappe.flags.mute_emails = True
	make_masters()
	make_patient()
	make_consulation()
	make_appointment()
	consulation_on_appointment()
	frappe.db.commit()
	frappe.clear_cache()

def make_masters():
	import_json("KIS Practitioner")
	frappe.db.commit()

def make_patient():
	file_path = get_json_path("Patient")
	with open(file_path, "r") as open_file:
		patient_data = json.loads(open_file.read())
		count = 1

		for d in enumerate(patient_data):
			patient = frappe.new_doc("Patient")
			patient.mobile = d[1]['mobile'].title()
			patient.email = d[1]['email']
			patient.ID = d[1]['ID']


def make_appointment():
	i = 1
	while i <= 4:
		practitioner = get_random("KIS Practitioner")
		department = frappe.get_value("KIS Practitioner", practitioner, "department")
		patient = get_random("Patient")
		appointment = frappe.new_doc("Patient Appointment")
		startDate = datetime.datetime.now()
		for x in random_date(startDate,0):
			appointment_datetime = x
		appointment.appointment_datetime = appointment_datetime
		appointment.appointment_time = appointment_datetime
		appointment.appointment_date = appointment_datetime
		appointment.patient = patient

		appointment.practitioner = practitioner
		appointment.department = department
		appointment.save(ignore_permissions = True)
		i += 1

def make_consulation():
	for i in range(3):
		practitioner = get_random("KIS Practitioner")
		department = frappe.get_value("KIS Practitioner", practitioner, "department")
		patient = get_random("Patient")
		patient_ID = frappe.get_value("Patient", patient, "ID")
		encounter = set_encounter(patient, patient_ID, practitioner, department, getdate(), i)
		encounter.save(ignore_permissions=True)

def consulation_on_appointment():
	for i in range(3):
		appointment = get_random("Patient Appointment")
		appointment = frappe.get_doc("Patient Appointment",appointment)
		encounter = set_encounter(appointment.patient, appointment.patient_ID, appointment.practitioner, appointment.department, appointment.appointment_date, i)
		encounter.appointment = appointment.name
		encounter.save(ignore_permissions=True)

def set_encounter(patient, patient_ID, practitioner, department, encounter_date, i):
	encounter = frappe.new_doc("Patient Encounter")
	encounter.patient = patient
	encounter.patient_ID = patient_ID
	encounter.practitioner = practitioner
	encounter.visit_department = department
	encounter.encounter_date = encounter_date

	return encounter




def random_date(start,l):
   current = start
   while l >= 0:
      curr = current + datetime.timedelta(minutes=60)
      yield curr
      l-=1



def get_json_path(doctype):
		return frappe.get_app_path('erpnext', 'demo', 'data', frappe.scrub(doctype) + '.json')
