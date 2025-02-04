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
    # conditions = []

    # Filter by date
    if filters.get("date_preset") == "None":
        if filters.get("date"):
            conditions.append(f"registration_date = '{filters.get('date')}'")
    elif filters.get("date_preset"):
        if filters["date_preset"] == "Past Week":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")
        elif filters["date_preset"] == "Past Two Weeks":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)")
        elif filters["date_preset"] == "Past Month":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)")
        elif filters["date_preset"] == "All":
            pass

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
        # Fetch the masjid name for the logged-in Molvi from Molvi Registration
        assigned_masjid = frappe.db.get_value(
            "Molvi Registration", {"email": frappe.session.user}, "masjid"
        )
        if assigned_masjid:
            # Use masjid_name for filtering in Student Registration
            conditions.append(f"masjid_name = '{assigned_masjid}'")
        else:
            # If no Masjid assigned, Molvi sees no data
            conditions.append("1=0")
    # Admin can view all data, so no restriction for Admin

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
        """,
        as_dict=True,
    )

    columns, data = add_custom_sl_no(columns, data)
    return columns, data


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

