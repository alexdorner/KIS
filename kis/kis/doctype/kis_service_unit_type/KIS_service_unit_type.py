# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.rename_doc import rename_doc

class KISServiceUnitType(Document):
	def validate(self):
		if self.allow_appointments:
			frappe.msgprint(
				_('kis Service Unit Type cannot have both {0} and {1}').format(
					frappe.bold('Allow Appointments'), frappe.bold('Inpatient Occupancy')),
				raise_exception=1, title=_('Validation Error'), indicator='red'
			)
		elif not self.allow_appointments:
			frappe.msgprint(
				_('kis Service Unit Type must allow atleast one among {0} and {1}').format(
					frappe.bold('Allow Appointments'), frappe.bold('Inpatient Occupancy')),
				raise_exception=1, title=_('Validation Error'), indicator='red'
			)

		if not self.allow_appointments:
			self.overlap_appointments = 0




