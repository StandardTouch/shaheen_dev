# import frappe
# from frappe.utils import getdate
# from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no  # Import the utility function


# def execute(filters=None):
#     """
#     Main function to fetch and display the report data.
#     """
#     # Define the columns for the report
#     columns = [
#         {"fieldname": "student_name", "label": "Student Name", "fieldtype": "Data", "width": 200},
#         {"fieldname": "fathers_name", "label": "Fathers Name", "fieldtype": "Data", "width": 200},
#         {"fieldname": "contact_number", "label": "Contact Number", "fieldtype": "Data", "width": 150},
#         {"fieldname": "registrar_name", "label": "Registrar Name", "fieldtype": "Data", "width": 150},
#         {"fieldname": "address", "label": "Address", "fieldtype": "Data", "width": 150},
#         {"fieldname": "area", "label": "Area", "fieldtype": "Data", "width": 150},
#         {"fieldname": "pincode", "label": "Pincode", "fieldtype": "Data", "width": 100},
#         {"fieldname": "masjid_name", "label": "Masjid Name", "fieldtype": "Data", "width": 200},
#         {"fieldname": "cluster_no", "label": "Cluster No", "fieldtype": "Data", "width": 100},
#         {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
#         {"fieldname": "registration_date", "label": "Registration Date", "fieldtype": "Date", "width": 120},
#     ]

#     # Add the "Last Topic" column for "All" and "In Batch" statuses
#     if filters and filters.get("status") in ["In Batch", "All"]:
#         columns.append({"fieldname": "last_topic_label", "label": "Last Topic", "fieldtype": "Data", "width": 150})

#     # If filters are not set or incomplete, return columns and empty data
#     if not filters or not filters.get("start_date") or not filters.get("end_date"):
#         return columns, []

#     # Fetch filtered data
#     data = get_filtered_data(filters)
#     columns, data = add_custom_sl_no(columns, data)
#     return columns, data


# def get_filtered_data(filters):
#     """
#     Fetches filtered data based on the provided filters.
#     """
#     conditions = []

#     # Apply date range filter
#     if filters.get("start_date") and filters.get("end_date"):
#         start_date = getdate(filters.get("start_date"))
#         end_date = getdate(filters.get("end_date"))
#         conditions.append(f"(registration_date BETWEEN '{start_date}' AND '{end_date}')")

#     # Apply filtered Masjid filter if provided
#     if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
#         conditions.append(f"masjid_name = '{filters.get('filtered_masjid')}'")

#     # Apply status filter
#     if filters.get("status") and filters.get("status") != "All":
#         conditions.append(f"status = '{filters.get('status')}'")

#     # If no conditions are specified, allow all data
#     condition_string = " AND ".join(conditions) if conditions else "1=1"

#     query = f"""
#         SELECT
#             student_name,
#             fathers_name,
#             contact_number,
#             registrar_name,
#             address,
#             area,
#             pincode,
#             masjid_name,
#             cluster_no,
#             status,
#             registration_date
#         FROM
#             `tabStudent Registration`
#         WHERE
#             {condition_string}
#         ORDER BY
#             registration_date ASC
#     """

#     # Fetch student data
#     student_data = frappe.db.sql(query, as_dict=True)

#     # Add "last_topic_label" for students in "In Batch" status or when "All" is selected
#     if filters.get("status") in ["In Batch", "All"]:
#         # Fetch data from "Student Complete Progress"
#         progress_data = frappe.db.sql("""
#             SELECT
#                 student_name2,
#                 last_topic_label
#             FROM
#                 `tabStudent Complete Progress`
#         """, as_dict=True)

#         # Create a lookup dictionary for last_topic_label
#         progress_lookup = {row["student_name2"]: row["last_topic_label"] for row in progress_data}

#         # Add last_topic_label to the student data
#         for row in student_data:
#             row["last_topic_label"] = progress_lookup.get(row["student_name"], "")

#     return student_data


# @frappe.whitelist()
# def get_filtered_masjids(status=None, start_date=None, end_date=None):
#     """
#     Returns a list of Masjids filtered by the provided status and date range.
#     """
#     conditions = ["masjid_name IS NOT NULL"]

#     # Add status condition if provided
#     if status and status != "All":
#         conditions.append(f"status = '{status}'")

#     # Add date range condition if provided
#     if start_date and end_date:
#         conditions.append(f"registration_date BETWEEN '{start_date}' AND '{end_date}'")

#     condition_string = " AND ".join(conditions)

#     query = f"""
#         SELECT DISTINCT
#             masjid_name
#         FROM
#             `tabStudent Registration`
#         WHERE
#             {condition_string}
#     """

#     masjids = frappe.db.sql(query, as_dict=False)

#     return [{"label": m[0], "value": m[0]} for m in masjids if m[0]]


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import frappe
from frappe.utils import getdate
from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no  # Import the utility function

def execute(filters=None):
    """
    Main function to fetch and display the report data.
    """
    columns = [
        {"fieldname": "student_name", "label": "Student Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "fathers_name", "label": "Fathers Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "contact_number", "label": "Contact Number", "fieldtype": "Data", "width": 150},
        {"fieldname": "registrar_name", "label": "Registrar Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "address", "label": "Address", "fieldtype": "Data", "width": 150},
        {"fieldname": "area", "label": "Area", "fieldtype": "Data", "width": 150},
        {"fieldname": "pincode", "label": "Pincode", "fieldtype": "Data", "width": 100},
        {"fieldname": "masjid_name", "label": "Masjid Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "cluster_no", "label": "Cluster No", "fieldtype": "Data", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
        {"fieldname": "registration_date", "label": "Registration Date", "fieldtype": "Date", "width": 120},
    ]

    # Add "Graduation Date" column if status = "Graduated"
    if filters and filters.get("status") == "Graduated":
        columns.append({"fieldname": "graduation_date", "label": "Graduation Date", "fieldtype": "Date", "width": 120})

    # Add "Last Topic" column for "In Batch" and "All" statuses
    if filters and filters.get("status") in ["In Batch", "All"]:
        columns.append({"fieldname": "last_topic_label", "label": "Last Topic", "fieldtype": "Data", "width": 150})

    if not filters or not filters.get("start_date") or not filters.get("end_date"):
        return columns, []

    data = get_filtered_data(filters)
    columns, data = add_custom_sl_no(columns, data)
    return columns, data

def get_filtered_data(filters):
    conditions = []
    join_progress = False

    if filters.get("status") == "Graduated":
        join_progress = True
        if filters.get("start_date") and filters.get("end_date"):
            start_date = getdate(filters.get("start_date"))
            end_date = getdate(filters.get("end_date"))
            conditions.append(f"(scp.graduation_date BETWEEN '{start_date}' AND '{end_date}')")
    else:
        if filters.get("start_date") and filters.get("end_date"):
            start_date = getdate(filters.get("start_date"))
            end_date = getdate(filters.get("end_date"))
            conditions.append(f"(sr.registration_date BETWEEN '{start_date}' AND '{end_date}')")

    if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
        conditions.append(f"sr.masjid_name = '{filters.get('filtered_masjid')}'")

    if filters.get("status") and filters.get("status") != "All":
        conditions.append(f"sr.status = '{filters.get('status')}'")

    condition_string = " AND ".join(conditions) if conditions else "1=1"

    if join_progress:
        query = f"""
            SELECT
                sr.student_name,
                sr.fathers_name,
                sr.contact_number,
                sr.registrar_name,
                sr.address,
                sr.area,
                sr.pincode,
                sr.masjid_name,
                sr.cluster_no,
                sr.status,
                sr.registration_date,
                scp.graduation_date
            FROM
                `tabStudent Registration` sr
            LEFT JOIN
                `tabStudent Complete Progress` scp
            ON
                sr.student_name = scp.student_name2
            WHERE
                {condition_string}
            ORDER BY
                scp.graduation_date ASC
        """
    else:
        query = f"""
            SELECT
                sr.student_name,
                sr.fathers_name,
                sr.contact_number,
                sr.registrar_name,
                sr.address,
                sr.area,
                sr.pincode,
                sr.masjid_name,
                sr.cluster_no,
                sr.status,
                sr.registration_date
            FROM
                `tabStudent Registration` sr
            WHERE
                {condition_string}
            ORDER BY
                sr.registration_date ASC
        """

    student_data = frappe.db.sql(query, as_dict=True)

    if filters.get("status") in ["In Batch", "All"]:
        progress_data = frappe.db.sql("""
            SELECT
                student_name2,
                last_topic_label
            FROM
                `tabStudent Complete Progress`
        """, as_dict=True)

        progress_lookup = {row["student_name2"]: row["last_topic_label"] for row in progress_data}

        for row in student_data:
            row["last_topic_label"] = progress_lookup.get(row["student_name"], "")

    return student_data

@frappe.whitelist()
def get_filtered_masjids(status=None, start_date=None, end_date=None):
    """
    Returns a list of Masjids filtered by the provided status and date range.
    """
    conditions = ["masjid_name IS NOT NULL"]

    if status and status != "All":
        conditions.append(f"status = '{status}'")

    if start_date and end_date:
        conditions.append(f"registration_date BETWEEN '{start_date}' AND '{end_date}'")

    condition_string = " AND ".join(conditions)

    query = f"""
        SELECT DISTINCT
            masjid_name
        FROM
            `tabStudent Registration`
        WHERE
            {condition_string}
    """

    masjids = frappe.db.sql(query, as_dict=False)

    # ✅ Corrected the return statement
    return [{"label": m[0], "value": m[0]} for m in masjids if m[0]]
