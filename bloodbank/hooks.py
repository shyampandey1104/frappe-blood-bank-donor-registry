# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "bloodbank"
app_title = "Frappe Blood Bank Donor Registry"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Blood Bank Donor Registry for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/bloodbank/css/bloodbank.bundle.css"
app_include_js = "/assets/bloodbank/js/bloodbank.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "bloodbank.engine.on_document_submit",
        "on_cancel": "bloodbank.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "bloodbank.engine.daily_scheduled_sync"
    ]
}
