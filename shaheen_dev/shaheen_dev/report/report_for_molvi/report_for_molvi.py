import frappe
from frappe import _
from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no

def execute(filters=None):
    filters = frappe._dict(filters or {})

    columns = [
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": _("Registration Date"), "fieldname": "registration_date", "fieldtype": "Date", "width": 150},
        {"label": _("Student Name"), "fieldname": "student_name", "fieldtype": "Data", "width": 200},
        {"label": _("Masjid Name"), "fieldname": "masjid_name", "fieldtype": "Data", "width": 150},
    ]

    conditions = ["registration_date IS NOT NULL AND registration_date != ''"]

    # Apply date range filter (strictly using From Date and To Date)
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append(f"registration_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'")

    # Filter for status checkboxes
    status_conditions = []
    if filters.get("graduated"):
        status_conditions.append("status = 'Graduated'")
    if filters.get("in_batch"):
        status_conditions.append("status = 'In Batch'")
    if filters.get("waiting"):
        status_conditions.append("status = 'Waiting'")
    if status_conditions:
        conditions.append(f"({' OR '.join(status_conditions)})")

    # Restrict data based on role
    user_roles = frappe.get_roles(frappe.session.user)
    if "Molvi" in user_roles:
        assigned_masjid = frappe.db.get_value(
            "Molvi Registration", {"email": frappe.session.user}, "masjid"
        )
        if assigned_masjid:
            conditions.append(f"masjid_name = '{assigned_masjid}'")
        else:
            conditions.append("1=0")  # No data for unassigned Molvis

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    data = frappe.db.sql(
        f"""
        SELECT
            status,
            registration_date,
            student_name,
            masjid_name
        FROM
            `tabStudent Registration`
        WHERE
            {where_clause}
        ORDER BY registration_date ASC
        """,
        as_dict=True,
    )

    columns, data = add_custom_sl_no(columns, data)
    return columns, data
