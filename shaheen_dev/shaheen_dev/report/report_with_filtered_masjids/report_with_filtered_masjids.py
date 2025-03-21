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
#working code with graduate filter
# import frappe
# from frappe.utils import getdate
# from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no  # Import the utility function


# @frappe.whitelist()
# def get_filtered_masjids(status=None, start_date=None, end_date=None):
#     """
#     Returns a list of Masjids filtered by the provided status and date range.
#     """
#     frappe.logger().info(f"Fetching Masjids for status: {status}, start_date: {start_date}, end_date: {end_date}")

#     conditions = ["sr.masjid_name IS NOT NULL", "sr.masjid_name != ''"]  # ✅ Exclude empty Masjid names

#     if status and status != "All":
#         conditions.append(f"sr.status = '{status}'")

#     if start_date and end_date:
#         if status == "Graduated":
#             conditions.append(f"scp.graduation_date BETWEEN '{start_date}' AND '{end_date}'")
#         else:
#             conditions.append(f"sr.registration_date BETWEEN '{start_date}' AND '{end_date}'")

#     condition_string = " AND ".join(conditions)

#     if status == "Graduated":
#         query = f"""
#             SELECT DISTINCT sr.masjid_name
#             FROM `tabStudent Registration` sr
#             LEFT JOIN `tabStudent Complete Progress` scp
#             ON sr.student_name = scp.student_name2
#             WHERE {condition_string}
#         """
#     else:
#         query = f"""
#             SELECT DISTINCT sr.masjid_name
#             FROM `tabStudent Registration` sr
#             WHERE {condition_string}
#         """

#     masjids = frappe.db.sql(query, as_dict=False)
#     frappe.logger().info(f"Masjids Retrieved: {masjids}")

#     # ✅ Remove empty Masjids before returning the list
#     return [{"label": m[0], "value": m[0]} for m in masjids if m[0] and m[0].strip() != ""]


# def execute(filters=None):
#     """
#     Main function to fetch and display the report data.
#     """
#     columns = [
#         {"fieldname": "sl_no", "label": "Sl No", "fieldtype": "Int", "width": 50},  # ✅ Ensure SL No column exists
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

#     if filters and filters.get("status") == "Graduated":
#         columns.append({"fieldname": "graduation_date", "label": "Graduation Date", "fieldtype": "Date", "width": 120})

#     data = get_filtered_data(filters)
#     columns, data = add_custom_sl_no(columns, data)
#     return columns, data


# def get_filtered_data(filters):
#     """
#     Fetches filtered data based on the provided filters.
#     """
#     conditions = []
#     join_progress = False  

#     if filters.get("status") == "Graduated":
#         join_progress = True
#         conditions.append(f"(scp.graduation_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")
#     else:
#         conditions.append(f"(sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")

#     if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
#         conditions.append(f"sr.masjid_name = '{filters.get('filtered_masjid')}'")

#     if filters.get("status") and filters.get("status") != "All":
#         conditions.append(f"sr.status = '{filters.get('status')}'")

#     condition_string = " AND ".join(conditions) if conditions else "1=1"

#     if join_progress:
#         query = f"""
#             SELECT sr.*, scp.graduation_date
#             FROM `tabStudent Registration` sr
#             LEFT JOIN `tabStudent Complete Progress` scp
#             ON sr.student_name = scp.student_name2
#             WHERE {condition_string}
#             ORDER BY scp.graduation_date ASC
#         """
#     else:
#         query = f"""
#             SELECT *
#             FROM `tabStudent Registration` sr
#             WHERE {condition_string}
#             ORDER BY sr.registration_date ASC
#         """

#     return frappe.db.sql(query, as_dict=True)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# working code withoiut graduate filter


import frappe
from frappe.utils import getdate
from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no  # Import the utility function

@frappe.whitelist()
def get_filtered_masjids(status=None, start_date=None, end_date=None):
    """
    Returns a list of Masjids filtered by the provided status and date range.
    """
    frappe.logger().info(f"Fetching Masjids for status: {status}, start_date: {start_date}, end_date: {end_date}")

    conditions = ["sr.masjid_name IS NOT NULL", "sr.masjid_name != ''"]  # ✅ Exclude empty Masjid names

    if status and status != "All":
        conditions.append(f"sr.status = '{status}'")

    if start_date and end_date:
        # Use registration_date for all statuses, even "Graduated"
        conditions.append(f"sr.registration_date BETWEEN '{start_date}' AND '{end_date}'")

    condition_string = " AND ".join(conditions)

    # No need to join with `Student Complete Progress` table anymore
    query = f"""
        SELECT DISTINCT sr.masjid_name
        FROM `tabStudent Registration` sr
        WHERE {condition_string}
    """

    masjids = frappe.db.sql(query, as_dict=False)
    frappe.logger().info(f"Masjids Retrieved: {masjids}")

    # ✅ Remove empty Masjids before returning the list
    return [{"label": m[0], "value": m[0]} for m in masjids if m[0] and m[0].strip() != ""]


def execute(filters=None):
    """
    Main function to fetch and display the report data.
    """
    columns = [
        {"fieldname": "sl_no", "label": "Sl No", "fieldtype": "Int", "width": 50},  # ✅ Ensure SL No column exists
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

    if filters and filters.get("status") == "Graduated":
        columns.append({"fieldname": "graduation_date", "label": "Graduation Date", "fieldtype": "Date", "width": 120})

    data = get_filtered_data(filters)
    columns, data = add_custom_sl_no(columns, data)
    return columns, data


def get_filtered_data(filters):
    """
    Fetches filtered data based on the provided filters.
    """
    conditions = []

    # Instead of joining with the 'Student Complete Progress' doctype, 
    # we'll only query the 'Student Registration' doctype.
    if filters.get("status") == "Graduated":
        # For "Graduated" status, still use registration date filter, 
        # but ignore the join with Student Complete Progress
        conditions.append(f"(sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")
    else:
        conditions.append(f"(sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")

    if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
        conditions.append(f"sr.masjid_name = '{filters.get('filtered_masjid')}'")

    if filters.get("status") and filters.get("status") != "All":
        conditions.append(f"sr.status = '{filters.get('status')}'")

    condition_string = " AND ".join(conditions) if conditions else "1=1"

    # Fetch data only from `Student Registration` doctype
    query = f"""
        SELECT *
        FROM `tabStudent Registration` sr
        WHERE {condition_string}
        ORDER BY sr.registration_date ASC
    """

    student_data = frappe.db.sql(query, as_dict=True)

    # For "Graduated" students, set the graduation date from `Student Complete Progress` doctype
    if filters.get("status") == "Graduated":
        student_names = [student["student_name"] for student in student_data]
        if student_names:
            graduation_query = f"""
                SELECT student_name2, graduation_date
                FROM `tabStudent Complete Progress`
                WHERE student_name2 IN ({', '.join([f"'{name}'" for name in student_names])})
            """
            graduation_data = frappe.db.sql(graduation_query, as_dict=True)
            graduation_dict = {gd["student_name2"]: gd["graduation_date"] for gd in graduation_data}
            
            # Set graduation_date in the student data
            for student in student_data:
                student["graduation_date"] = graduation_dict.get(student["student_name"], None)

    return student_data

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#working code with both the functionality 
# import frappe
# from frappe.utils import getdate
# from shaheen_dev.shaheen_dev.utils.report_utils import add_custom_sl_no  # Import the utility function

# @frappe.whitelist()
# def get_filtered_masjids(status=None, start_date=None, end_date=None):
#     """
#     Returns a list of Masjids filtered by the provided status and date range.
#     """
#     frappe.logger().info(f"Fetching Masjids for status: {status}, start_date: {start_date}, end_date: {end_date}")

#     conditions = ["sr.masjid_name IS NOT NULL", "sr.masjid_name != ''"]  # ✅ Exclude empty Masjid names

#     if status and status != "All":
#         conditions.append(f"sr.status = '{status}'")

#     if start_date and end_date:
#         # Use registration_date for all statuses, even "Graduated"
#         conditions.append(f"sr.registration_date BETWEEN '{start_date}' AND '{end_date}'")

#     condition_string = " AND ".join(conditions)

#     # No need to join with `Student Complete Progress` table anymore
#     query = f"""
#         SELECT DISTINCT sr.masjid_name
#         FROM `tabStudent Registration` sr
#         WHERE {condition_string}
#     """

#     masjids = frappe.db.sql(query, as_dict=False)
#     frappe.logger().info(f"Masjids Retrieved: {masjids}")

#     # ✅ Remove empty Masjids before returning the list
#     return [{"label": m[0], "value": m[0]} for m in masjids if m[0] and m[0].strip() != ""]

# def execute(filters=None):
#     """
#     Main function to fetch and display the report data.
#     """
#     # Check if "Apply Graduate Filter" is checked (1) or unchecked (0)
#     apply_graduate_filter = filters.get("apply_graduate_filter", 0)

#     # Define columns to display in the report
#     columns = [
#         {"fieldname": "sl_no", "label": "Sl No", "fieldtype": "Int", "width": 50},
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

#     # Add the Graduation Date column if the status is "Graduated", regardless of the checkbox state
#     if filters.get("status") == "Graduated":
#         columns.append({"fieldname": "graduation_date", "label": "Graduation Date", "fieldtype": "Date", "width": 120})

#     # Fetch the data based on the checkbox value
#     if apply_graduate_filter == 1:  # If "Apply Graduate Filter" is checked
#         data = get_filtered_data_for_graduated(filters)
#     else:  # If unchecked, use the regular data fetching
#         data = get_filtered_data(filters)

#     columns, data = add_custom_sl_no(columns, data)
#     return columns, data

# def get_filtered_data_for_graduated(filters):
#     """
#     Fetches filtered data for graduated students based on the provided filters.
#     """
#     conditions = []

#     # Apply the date filter for all statuses, including "Graduated"
#     if filters.get("start_date") and filters.get("end_date"):
#         conditions.append(f"sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}'")

#     # If the status is "Graduated", apply the graduation_date filter as well
#     if filters.get("status") == "Graduated" and filters.get("start_date") and filters.get("end_date"):
#         conditions.append(f"scp.graduation_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}'")

#     # Apply masjid filter if selected
#     if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
#         conditions.append(f"sr.masjid_name = '{filters.get('filtered_masjid')}'")

#     # Apply status filter (only if it's not "All")
#     if filters.get("status") and filters.get("status") != "All":
#         conditions.append(f"sr.status = '{filters.get('status')}'")

#     # Combine conditions into a single condition string
#     condition_string = " AND ".join(conditions) if conditions else "1=1"

#     # Query to fetch data from `Student Registration` and `Student Complete Progress`
#     query = f"""
#         SELECT sr.*, scp.graduation_date
#         FROM `tabStudent Registration` sr
#         LEFT JOIN `tabStudent Complete Progress` scp
#         ON sr.student_name = scp.student_name2
#         WHERE {condition_string}
#         ORDER BY sr.registration_date ASC
#     """

#     student_data = frappe.db.sql(query, as_dict=True)

#     return student_data

# def get_filtered_data(filters):
    """
    Fetches filtered data based on the provided filters.
    """
    conditions = []

    # Instead of joining with the 'Student Complete Progress' doctype, 
    # we'll only query the 'Student Registration' doctype.
    if filters.get("status") == "Graduated":
        # For "Graduated" status, still use registration date filter, 
        # but ignore the join with Student Complete Progress
        conditions.append(f"(sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")
    else:
        conditions.append(f"(sr.registration_date BETWEEN '{filters.get('start_date')}' AND '{filters.get('end_date')}')")

    if filters.get("filtered_masjid") and filters.get("filtered_masjid") != "All":
        conditions.append(f"sr.masjid_name = '{filters.get('filtered_masjid')}'")

    if filters.get("status") and filters.get("status") != "All":
        conditions.append(f"sr.status = '{filters.get('status')}'")

    condition_string = " AND ".join(conditions) if conditions else "1=1"

    # Fetch data only from `Student Registration` doctype
    query = f"""
        SELECT *
        FROM `tabStudent Registration` sr
        WHERE {condition_string}
        ORDER BY sr.registration_date ASC
    """

    student_data = frappe.db.sql(query, as_dict=True)

    # For "Graduated" students, set the graduation date from `Student Complete Progress` doctype
    if filters.get("status") == "Graduated":
        student_names = [student["student_name"] for student in student_data]
        if student_names:
            graduation_query = f"""
                SELECT student_name2, graduation_date
                FROM `tabStudent Complete Progress`
                WHERE student_name2 IN ({', '.join([f"'{name}'" for name in student_names])})
            """
            graduation_data = frappe.db.sql(graduation_query, as_dict=True)
            graduation_dict = {gd["student_name2"]: gd["graduation_date"] for gd in graduation_data}
            
            # Set graduation_date in the student data
            for student in student_data:
                student["graduation_date"] = graduation_dict.get(student["student_name"], None)

    return student_data