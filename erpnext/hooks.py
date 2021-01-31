from __future__ import unicode_literals
from frappe import _
from . import __version__ as app_version

app_name = "KIS"
app_title = "KIS"
app_publisher = "BYH"
app_description = ""
app_icon = "fa fa-th"
app_color = "#e74c3c"
app_email = ""
app_license = ""

doc_events = {
	"Patient": {
		"after_insert": "kis.api.make_patient_appointment"
	}
}
