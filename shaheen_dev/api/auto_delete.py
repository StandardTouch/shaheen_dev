import frappe
from frappe.utils import nowdate, add_days,getdate

def delete_old_files():
    # Define the doctype where the files are attached
    doctype = "Weekly Student Progress"

    docs = frappe.get_all(doctype, fields=["name"])

    for doc in docs:
        # Get the attached files for each document
        attached_files = frappe.get_all("File", filters={"attached_to_doctype": doctype, "attached_to_name": doc.name})
        
        for file in attached_files:
            # Get the file document
            file_doc = frappe.get_doc("File", file.name)
            
            # Convert the creation date to a date object for comparison
            file_creation_date = getdate(file_doc.creation)
            comparison_date = getdate(add_days(nowdate(), -7))

            # Check if the file was attached more than 7 days ago
            if file_creation_date <= comparison_date:
                # Delete the file
                file_doc.delete()
                frappe.db.commit()

                # Optionally, log the deletion
                frappe.logger().info(f"Deleted file {file_doc.file_name} attached to {doctype} {doc.name}")


