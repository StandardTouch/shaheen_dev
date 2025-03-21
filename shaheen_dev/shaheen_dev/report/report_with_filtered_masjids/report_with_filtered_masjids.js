frappe.query_reports["report with filtered masjids"] = {
	filters: [
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": frappe.datetime.get_today(),
			"on_change": function () {
				populateMasjidDropdown();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"mandatory": 1,
			"default": frappe.datetime.get_today(),
			"on_change": function () {
				populateMasjidDropdown();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "All\nWaiting\nGraduated\nIn Batch",
			"default": "All",
			"on_change": function () {
				populateMasjidDropdown();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname": "filtered_masjid",
			"label": "Filtered Masjid",
			"fieldtype": "Select",
			"options": "All",
			"mandatory": 0,
			"default": "All",
			"on_change": function () {
				frappe.query_report.refresh();
			}
		},
	],
	onload: function (report) {
		populateMasjidDropdown();
	}
};

function populateMasjidDropdown() {
	let filters = frappe.query_report.get_filter_values();
	let masjid_filter = frappe.query_report.get_filter("filtered_masjid");

	let current_selected_masjid = masjid_filter.get_value() || "All";

	frappe.call({
		method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
		args: {
			status: filters.status,
			start_date: filters.start_date,
			end_date: filters.end_date
		},
		callback: function (r) {
			if (r.message) {
				let filteredMasjids = r.message.filter(m => m.label && m.label.trim() !== ""); // ✅ Remove empty Masjids

				let masjid_options = ["All"].concat(filteredMasjids.map(m => m.label));

				masjid_filter.df.options = masjid_options.join("\n");
				masjid_filter.refresh();

				if (masjid_options.includes(current_selected_masjid)) {
					masjid_filter.set_input(current_selected_masjid);
				} else {
					masjid_filter.set_input("All");
				}

				setTimeout(() => {
					let $selectField = $('select[data-fieldname="filtered_masjid"]');
					if ($selectField.length > 0) {
						$selectField.select2({ placeholder: "Search Masjid...", allowClear: true, width: '100%' });
					}
				}, 500);
			}
		}
	});
}
