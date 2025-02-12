frappe.query_reports["report with filtered masjids"] = {
	filters: [
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
				// Update the Masjid dropdown dynamically
				populateMasjidDropdown();

				// Refresh the report automatically
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname": "filtered_masjid",
			"label": "Filtered Masjid",
			"fieldtype": "Select",
			"options": "All", // Set default as "All"
			"mandatory": 0,
			"default": "All",
			"on_change": function () {
				// Refresh the report automatically when the Masjid filter changes
				frappe.query_report.refresh();
			}
		}
	],

	onload: function (report) {
		populateMasjidDropdown(); // Populate the dropdown when the report loads

		setTimeout(() => {
			let $selectField = $('select[data-fieldname="filtered_masjid"]');
			if ($selectField.length > 0) {
				// Apply Select2 for better UI
				$selectField.select2({
					placeholder: ".", // Minimal placeholder
					allowClear: true,
					width: '100%'
				});
			}
		}, 500); // Delay to ensure rendering is complete
	}
};

// // Function to populate the Masjid dropdown dynamically
// function populateMasjidDropdown() {
// 	let filters = frappe.query_report.get_filter_values();
// 	frappe.call({
// 		method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
// 		args: {
// 			status: filters.status,
// 			start_date: filters.start_date,
// 			end_date: filters.end_date
// 		},
// 		callback: function (r) {
// 			if (r.message) {
// 				let masjid_filter = frappe.query_report.get_filter("filtered_masjid");
// 				// Add "All" option as the default
// 				masjid_filter.df.options = ["All"].concat(r.message.map(m => m.label)).join("\n");
// 				masjid_filter.refresh();
// 				masjid_filter.set_input("All"); // Set "All" as the default value
// 			}
// 		}
// 	});
// }



// Function to populate the Masjid dropdown dynamically without resetting selection
function populateMasjidDropdown() {
	let filters = frappe.query_report.get_filter_values();
	let masjid_filter = frappe.query_report.get_filter("filtered_masjid");

	// Store the currently selected masjid before updating
	let current_selected_masjid = masjid_filter.get_value();

	frappe.call({
		method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
		args: {
			status: filters.status,
			start_date: filters.start_date,
			end_date: filters.end_date
		},
		callback: function (r) {
			if (r.message) {
				let masjid_options = ["All"].concat(r.message.map(m => m.label));

				// Update options without resetting selection
				masjid_filter.df.options = masjid_options.join("\n");
				masjid_filter.refresh();

				// If the previously selected masjid exists in the new list, restore it
				if (masjid_options.includes(current_selected_masjid)) {
					masjid_filter.set_input(current_selected_masjid);
				} else {
					// Otherwise, keep "All" as the default
					masjid_filter.set_input("All");
				}
			}
		}
	});
}
