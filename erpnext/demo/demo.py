from __future__ import unicode_literals

import frappe, sys
import erpnext
import frappe.utils

from erpnext.demo.setup import KIS, setup_data

"""
Make a demo

1. Start with a fresh account

bench --site demo.erpnext.dev reinstall

2. Install Demo

bench --site demo.erpnext.dev execute erpnext.demo.demo.make

3. If Demo breaks, to continue

bench --site demo.erpnext.dev execute erpnext.demo.demo.simulate

"""

def make(domain='Manufacturing', days=100):
	frappe.flags.domain = domain
	frappe.flags.mute_emails = True
	setup_data.setup(domain)

	if domain == 'KIS':
		KIS.setup_data()

	site = frappe.local.site
	frappe.destroy()
	frappe.init(site)
	frappe.connect()

