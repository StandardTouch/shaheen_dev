frappe.query_reports["Report for molvi"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -7)
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.nowdate()
		},
		{
			fieldname: "graduated",
			label: __("Graduated"),
			fieldtype: "Check"
		},
		{
			fieldname: "in_batch",
			label: __("In Batch"),
			fieldtype: "Check"
		},
		{
			fieldname: "waiting",
			label: __("Waiting"),
			fieldtype: "Check"
		}
	]
};
