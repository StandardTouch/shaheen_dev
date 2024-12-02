frappe.query_reports["Your Report Name"] = {
    filters: [
        {
            fieldname: "date",
            label: __("Registration Date"),
            fieldtype: "Date",
            default: frappe.datetime.nowdate()
        },
        {
            fieldname: "date_preset",
            label: __("Date Preset"),
            fieldtype: "Select",
            options: ["None", "Past Week", "Past Two Weeks", "Past Month", "All"],
            default: "None",
            onchange: function () {
                let preset = frappe.query_report.get_filter_value("date_preset");
                if (preset === "None") {
                    frappe.query_report.toggle_filter_display("date", true); // Show the date filter
                } else {
                    frappe.query_report.toggle_filter_display("date", false); // Hide the date filter
                }
            }
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
