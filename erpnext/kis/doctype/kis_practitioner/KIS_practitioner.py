# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from erpnext.accounts.party import validate_party_accounts
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from frappe.model.naming import append_number_if_name_exists
from frappe.desk.reportview import build_match_conditions, get_filters_cond

class HealthcarePractitioner(Document):
	def onload(self):
		load_address_and_contact(self)

	def autoname(self):
		# concat first and last name
		self.name = self.practitioner_name

		if frappe.db.exists('KIS Practitioner', self.name):
			self.name = append_number_if_name_exists('Contact', self.name)

	def validate(self):
		self.set_full_name()
		validate_party_accounts(self)
		i
		if self.user_id:
			self.validate_user_id()
		else:
			existing_user_id = frappe.db.get_value('KIS Practitioner', self.name, 'user_id')
			if existing_user_id:
				frappe.permissions.remove_user_permission(
					'KIS Practitioner', self.name, existing_user_id)

	def on_update(self):
		if self.user_id:
			frappe.permissions.add_user_permission('KIS Practitioner', self.name, self.user_id)

	def set_full_name(self):
		if self.last_name:
			self.practitioner_name = ' '.join(filter(None, [self.first_name, self.last_name]))
		else:
			self.practitioner_name = self.first_name

	def validate_user_id(self):
		if not frappe.db.exists('User', self.user_id):
			frappe.throw(_('User {0} does not exist').format(self.user_id))
		elif not frappe.db.exists('User', self.user_id, 'enabled'):
			frappe.throw(_('User {0} is disabled').format(self.user_id))

		# check duplicate
		practitioner = frappe.db.exists('KIS Practitioner', {
			'user_id': self.user_id,
			'name': ('!=', self.name)
		})
		if practitioner:
			frappe.throw(_('User {0} is already assigned to KIS Practitioner {1}').format(
				self.user_id, practitioner))

	def on_trash(self):
		delete_contact_and_address('KIS Practitioner', self.name)



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_practitioner_list(doctype, txt, searchfield, start, page_len, filters=None):
	fields = ['name', 'practitioner_name', 'mobile_phone']

	filters = {
		'name': ('like', '%%%s%%' % txt)
	}

	return frappe.get_all('KIS Practitioner', fields = fields,
		filters = filters, start=start, page_length=page_len, order_by='name, practitioner_name', as_list=1)
