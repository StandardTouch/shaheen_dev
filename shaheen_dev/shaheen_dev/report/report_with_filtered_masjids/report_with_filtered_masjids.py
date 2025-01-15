import frappe
from frappe.utils import getdate

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

    if not filters or not filters.get("start_date") or not filters.get("end_date"):
        return columns, []

    data = get_filtered_data(filters)
    return columns, data


def get_filtered_data(filters):
    """
    Fetches filtered data based on the provided filters.
    """
    conditions = []

    # Apply date range filter
    if filters.get("start_date") and filters.get("end_date"):
        start_date = getdate(filters.get("start_date"))
        end_date = getdate(filters.get("end_date"))
        conditions.append(f"(registration_date BETWEEN '{start_date}' AND '{end_date}')")

    # Apply filtered Masjid filter
    if filters.get("filtered_masjid"):
        conditions.append(f"masjid_name = '{filters.get('filtered_masjid')}'")

    # Apply status filter
    if filters.get("status") and filters.get("status") != "All":
        conditions.append(f"status = '{filters.get('status')}'")

    condition_string = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            student_name,
            fathers_name,
            contact_number,
            registrar_name,
            address,
            area,
            pincode,
            masjid_name,
            cluster_no,
            status,
            registration_date
        FROM
            `tabStudent Registration`
        WHERE
            {condition_string}
        ORDER BY
            registration_date ASC
    """

    return frappe.db.sql(query, as_dict=True)

@frappe.whitelist()
def get_filtered_masjids(status=None, start_date=None, end_date=None):
    """
    Returns a list of Masjids filtered by the provided status and date range.
    Only includes Masjids with data in the Student Registration doctype.
    """
    # Base condition: only include Masjids with student data
    conditions = ["masjid_name IS NOT NULL"]

    # Add status condition if provided
    if status and status != "All":
        conditions.append(f"status = '{status}'")

    # Add date range condition if provided
    if start_date and end_date:
        conditions.append(f"registration_date BETWEEN '{start_date}' AND '{end_date}'")

    # Combine conditions into a WHERE clause
    condition_string = " AND ".join(conditions)

    # Query to fetch distinct Masjids with data
    query = f"""
        SELECT DISTINCT
            masjid_name
        FROM
            `tabStudent Registration`
        WHERE
            {condition_string}
    """

    # Execute the query
    masjids = frappe.db.sql(query, as_dict=False)

    # Format the results for the dropdown
    return [{"label": m[0], "value": m[0]} for m in masjids if m[0]]
