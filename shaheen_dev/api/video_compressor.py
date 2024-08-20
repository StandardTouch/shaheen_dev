import os
import frappe
import subprocess
from werkzeug.utils import secure_filename

@frappe.whitelist(allow_guest=True)
def upload_and_convert_video():
    try:
        # Access the file from the request
        file = frappe.request.files.get('filedata')
        if not file:
            frappe.throw(("No file uploaded"))

        # Secure the filename and save the WebM file temporarily
        filename = secure_filename(file.filename)
        webm_path = os.path.join(frappe.get_site_path('private', 'files'), filename)

        with open(webm_path, 'wb') as f:
            f.write(file.read())

        # Generate the MP4 filename and path
        mp4_filename = os.path.splitext(filename)[0] + '.mp4'
        mp4_path = os.path.join(frappe.get_site_path('private', 'files'), mp4_filename)

        try:
            # Run FFmpeg to convert WebM to MP4
            subprocess.run(['ffmpeg', '-i', webm_path, mp4_path], check=True)

            # Read the MP4 file
            with open(mp4_path, 'rb') as f:
                mp4_data = f.read()

            # Clean up temporary files
            os.remove(webm_path)
            os.remove(mp4_path)

            # Return the MP4 file as a response
            frappe.local.response.filecontent = mp4_data
            frappe.local.response.type = "binary"
            frappe.local.response.filename = mp4_filename
            frappe.local.response.content_type = "video/mp4"

            return

        except subprocess.CalledProcessError as e:
            frappe.logger().error(f'FFmpeg error: {e}')
            frappe.throw(('Video conversion failed'))

    except Exception as e:
        frappe.logger().error(f'Error in video upload and conversion: {e}')
        frappe.throw(('An error occurred during the video upload and conversion process'))
