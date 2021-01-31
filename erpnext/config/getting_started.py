from __future__ import unicode_literals
import frappe
from frappe import _

active_domains = frappe.get_active_domains()

def get_data():
	return [
		{

		{
			"label": _("Data Import and Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Data Import",
					"label": _("Import Data"),
					"icon": "octicon octicon-cloud-upload",
					"description": _("Import Data from CSV / Excel files."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Chart of Accounts Importer",
					"label": _("Chart of Accounts Importer"),
					"description": _("Import Chart of Accounts from CSV / Excel files"),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "Letter Head",
					"description": _("Letter Heads for print templates."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Email Account",
					"description": _("Add / Manage Email Accounts."),
					"onboard": 1,
				},

			]
		},

		{
			"label": _("KIS"),
			"condition": "KIS" in active_domains,
			"items": [
				{
					"type": "doctype",
					"name": "Patient",
					"label": _("Patient"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Physician",
					"label": _("Physician"),
					"onboard": 1,
				}
			]
		}
		}

	]
