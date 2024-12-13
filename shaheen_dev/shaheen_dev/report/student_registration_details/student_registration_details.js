// Copyright (c) 2024, zaid and contributors
// For license information, please see license.txt

frappe.query_reports["Student registration Details"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"mandatory": 1
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"mandatory": 1
		},
		{
			"fieldname": "masjid",
			"label": "Masjid",
			"fieldtype": "Link",
			"options": "Masjid",
			"mandatory": 0
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "All\nWaiting\nGraduated\nIn Batch",
			"mandatory": 0
		}
	]

};
