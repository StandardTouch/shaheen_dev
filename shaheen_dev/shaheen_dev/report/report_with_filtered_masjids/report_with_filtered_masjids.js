frappe.query_reports["report with filtered masjids"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "All\nWaiting\nGraduated\nIn Batch",
			"default": "All",
			"on_change": function () {
				// Fetch filtered Masjids when the status changes
				let filters = frappe.query_report.get_filter_values();
				frappe.call({
					method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
					args: {
						status: filters.status,
						start_date: filters.start_date,
						end_date: filters.end_date
					},
					callback: function (r) {
						if (r.message) {
							let masjid_filter = frappe.query_report.get_filter("filtered_masjid");
							masjid_filter.df.options = r.message;
							masjid_filter.refresh();
							masjid_filter.set_input("");
						}
					}
				});
			}
		},
		{
			"fieldname": "filtered_masjid",
			"label": "Filtered Masjid",
			"fieldtype": "Select",
			"options": [],
			"mandatory": 0
		}
	]
};
