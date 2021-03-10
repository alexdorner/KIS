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
			print("Error! Wrong value! Please insert your email-address")
			sys.exit




	def set_phone(mobile):
		mobile = frappe.get_doc('Patient ', mobile)
		if not re.match("^[0-9]*$", mobile):
			print
			"Error! Only Numbers allowed!"
			sys.exit()
		elif len(mobile) > 12:
			print
			"Error! Just Austrian phone numbers"
			sys.exit()










