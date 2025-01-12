# import frappe
# from frappe.utils import getdate

# def execute(filters=None):
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

#     # If filters are not set or incomplete, return columns and empty data
#     if not filters or not filters.get("masjid") or not filters.get("start_date") or not filters.get("end_date"):
#         return columns, []

#     # Fetch filtered data
#     data = get_filtered_data(filters)

#     return columns, data


# def get_filtered_data(filters):
#     # Validate filters
#     if not filters:
#         filters = {}

#     # Build conditions based on filters
#     conditions = []
#     if filters.get("masjid"):
#         conditions.append(f"masjid_name = '{filters.get('masjid')}'")
#     if filters.get("start_date") and filters.get("end_date"):
#         start_date = getdate(filters.get("start_date"))
#         end_date = getdate(filters.get("end_date"))
#         conditions.append(f"registration_date BETWEEN '{start_date}' AND '{end_date}'")

#     # Check for the "All" option in status
#     if filters.get("status") and filters.get("status") != "All":
#         conditions.append(f"status = '{filters.get('status')}'")

#     condition_string = " AND ".join(conditions) if conditions else "1=1"

#     # SQL query to fetch data
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
#     """

#     # Debug log for the generated query (useful for troubleshooting)
#     frappe.logger().debug(f"Generated query: {query}")

#     return frappe.db.sql(query, as_dict=True)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# import frappe
# from frappe.utils import getdate  # Import getdate to handle date conversions

# def execute(filters=None):
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

#     # If filters are not set or incomplete, return columns and empty data
#     # Remove the check for 'masjid' to allow it to be optional
#     if not filters or not filters.get("start_date") or not filters.get("end_date"):
#         return columns, []

#     # Fetch filtered data
#     data = get_filtered_data(filters)

#     return columns, data


# def get_filtered_data(filters):
#     # Validate filters
#     if not filters:
#         filters = {}

#     # Build conditions based on filters
#     conditions = []

#     # Always apply the date range filter
#     if filters.get("start_date") and filters.get("end_date"):
#         start_date = getdate(filters.get("start_date"))
#         end_date = getdate(filters.get("end_date"))
#         # Include students with NULL registration_date
#         conditions.append(f"(registration_date BETWEEN '{start_date}' AND '{end_date}')")

#     # Apply masjid filter only if it is selected
#     if filters.get("masjid"):
#         conditions.append(f"masjid_name = '{filters.get('masjid')}'")

#     # Check for the "status" filter
#     if filters.get("status") and filters.get("status") != "All":
#         conditions.append(f"status = '{filters.get('status')}'")

#     # Combine all conditions; default to "1=1" if no conditions
#     condition_string = " AND ".join(conditions)

#     # SQL query to fetch data, ordering by registration_date
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
#             registration_date IS NULL,  -- NULL dates will be ordered last
#             registration_date ASC       -- Non-NULL dates will be ordered earliest to latest
#     """

#     # Debug log for the generated query (useful for troubleshooting)
#     frappe.logger().debug(f"Generated query: {query}")

#     # Execute the SQL query and return results
#     return frappe.db.sql(query, as_dict=True)


import frappe
from frappe.utils import getdate

def execute(filters=None):
    # Define the base columns for the report
    columns = [
        {"fieldname": "student_name", "label": "Student Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "fathers_name", "label": "Fathers Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "contact_number", "label": "Contact Number", "fieldtype": "Data", "width": 150},
        {"fieldname": "registrar_name", "label": "Registrar Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "address", "label": "Address", "fieldtype": "Data", "width": 150},
        # {"fieldname": "area", "label": "Area", "fieldtype": "Data", "width": 150},
        # {"fieldname": "pincode", "label": "Pincode", "fieldtype": "Data", "width": 100},
        {"fieldname": "masjid_name", "label": "Masjid Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "cluster_no", "label": "Cluster No", "fieldtype": "Data", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
        {"fieldname": "registration_date", "label": "Registration Date", "fieldtype": "Date", "width": 120},
    ]

    # Add the "Last Topic" column only if the status is "In Batch"
    if filters and filters.get("status") == "In Batch":
        columns.append({"fieldname": "last_topic_label", "label": "Last Topic", "fieldtype": "Data", "width": 150})

    # If filters are not set or incomplete, return columns and empty data
    if not filters or not filters.get("start_date") or not filters.get("end_date"):
        return columns, []

    # Fetch filtered data
    data = get_filtered_data(filters)

    return columns, data


def get_filtered_data(filters):
    if not filters:
        filters = {}

    # Build conditions for the query
    conditions = []

    # Date filter
    if filters.get("start_date") and filters.get("end_date"):
        start_date = getdate(filters.get("start_date"))
        end_date = getdate(filters.get("end_date"))
        conditions.append(f"(registration_date BETWEEN '{start_date}' AND '{end_date}')")

    # Masjid filter
    if filters.get("masjid"):
        conditions.append(f"masjid_name = '{filters.get('masjid')}'")

    # Status filter
    if filters.get("status") and filters.get("status") != "All":
        if filters.get("status") == "In Batch":
            conditions.append(f"status = 'In Batch'")
        else:
            conditions.append(f"status = '{filters.get('status')}'")

    # Combine all conditions
    condition_string = " AND ".join(conditions)

    # Query to fetch student registration data
    query = f"""
        SELECT
            student_name,
            fathers_name,
            contact_number,
            registrar_name,
            address,
            # area,
            # pincode,
            masjid_name,
            cluster_no,
            status,
            registration_date
        FROM
            `tabStudent Registration`
        WHERE
            {condition_string}
        ORDER BY
            registration_date IS NULL,  -- NULL dates will be ordered last
            registration_date ASC       -- Non-NULL dates will be ordered earliest to latest
    """

    # Fetch student data
    student_data = frappe.db.sql(query, as_dict=True)
    frappe.logger().debug(f"Student Data: {student_data}")

    # If status is "In Batch", fetch last_topic_label from Student Complete Progress
    if filters.get("status") == "In Batch":
        progress_data = frappe.db.sql("""
            SELECT
                student_name2,  -- Fetch student_name2 from Student Complete Progress
                last_topic_label
            FROM
                `tabStudent Complete Progress`
        """, as_dict=True)
        frappe.logger().debug(f"Progress Data: {progress_data}")

        # Create a lookup dictionary for last_topic_label
        progress_lookup = {row["student_name2"]: row["last_topic_label"] for row in progress_data}
        frappe.logger().debug(f"Progress Lookup: {progress_lookup}")

        # Add last_topic_label to the student data
        for row in student_data:
            if row["status"] == "In Batch":
                row["last_topic_label"] = progress_lookup.get(row["student_name"], "")

    frappe.logger().debug(f"Final Student Data: {student_data}")
    return student_data
