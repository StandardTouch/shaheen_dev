import frappe
from PIL import Image
from fpdf import FPDF
import os
import io
from frappe import _

@frappe.whitelist()
def generate_pdf_from_folder(folder_path):
    try:
        # Log the folder path received from the frontend
        frappe.logger().info(f"Received folder path: {folder_path}")
        
        # Retrieve all image files in the selected folder using Frappe ORM
        file_records = frappe.get_all(
            'File', 
            fields=['name', 'file_name', 'file_url', 'custom_is_exported'], 
            filters={'folder': folder_path, 'custom_is_exported': 0}
        )

        # Log the retrieved file records to debug
        frappe.logger().info(f"Retrieved file records from folder '{folder_path}': {file_records}")
        
        image_files = []
        for file_record in file_records:
            file_url = file_record['file_url']

            # Check if file_url is not None
            if not file_url:
                frappe.logger().error(f"File URL is missing for record {file_record['name']}")
                continue  # Skip files with missing URLs

            # Construct the full file path
            full_file_path = frappe.get_site_path('public', 'files', os.path.basename(file_url))
            
            # Log the full file path for troubleshooting
            frappe.logger().info(f"Constructed file path: {full_file_path}")
            
            if full_file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append({
                    "file_id": file_record['name'],  # File ID for updating is_exported
                    "file_path": full_file_path
                })

        if not image_files:
            frappe.throw(f"No image files found in the folder {folder_path}.")

        # Sort the image files to ensure they are processed in a consistent order
        image_files.sort(key=lambda x: x['file_path'])

        # Create a PDF from the image files in landscape mode
        pdf = FPDF(orientation='L', unit='mm', format='A4')

        # Keep track of successfully processed file IDs for batch updating later
        updated_files = []

        for image in image_files:
            image_file = image['file_path']
            file_id = image['file_id']

            # Check if file exists before adding it to the PDF
            if not os.path.exists(image_file):
                frappe.logger().error(f"File not found: {image_file}")
                frappe.throw(f"File not found: {image_file}")

            # Log the image file being processed
            frappe.logger().info(f"Processing image: {image_file}")

            # Add image to the PDF
            pdf.add_page()
            pdf.image(image_file, 10, 10, 277)  # 277mm is the width of an A4 page in landscape

            # Collect the file ID for updating custom_is_exported later
            updated_files.append(file_id)

        # Batch update all successfully processed files' custom_is_exported field to True (1)
        if updated_files:
            frappe.db.set_value('File', updated_files, 'custom_is_exported', 1)
            frappe.db.commit()
            frappe.logger().info(f"Updated custom_is_exported for files: {updated_files}")

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
