import frappe
from PIL import Image
from fpdf import FPDF
import os
import io
from frappe import _

@frappe.whitelist()
def generate_pdf_from_folder(folder_path):
    try:
        # Retrieve all image files in the selected folder using Frappe ORM
        file_records = frappe.get_all('File', fields=['file_name', 'file_url'], filters={'folder': folder_path})
        
        image_files = []
        for file_record in file_records:
            file_url = file_record['file_url']
            if file_url.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(frappe.get_site_path(file_url.lstrip('/')))

        if not image_files:
            frappe.throw(f"No image files found in the folder {folder_path}.")

        # Sort the image files to ensure they are processed in a consistent order
        image_files.sort()

        # Create a PDF from the image files in landscape mode
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        for image_file in image_files:
            pdf.add_page()
            # Adjust positioning to fit landscape mode
            pdf.image(image_file, 10, 10, 277)  # 277mm is the width of an A4 page in landscape

        # Generate PDF file in memory
        pdf_output = io.BytesIO()
        pdf_output_value = pdf.output(dest='S').encode('latin1')  # Output as string and encode to binary
        pdf_output.write(pdf_output_value)
        pdf_output.seek(0)

        # Send the PDF as a file download response
        frappe.local.response.filename = f"{os.path.basename(folder_path)}_Certificates.pdf"
        frappe.local.response.filecontent = pdf_output.read()
        frappe.local.response.type = "download"

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Error in generate_pdf_from_folder")
        frappe.throw(_("There was an error generating the PDF. Please check the logs for more details."))
