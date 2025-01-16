// frappe.query_reports["report with filtered masjids"] = {
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
// 			"default": "All",
// 			"on_change": function () {
// 				// Fetch filtered Masjids when the status changes
// 				let filters = frappe.query_report.get_filter_values();
// 				frappe.call({
// 					method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
// 					args: {
// 						status: filters.status,
// 						start_date: filters.start_date,
// 						end_date: filters.end_date
// 					},
// 					callback: function (r) {
// 						if (r.message) {
// 							let masjid_filter = frappe.query_report.get_filter("filtered_masjid");
// 							masjid_filter.df.options = r.message;
// 							masjid_filter.refresh();
// 							masjid_filter.set_input("");
// 						}
// 					}
// 				});
// 			}
// 		},
// 		{
// 			"fieldname": "filtered_masjid",
// 			"label": "Filtered Masjid",
// 			"fieldtype": "Select",
// 			"options": [],
// 			"mandatory": 0
// 		}
// 	]
// };




// frappe.query_reports["report with filtered masjids"] = {
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
// 			"default": "All",
// 			"on_change": function () {
// 				// Fetch filtered Masjids when the status changes
// 				let filters = frappe.query_report.get_filter_values();
// 				frappe.call({
// 					method: "shaheen_dev.shaheen_dev.report.report_with_filtered_masjids.report_with_filtered_masjids.get_filtered_masjids",
// 					args: {
// 						status: filters.status,
// 						start_date: filters.start_date,
// 						end_date: filters.end_date
// 					},
// 					callback: function (r) {
// 						if (r.message) {
// 							let masjid_filter = frappe.query_report.get_filter("filtered_masjid");
// 							masjid_filter.df.options = r.message;
// 							masjid_filter.refresh();
// 							masjid_filter.set_input("");

// 							// Refresh the report to apply changes
// 							frappe.query_report.refresh();
// 						}
// 					}
// 				});
// 			}
// 		},
// 		{
// 			"fieldname": "filtered_masjid",
// 			"label": "Filtered Masjid",
// 			"fieldtype": "Select",
// 			"options": [],
// 			"mandatory": 0
// 		}
// 	]
// };







//////////////////////////////////////below code is for the searchable dropdown/////////////////////////////////////////////////






// frappe.query_reports["report with filtered masjids"] = {
// 	filters: [
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
// 			"default": "All",
// 			"on_change": function () {
// 				populateMasjidDropdown(); // Populate dropdown dynamically
// 			}
// 		},
// 		{
// 			"fieldname": "filtered_masjid",
// 			"label": "Filtered Masjid",
// 			"fieldtype": "Select",
// 			"options": [],
// 			"mandatory": 0
// 		}
// 	],

// 	onload: function (report) {
// 		populateMasjidDropdown(); // Populate the dropdown on load

// 		setTimeout(() => {
// 			let $selectField = $('select[data-fieldname="filtered_masjid"]');

// 			if ($selectField.length > 0) {
// 				console.log("Applying Select2 to filtered_masjid...");

// 				// Remove default ERPNext placeholder and empty options
// 				$selectField.find("option[value=''], option:empty").remove();

// 				// Ensure the field has no conflicting placeholder attributes
// 				$selectField.removeAttr("placeholder");

// 				// Apply Select2
// 				$selectField.select2({
// 					placeholder: "Search Masjid...", // Custom placeholder for Select2
// 					allowClear: true, // Allow clearing the selection
// 					width: '100%' // Ensure dropdown fits ERPNext layout
// 				});

// 				// Dynamically adjust the placeholder style
// 				$('.select2-selection__placeholder').css({
// 					color: '#8d99a6', // Placeholder color similar to ERPNext
// 					fontStyle: 'normal' // Placeholder font style
// 				});
// 			}
// 		}, 500); // Delay ensures rendering is complete
// 	}
// };

// // Function to populate dropdown dynamically
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
// 				masjid_filter.df.options = r.message.map(m => m.label).join("\n");
// 				masjid_filter.refresh();
// 				masjid_filter.set_input("");
// 			}
// 		}
// 	});
// }



///////////////////////////////////////////////////////////////////////////////////////////////////////

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
				populateMasjidDropdown(); // Populate dropdown dynamically
			}
		},
		{
			"fieldname": "filtered_masjid",
			"label": "Filtered Masjid",
			"fieldtype": "Select",
			"options": [], // Options will be dynamically populated
			"mandatory": 0
		}
	],

	onload: function (report) {
		populateMasjidDropdown(); // Populate the Masjid dropdown on report load
	}
};

// Function to populate the Masjid dropdown dynamically
function populateMasjidDropdown() {
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
				masjid_filter.df.options = r.message.map(m => m.label).join("\n");
				masjid_filter.refresh();
				masjid_filter.set_input("");
			}
		}
	});
}
