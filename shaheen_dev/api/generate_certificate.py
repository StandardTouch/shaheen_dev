import frappe
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
import os
import requests

@frappe.whitelist(allow_guest=True)
def generate_send_certificate(docname):
    frappe.enqueue(process_certificate_and_send,
        queue='short',
        timeout=6000,
        docname=docname
    )


def process_certificate_and_send(docname):
    try:
        # Fetch the student details from the provided docname
        student_details = frappe.get_doc('Weekly Student Progress', docname)
        student_name = student_details.students_name
        cluster_no = student_details.cluster_no
        masjid = student_details.masjid_name
        completion_date = student_details.date_of_progress
        contact_number = student_details.contact_number

        # Fetch the certificate template from the private directory based on the cluster_no
        template_file_url = f"/private/files/Cluster {cluster_no}.pdf"
        template_file_path = frappe.get_site_path(template_file_url.lstrip('/'))

        if not os.path.exists(template_file_path):
            frappe.throw(f"Template file {template_file_path} does not exist.")

        # Convert the PDF to an image
        images = convert_from_path(template_file_path)
        image = images[0]  # Assuming the template is a single-page PDF
        draw = ImageDraw.Draw(image)

        # Define font and size
        font_path = frappe.get_site_path("private", "files", "Merriweather-Italic.ttf")
        font = ImageFont.truetype(font_path, 40)

        # Define text position
        name_position = (1000, 930)  # Example position

        # Add the student's name and completion date to the image
        draw.text(name_position, student_name, font=font, fill="black")

        # Define the new folder path in ERPNext File Doctype for public access
        new_folder_name = f"Cluster {cluster_no}"
        new_subfolder_name = masjid
        new_folder_path = frappe.get_site_path("public", "files", new_folder_name)
        new_subfolder_path = frappe.get_site_path("public", "files", new_folder_name, new_subfolder_name)

        # Ensure the folders exist
        os.makedirs(new_subfolder_path, exist_ok=True)

        # Save the edited image in the public directory
        new_file_name = f"{cluster_no}-{student_name}-{completion_date}.jpg"
        new_file_path = os.path.join(new_subfolder_path, new_file_name)

        # Save the image
        try:
            image.save(new_file_path)
        except Exception as e:
            frappe.throw(f"Error saving the image file: {str(e)}")

        # Verify the file exists
        if not os.path.exists(new_file_path):
            frappe.throw(f"The file was not found at {new_file_path}. Please check the file saving process.")

        # Ensure the parent folder exists in the File Doctype
        if not frappe.db.exists("File", {"file_name": new_folder_name, "folder": "Home"}):
            parent_folder = frappe.get_doc({
                "doctype": "File",
                "file_name": new_folder_name,
                "folder": "Home",
                "is_folder": 1
            })
            parent_folder.insert()
        else:
            parent_folder = frappe.get_doc("File", {"file_name": new_folder_name, "folder": "Home"})

        # Ensure the subfolder exists in the File Doctype
        if not frappe.db.exists("File", {"file_name": new_subfolder_name, "folder": parent_folder.name}):
            subfolder = frappe.get_doc({
                "doctype": "File",
                "file_name": new_subfolder_name,
                "folder": parent_folder.name,
                "is_folder": 1
            })
            subfolder.insert()
        else:
            subfolder = frappe.get_doc("File", {"file_name": new_subfolder_name, "folder": parent_folder.name})

        # Create a new File document for the generated certificate
        new_file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": new_file_name,
            "file_url": f"/files/{new_folder_name}/{new_subfolder_name}/{new_file_name}",
            "folder": subfolder.name, 
            'is_private': 0,
        })
        doc = frappe.get_doc("Student Complete Progress", student_details.student_id)
        doc.attached_certificate = new_file_doc.file_url
        doc.reload()
        doc.save(ignore_permissions= True)
        frappe.db.commit()
        frappe.enqueue(send_certificate,
        queue='short',
        timeout=6000,
        docname=docname,
        student_id=student_details.student_id,
        contact_number = contact_number,
        
    )
        

        try:
            new_file_doc.insert()
            student_details.attached_certificate = new_file_doc.file_url
            student_details.save(ignore_permissions= True)
            frappe.db.commit()
        except Exception as e:
            frappe.throw(f"Error inserting the file into the File doctype: {str(e)}")

        return new_file_doc.file_url

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Error in generate_certificate")
        frappe.throw("There was an error generating the certificate. Please check the logs for more details.")


@frappe.whitelist()
def send_certificate(docname,student_id,contact_number):
    settings = frappe.get_doc('Shaheen Whatsapp Settings')
    token = settings.get('token')
    msg1 = settings.get('message')
    image_url = settings.get('image_url')
    
    doc = frappe.get_doc("Student Complete Progress", student_id)
    
    
    
    site_url = frappe.utils.get_url()
    
    site_image_url = f"{site_url}{doc.attached_certificate}"

    
    payload = {
        'token': token,
        'to': contact_number,
        'image': site_image_url,  # Use the actual file URL generated
        'caption': msg1
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(image_url, data=payload, headers=headers)
    
    if response.status_code == 200:
        frappe.logger().info('WhatsApp message sent successfully')
    else:
        frappe.log_error(f"WhatsApp API error: {response.text}")
        frappe.logger().error(f"WhatsApp API error: {response.text}")
