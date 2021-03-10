# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import re #REGULAR EXPRESSION --> library
import sys

from frappe.model.document import Document
import frappe


class Patient(Document):

	def set_email(email):
		email = frappe.get_doc('Patient ', email)
		if not re.match("^[a-z]{@,.}*$", email):
			
			msg = _('Error!!! Please insert your email')

			frappe.msgprint(msg)




	def set_phone(mobile):
		mobile = frappe.get_doc('Patient ', mobile)
		if not re.match("^[0-9]{+}*$", mobile):


			msg = _('Error!!! Please insert a phone number')

			frappe.msgprint(msg)
		elif len(mobile) > 12:


			msg = _('Error!!! Please insert an Austrian phone number ')

			frappe.msgprint(msg)










