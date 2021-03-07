# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, cstr, getdate

class Patient(Document):
	def validate(self):
		self.set_mobile()


	#def before_insert(self):
		#self.set_missing_customer_details()

	def after_insert(self):
		#self.add_as_website_user()
		self.reload()
		if frappe.db.get_single_value('kis Settings', 'link_customer_to_patient') and not self.customer:
			create_customer(self)
		if frappe.db.get_single_value('kis Settings', 'collect_registration_fee'):
			frappe.db.set_value('Patient', self.mobile)

		self.reload() # self.notify_update()

	def on_update(self):
		if self.customer:
			customer = frappe.get_doc('Customer', self.customer)
			if self.customer_group:
				customer.customer_group = self.customer_group
			if self.territory:
				customer.territory = self.territory

			customer.customer_mobile = self.patient_mobile

			customer.ignore_mandatory = True
			customer.save(ignore_permissions=True)
		else:
			if frappe.db.get_single_value('kis Settings', 'link_customer_to_patient'):
				create_customer(self)



	def automobile(self):
		patient_mobile_by = frappe.db.get_single_value('kis Settings', 'patient_mobile_by')
		if patient_mobile_by == 'Patient Mobile':
			self.mobile = self.get_patient_mobile()
		#else:
		#	set_name_by_naming_series(self) #es wird trotzdem die nummer gesettet aber der import heißt halt name im framework ...

	def get_patient_mobile(self):

		mobile = self.patient_mobile
		if frappe.db.get_value('Patient', mobile):
			count = frappe.db.sql("""select ifnull(MAX(CAST(SUBSTRING_INDEX(mobile, ' ', -1) AS UNSIGNED)), 0) from tabPatient
				 where mobile like %s""", "%{0} - %".format(mobile), as_list=1)[0][0]
			count = cint(count) + 1
			return "{0} - {1}".format(mobile, cstr(count))

		return mobile




def create_customer(doc):
	customer = frappe.get_doc({
		'doctype': 'Customer',
		'customer_mobile': doc.patient_mobile,
		'customer_group': doc.customer_group or frappe.db.get_single_value('Selling Settings', 'customer_group'),
		'territory' : doc.territory or frappe.db.get_single_value('Selling Settings', 'territory'),
		'customer_type': 'Individual',
		'default_currency': doc.default_currency,
		'default_price_list': doc.default_price_list,
		'language': doc.language
	}).insert(ignore_permissions=True, ignore_mandatory=True)

	frappe.db.set_value('Patient', doc.mobile, 'customer', customer.mobile)
	frappe.msgprint(_('Customer {0} is created.').format(customer.mobile), alert=True)


@frappe.whitelist()
def get_patient_detail(patient):
	patient_dict = frappe.db.sql("""select * from tabPatient where mobile=%s""", (patient), as_dict=1)
	if not patient_dict:
		frappe.throw(_('Patient not found'))


