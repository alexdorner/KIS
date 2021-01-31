# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import getdate, get_time, flt
from frappe.model.mapper import get_mapped_doc
from frappe import _
import datetime
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from erpnext.hr.doctype.employee.employee import is_holiday
from erpnext.KIS.doctype.healthcare_settings.healthcare_settings import get_receivable_account, get_income_account
from erpnext.KIS.utils import check_fee_validity, get_service_item_and_practitioner_charge, manage_fee_validity

class PatientAppointment(Document):
	def validate(self):
		self.validate_overlaps()
		self.set_appointment_datetime()
		self.validate_customer_created()
		self.set_status()
		self.set_title()

	def after_insert(self):
		self.update_prescription_details()
		#invoice_appointment(self)
		self.update_fee_validity()


	def set_title(self):
		self.title = _('{0} with {1}').format(self.patient_mobile or self.patient,
			self.practitioner_name or self.practitioner)

	def set_status(self):
		today = getdate()
		appointment_date = getdate(self.appointment_date)

		# If appointment is created for today set status as Open else Scheduled
		if appointment_date == today:
			self.status = 'Open'
		elif appointment_date > today:
			self.status = 'Scheduled'

	def validate_overlaps(self):
		end_time = datetime.datetime.combine(getdate(self.appointment_date), get_time(self.appointment_time)) \
			 + datetime.timedelta(minutes=flt(self.duration))

		overlaps = frappe.db.sql("""
		select
			name, practitioner, patient, appointment_time, duration
		from
			`tabPatient Appointment`
		where
			appointment_date=%s and name!=%s and status NOT IN ("Closed", "Cancelled")
			and (practitioner=%s or patient=%s) and
			((appointment_time<%s and appointment_time + INTERVAL duration MINUTE>%s) or
			(appointment_time>%s and appointment_time<%s) or
			(appointment_time=%s))
		""", (self.appointment_date, self.name, self.practitioner, self.patient,
		self.appointment_time, end_time.time(), self.appointment_time, end_time.time(), self.appointment_time))

		if overlaps:
			overlapping_details = _('Appointment overlaps with ')
			overlapping_details += "<b><a href='#Form/Patient Appointment/{0}'>{0}</a></b><br>".format(overlaps[0][0])
			overlapping_details += _('{0} has appointment scheduled with {1} at {2} having {3} minute(s) duration.').format(
				overlaps[0][1], overlaps[0][2], overlaps[0][3], overlaps[0][4])
			frappe.throw(overlapping_details, title=_('Appointments Overlapping'))

	def set_appointment_datetime(self):
		self.appointment_datetime = "%s %s" % (self.appointment_date, self.appointment_time or "00:00:00")

	def validate_customer_created(self):
		if frappe.db.get_single_value('Healthcare Settings', 'automate_appointment_invoicing'):
			if not frappe.db.get_value('Patient', self.patient, 'customer'):
				msg = _("Please set a Customer linked to the Patient")
				msg +=  " <b><a href='#Form/Patient/{0}'>{0}</a></b>".format(self.patient)
				frappe.throw(msg, title=_('Customer Not Found'))

	def update_prescription_details(self):
		if self.procedure_prescription:
			frappe.db.set_value('Procedure Prescription', self.procedure_prescription, 'appointment_booked', 1)
			if self.procedure_template:
				comments = frappe.db.get_value('Procedure Prescription', self.procedure_prescription, 'comments')
				if comments:
					frappe.db.set_value('Patient Appointment', self.name, 'notes', comments)




@frappe.whitelist()


def check_is_new_patient(patient, mobile=None):
	filters = {'patient': patient, 'status': ('!=','Cancelled')}
	if mobile:
		filters['mobile'] = ('!=', mobile)

	has_previous_appointment = frappe.db.exists('Patient Appointment', filters)
	if has_previous_appointment:
		return False
	return True


def get_appointment_item(appointment_doc, item):
	service_item, practitioner_charge = get_service_item_and_practitioner_charge(appointment_doc)
	item.item_code = service_item
	item.description = _('Consulting Charges: {0}').format(appointment_doc.practitioner)
	item.income_account = get_income_account(appointment_doc.practitioner, appointment_doc.company)
	item.cost_center = frappe.get_cached_value('Company', appointment_doc.company, 'cost_center')
	item.rate = practitioner_charge
	item.amount = practitioner_charge
	item.qty = 1
	item.reference_dt = 'Patient Appointment'
	item.reference_dn = appointment_doc.name
	return item


def cancel_appointment(appointment_id):
	appointment = frappe.get_doc('Patient Appointment', appointment_id)


	msg = _('Appointment Cancelled.')


	frappe.msgprint(msg)




@frappe.whitelist()
def get_availability_data(date, practitioner):
	"""
	Get availability data of 'practitioner' on 'date'
	:param date: Date to check in schedule
	:param practitioner: Name of the practitioner
	:return: dict containing a list of available slots, list of appointments and time of appointments
	"""

	date = getdate(date)
	weekday = date.strftime('%A')

	practitioner_doc = frappe.get_doc('KIS Practitioner', practitioner)


	if practitioner_doc.practitioner_schedules:
		slot_details = get_available_slots(practitioner_doc, date)
	else:
		frappe.throw(_('{0} does not have a KIS Practitioner Schedule. Add it in KIS Practitioner master').format(
			practitioner), title=_('Practitioner Schedule Not Found'))


	if not slot_details:
		# TODO: return available slots in nearby dates
		frappe.throw(_('KIS Practitioner not available on {0}').format(weekday), title=_('Not Available'))

	return {'slot_details': slot_details}




def get_available_slots(practitioner_doc, date):
	available_slots = []
	slot_details = []
	weekday = date.strftime('%A')
	practitioner = practitioner_doc.name

	for schedule_entry in practitioner_doc.practitioner_schedules:
		if schedule_entry.schedule:
			practitioner_schedule = frappe.get_doc('Practitioner Schedule', schedule_entry.schedule)
		else:
			frappe.throw(_('{0} does not have a KIS Practitioner Schedule. Add it in KIS Practitioner').format(
				frappe.bold(practitioner)), title=_('Practitioner Schedule Not Found'))

		if practitioner_schedule:
			available_slots = []
			for time_slot in practitioner_schedule.time_slots:
				if weekday == time_slot.day:
					available_slots.append(time_slot)

			if available_slots:
				appointments = []
				# fetch all appointments to practitioner by service unit
				filters = {
					'practitioner': practitioner,
					'service_unit': schedule_entry.service_unit,
					'appointment_date': date,
					'status': ['not in',['Cancelled']]
				}

				if schedule_entry.service_unit:
					slot_name  = schedule_entry.schedule + ' - ' + schedule_entry.service_unit
					allow_overlap = frappe.get_value('KIS Service Unit', schedule_entry.service_unit, 'overlap_appointments')
					if not allow_overlap:
						# fetch all appointments to service unit
						filters.pop('practitioner')
				else:
					slot_name = schedule_entry.schedule
					# fetch all appointments to practitioner without service unit
					filters['practitioner'] = practitioner
					filters.pop('service_unit')

				appointments = frappe.get_all(
					'Patient Appointment',
					filters=filters,
					fields=['name', 'appointment_time', 'duration', 'status'])

				slot_details.append({'slot_name':slot_name, 'service_unit':schedule_entry.service_unit,
					'avail_slot':available_slots, 'appointments': appointments})

	return slot_details


@frappe.whitelist()
def update_status(appointment_id, status):
	frappe.db.set_value('Patient Appointment', appointment_id, 'status', status)
	appointment_booked = True
	if status == 'Cancelled':
		appointment_booked = False
		cancel_appointment(appointment_id)

	procedure_prescription = frappe.db.get_value('Patient Appointment', appointment_id, 'procedure_prescription')
	if procedure_prescription:
		frappe.db.set_value('Procedure Prescription', procedure_prescription, 'appointment_booked', appointment_booked)


@frappe.whitelist()
def make_encounter(source_name, target_doc=None):
	doc = get_mapped_doc('Patient Appointment', source_name, {
		'Patient Appointment': {
			'doctype': 'Patient Encounter',
			'field_map': [
				['appointment', 'name'],
				['patient', 'patient'],
				['practitioner', 'practitioner'],
				['medical_department', 'department'],
				['patient_mobile', 'patient_mobile'],

				['company', 'company']
			]
		}
	}, target_doc)
	return doc


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions('Patient Appointment', filters)

	data = frappe.db.sql("""
		select
		`tabPatient Appointment`.name, `tabPatient Appointment`.patient,
		`tabPatient Appointment`.practitioner, `tabPatient Appointment`.status,
		`tabPatient Appointment`.duration,
		timestamp(`tabPatient Appointment`.appointment_date, `tabPatient Appointment`.appointment_time) as 'start',
		`tabAppointment Type`.color
		from
		`tabPatient Appointment`
		left join `tabAppointment Type` on `tabPatient Appointment`.appointment_type=`tabAppointment Type`.name
		where
		(`tabPatient Appointment`.appointment_date between %(start)s and %(end)s)
		and `tabPatient Appointment`.status != 'Cancelled' and `tabPatient Appointment`.docstatus < 2 {conditions}""".format(conditions=conditions),
		{"start": start, "end": end}, as_dict=True, update={"allDay": 0})

	for item in data:
		item.end = item.start + datetime.timedelta(minutes = item.duration)

	return data




def update_appointment_status():
	# update the status of appointments daily
	appointments = frappe.get_all('Patient Appointment', {
		'status': ('not in', ['Closed', 'Cancelled'])
	}, as_dict=1)

	for appointment in appointments:
		frappe.get_doc('Patient Appointment', appointment.name).set_status()
