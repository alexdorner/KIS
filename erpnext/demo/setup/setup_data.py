from __future__ import print_function, unicode_literals

import random, json
import frappe, erpnext
from erpnext.demo.domains import data
from frappe import _

def setup(domain):
	frappe.flags.in_demo = 1
	setup_demo_page()
	setup_user()
	setup_user_roles(domain)




	#setup_customer()

	import_json('Address')
	import_json('Contact')
	import_json('Lead')

	setup_account_to_expense_type()


	frappe.db.commit()
	frappe.clear_cache()


def setup_demo_page():
	# home page should always be "start"
	website_settings = frappe.get_doc("Website Settings", "Website Settings")
	website_settings.home_page = "demo"
	website_settings.save()



def setup_user():
	frappe.db.sql('delete from tabUser where name not in ("Guest", "Administrator")')
	for u in json.loads(open(frappe.get_app_path('erpnext', 'demo', 'data', 'user.json')).read()):
		user = frappe.new_doc("User")
		user.update(u)
		user.flags.no_welcome_mail = True
		user.new_password = 'Demo1234567!!!'
		user.insert()



def setup_user_roles(domain):
	user = frappe.get_doc('User', 'demo@erpnext.com')


	if domain == "KIS":
		user.add_roles('Physician', 'KIS Administrator', 'Patient')





def setup_account():
	frappe.flags.in_import = True
	data = json.loads(open(frappe.get_app_path('erpnext', 'demo', 'data',
		'account.json')).read())
	for d in data:
		doc = frappe.new_doc('Account')
		doc.update(d)
		doc.parent_account = frappe.db.get_value('Account', {'account_name': doc.parent_account})
		doc.insert()

	frappe.flags.in_import = False

def setup_account_to_expense_type():
	company_abbr = frappe.get_cached_value('Company',  erpnext.get_default_company(),  "abbr")
	expense_types = [{'name': _('Calls'), "account": "Sales Expenses - "+ company_abbr},

		{'name': _('Medical'), "account": "Utility Expenses - "+ company_abbr}
]




def import_json(doctype, submit=False, values=None):
	frappe.flags.in_import = True
	data = json.loads(open(frappe.get_app_path('erpnext', 'demo', 'data',
		frappe.scrub(doctype) + '.json')).read())
	for d in data:
		doc = frappe.new_doc(doctype)
		doc.update(d)
		doc.insert()
		if submit:
			doc.submit()

	frappe.db.commit()

	frappe.flags.in_import = False
