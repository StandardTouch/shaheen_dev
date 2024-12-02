import frappe
from frappe import _

def execute(filters=None):
    # Ensure filters are initialized
    filters = frappe._dict(filters or {})

    # Define columns for the report
    columns = [
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": _("Registration Date"), "fieldname": "registration_date", "fieldtype": "Date", "width": 150},
        {"label": _("Student Name"), "fieldname": "student_name", "fieldtype": "Data", "width": 200},
    ]

    # Build the query conditions dynamically
    conditions = []

    # Handle Date Preset and Registration Date
    if filters.get("date_preset") == "None":
        # If "None" is selected, filter by the exact registration date
        if filters.get("date"):
            conditions.append(f"registration_date = '{filters.get('date')}'")
    elif filters.get("date_preset"):
        # Handle other date presets
        if filters["date_preset"] == "Past Week":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")
        elif filters["date_preset"] == "Past Two Weeks":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)")
        elif filters["date_preset"] == "Past Month":
            conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)")
        elif filters["date_preset"] == "All":
            pass  # No additional filtering for "All"

    # Filter for checkboxes
    status_conditions = []
    if filters.get("graduated"):
        status_conditions.append("status = 'Graduated'")
    if filters.get("in_batch"):
        status_conditions.append("status = 'In Batch'")
    if filters.get("waiting"):
        status_conditions.append("status = 'Waiting'")
    
    # Combine checkbox filters (OR condition for status)
    if status_conditions:
        conditions.append(f"({' OR '.join(status_conditions)})")

    # Convert conditions into a WHERE clause
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Fetch data from the database
    data = frappe.db.sql(
        f"""
        SELECT
            status,
            registration_date,
            student_name
        FROM
            `tabStudent Registration`
        WHERE
            {where_clause}
        """,
        as_dict=True,
    )

    return columns, data
