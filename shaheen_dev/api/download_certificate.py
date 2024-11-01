import frappe
from PIL import Image
from fpdf import FPDF
import os
import io
from frappe import _
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def download_student_progress_pdf(student_ids):
    try:
        student_id_list = student_ids.split(',')
        
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        updated_files = []

        for student_id in student_id_list:
            # Retrieve image records for each student
            student_progress = frappe.get_all(
                'Student Complete Progress', 
                filters={'name': student_id, 'is_downloaded': 0, 'certificate_downloaded': 'No'},
                fields=['name', 'attached_certificate']
            )

            image_files = []
            for record in student_progress:
                image_url = record['attached_certificate']
                if not image_url:
                    continue

                full_file_path = frappe.get_site_path('public', 'files', os.path.basename(image_url))
                if full_file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_files.append({
                        "file_id": record['name'],
                        "file_path": full_file_path
                    })

            # Add each image to the PDF
            for image in image_files:
                image_file = image['file_path']
                pdf.add_page()
                pdf.image(image_file, 10, 10, 277)
                updated_files.append(image["file_id"])

        # Batch update all processed files' custom_is_exported and is_downloaded fields
        if updated_files:
            for file_id in updated_files:
                frappe.db.set_value('Student Complete Progress', file_id, 'is_downloaded', 1)
                frappe.db.set_value('Student Complete Progress', file_id, 'certificate_downloaded', 'Yes')
            frappe.db.commit()

        # Get the current date and format it
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Generate the PDF with date in the filename
        pdf_output = io.BytesIO()
        pdf_output_value = pdf.output(dest='S').encode('latin1')
        pdf_output.write(pdf_output_value)
        pdf_output.seek(0)

        frappe.local.response.filename = f"Student_Certificates_{current_date}.pdf"
        frappe.local.response.filecontent = pdf_output.read()
        frappe.local.response.type = "download"

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Error in download_student_progress_pdf")
        frappe.throw(_("An error occurred while generating the PDF. Check the logs for details."))
