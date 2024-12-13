# import frappe
# from frappe import _

# def execute(filters=None):
#     # Ensure filters are initialized
#     filters = frappe._dict(filters or {})

#     # Define columns for the report
#     columns = [
#         {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 150},
#         {"label": _("Registration Date"), "fieldname": "registration_date", "fieldtype": "Date", "width": 150},
#         {"label": _("Student Name"), "fieldname": "student_name", "fieldtype": "Data", "width": 200},
#     ]

#     # Build the query conditions dynamically
#     conditions = []

#     # Handle Date Preset and Registration Date
#     if filters.get("date_preset") == "None":
#         # If "None" is selected, filter by the exact registration date
#         if filters.get("date"):
#             conditions.append(f"registration_date = '{filters.get('date')}'")
#     elif filters.get("date_preset"):
#         # Handle other date presets
#         if filters["date_preset"] == "Past Week":
#             conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")
#         elif filters["date_preset"] == "Past Two Weeks":
#             conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)")
#         elif filters["date_preset"] == "Past Month":
#             conditions.append("registration_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)")
#         elif filters["date_preset"] == "All":
#             pass  # No additional filtering for "All"

#     # Filter for checkboxes
#     status_conditions = []
#     if filters.get("graduated"):
#         status_conditions.append("status = 'Graduated'")
#     if filters.get("in_batch"):
#         status_conditions.append("status = 'In Batch'")
#     if filters.get("waiting"):
#         status_conditions.append("status = 'Waiting'")
    
#     # Combine checkbox filters (OR condition for status)
#     if status_conditions:
#         conditions.append(f"({' OR '.join(status_conditions)})")

#     # Convert conditions into a WHERE clause
#     where_clause = " AND ".join(conditions) if conditions else "1=1"

#     # Fetch data from the database
#     data = frappe.db.sql(
#         f"""
#         SELECT
#             status,
#             registration_date,
#             student_name
#         FROM
#             `tabStudent Registration`
#         WHERE
#             {where_clause}
#         """,
#         as_dict=True,
#     )

#     return columns, data



# import frappe
# from frappe import _


# def execute(filters=None):
#     # Ensure filters are initialized
#     filters = frappe._dict(filters or {})


#     # Determine the column label and date field based on selected statuses
#     date_field_label = "Graduation Date"
#     date_field_name = "graduation_date"  # Default to graduation date


#     # Check selected statuses
#     if filters.get("graduated") and not (filters.get("in_batch") or filters.get("waiting")):
#         date_field_label = _("Graduation Date")
#         date_field_name = "graduation_date"
#     elif filters.get("in_batch") or filters.get("waiting"):
#         date_field_label = _("Registration Date")
#         date_field_name = "student_registration_date"


#     # Define columns dynamically
#     columns = [
#         {"label": _("Status"), "fieldname": "select_jgir", "fieldtype": "Data", "width": 150},
#         {"label": date_field_label, "fieldname": date_field_name, "fieldtype": "Date", "width": 150},
#         {"label": _("Student Name"), "fieldname": "student_name2", "fieldtype": "Data", "width": 200},
#     ]


#     # Build the query conditions dynamically
#     conditions = []


#     # Handle date filters dynamically based on the date_field_name
#     if filters.get("date_preset") == "None":
#         if filters.get("date"):
#             conditions.append(f"{date_field_name} = %(date)s")
#     elif filters.get("date_preset"):
#         if filters["date_preset"] == "Past Week":
#             conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")
#         elif filters["date_preset"] == "Past Two Weeks":
#             conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)")
#         elif filters["date_preset"] == "Past Month":
#             conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)")


#     # Add status filters
#     status_conditions = []
#     if filters.get("graduated"):
#         status_conditions.append("select_jgir = 'Graduated'")
#     if filters.get("in_batch"):
#         status_conditions.append("select_jgir = 'In Batch'")
#     if filters.get("waiting"):
#         status_conditions.append("select_jgir = 'Waiting'")


#     # Combine status conditions
#     if status_conditions:
#         conditions.append(f"({' OR '.join(status_conditions)})")


#     # If no status filters are selected, set a condition that returns no results
#     if not (filters.get("graduated") or filters.get("in_batch") or filters.get("waiting")):
#         conditions.append("1=0")  # This ensures no data is returned


#     # Convert conditions into a WHERE clause
#     where_clause = " AND ".join(conditions) if conditions else "1=1"


#     # Prepare query parameters
#     query_params = {}
#     if filters.get("date_preset") == "None" and filters.get("date"):
#         query_params["date"] = filters.get("date")


#     # Fetch data from the database
#     data = frappe.db.sql(
#         f"""
#         SELECT
#             select_jgir AS select_jgir,
#             {date_field_name} AS {date_field_name},
#             student_name2 AS student_name2
#         FROM
#             `tabStudent Complete Progress`
#         WHERE
#             {where_clause}
#         ORDER BY
#             {date_field_name} DESC
#         """,
#         query_params,
#         as_dict=True,
#     )


#     return columns, data




import frappe
from frappe import _

def execute(filters=None):
    # Initialize filters
    filters = frappe._dict(filters or {})

    # Determine the column label and date field based on selected filters
    date_field_label = _("Graduation Date")
    date_field_name = "graduation_date"  # Default to graduation date

    if filters.get("graduated"):
        # Prioritize "Graduated" filter
        date_field_label = _("Graduation Date")
        date_field_name = "graduation_date"
    elif filters.get("in_batch") or filters.get("waiting"):
        # Switch to registration date for "In Batch" or "Waiting"
        date_field_label = _("Registration Date")
        date_field_name = "student_registration_date"

    # Define columns dynamically
    columns = [
        {"label": _("Status"), "fieldname": "select_jgir", "fieldtype": "Data", "width": 150},
        {"label": date_field_label, "fieldname": date_field_name, "fieldtype": "Date", "width": 150},
        {"label": _("Student Name"), "fieldname": "student_name2", "fieldtype": "Data", "width": 200},
    ]

    # Build query conditions dynamically
    conditions = []

    # Date filters based on the dynamically assigned date field
    if filters.get("date_preset") == "None":
        if filters.get("date"):
            conditions.append(f"{date_field_name} = %(date)s")
    elif filters.get("date_preset"):
        if filters["date_preset"] == "Past Week":
            conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")
        elif filters["date_preset"] == "Past Two Weeks":
            conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)")
        elif filters["date_preset"] == "Past Month":
            conditions.append(f"{date_field_name} >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)")

    # Status filters
    status_conditions = []
    if filters.get("graduated"):
        status_conditions.append("select_jgir = 'Graduated'")
    if filters.get("in_batch"):
        status_conditions.append("select_jgir = 'In Batch'")
    if filters.get("waiting"):
        status_conditions.append("select_jgir = 'Waiting'")

    # Combine status conditions
    if status_conditions:
        conditions.append(f"({' OR '.join(status_conditions)})")

    # If no status filters are selected, ensure no data is fetched
    if not (filters.get("graduated") or filters.get("in_batch") or filters.get("waiting")):
        conditions.append("1=0")

    # Construct WHERE clause
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Prepare query parameters
    query_params = {}
    if filters.get("date_preset") == "None" and filters.get("date"):
        query_params["date"] = filters.get("date")

    # Execute query
    data = frappe.db.sql(
        f"""
        SELECT
            select_jgir AS select_jgir,
            {date_field_name} AS {date_field_name},
            student_name2 AS student_name2
        FROM
            `tabStudent Complete Progress`
        WHERE
            {where_clause}
        ORDER BY
            {date_field_name} DESC
        """,
        query_params,
        as_dict=True,
    )

    return columns, data
