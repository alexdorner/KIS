# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, getdate, add_days
from frappe import _
from frappe.model.mapper import get_mapped_doc

class PatientEncounter(Document):
	def validate(self):
		self.set_title()

	def on_update(self):
		if self.appointment:
			frappe.db.set_value('Patient Appointment', self.appointment, 'status', 'Closed')
		update_encounter_medical_record(self)

	def after_insert(self):
		insert_encounter_to_medical_record(self)


	def on_cancel(self):
		if self.appointment:
			frappe.db.set_value('Patient Appointment', self.appointment, 'status', 'Open')

		delete_medical_record(self)

	def set_title(self):
		self.title = _('{0} with {1}').format(self.patient_mobile or self.patient,
			self.practitioner_name or self.practitioner)[:100]

@frappe.whitelist()


def insert_encounter_to_medical_record(doc):
	medical_record = frappe.new_doc('Patient Medical Record')
	medical_record.patient = doc.patient
	medical_record.status = 'Open'
	medical_record.communication_date = doc.encounter_date
	medical_record.reference_doctype = 'Patient Encounter'
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)


def update_encounter_medical_record(encounter):
	medical_record_id = frappe.db.exists('Patient Medical Record', {'reference_name': encounter.name})

	if medical_record_id and medical_record_id[0][0]:
		frappe.db.set_value('Patient Medical Record', medical_record_id[0][0])
	else:
		insert_encounter_to_medical_record(encounter)


def delete_medical_record(encounter):
	record = frappe.db.exists('Patient Medical Record', {'reference_name', encounter.name})
	if record:
		frappe.delete_doc('Patient Medical Record', record, force=1)

