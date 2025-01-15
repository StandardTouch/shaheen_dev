// Copyright (c) 2024, zaid and contributors
// For license information, please see license.txt

frappe.query_reports["Student registration Details"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": "Today"
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": "Today"
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
			"mandatory": 0,
			"default": "All"
		}
	]

};



// frappe.query_reports["Student registration Details"] = {
// 	"filters": [
// 		{
// 			"fieldname": "start_date",
// 			"label": "Start Date",
// 			"fieldtype": "Date",
// 			"mandatory": 1,
// 			"default": frappe.datetime.get_today()
// 		},
// 		{
// 			"fieldname": "end_date",
// 			"label": "End Date",
// 			"fieldtype": "Date",
// 			"mandatory": 1,
// 			"default": frappe.datetime.get_today()
// 		},
// 		{
// 			"fieldname": "status",
// 			"label": "Status",
// 			"fieldtype": "Select",
// 			"options": "All\nWaiting\nGraduated\nIn Batch",
// 			"mandatory": 0,
// 			"default": "All",
// 			"on_change": function () {
// 				// Refresh the Masjid filter dynamically when Status changes
// 				frappe.query_report.refresh_filter("masjid");
// 			}
// 		},
// 		{
// 			"fieldname": "masjid",
// 			"label": "Masjid",
// 			"fieldtype": "Link",
// 			"options": "Masjid",
// 			"mandatory": 0,
// 			"get_query": function () {
// 				const status = frappe.query_report.get_filter_value("status");
// 				return {
// 					query: "shaheen_dev.shaheen_dev.report.student_registration_details.student_registration_details.get_masjids_with_status",
// 					filters: JSON.stringify({ status: status || "All" })
// 				};
// 			}
// 		}
// 	]
// };
