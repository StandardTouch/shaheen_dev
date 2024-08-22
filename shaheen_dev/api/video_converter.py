import frappe
import os
import subprocess
import logging
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response

# Configure logging to the terminal
logging.basicConfig(level=logging.DEBUG)

@frappe.whitelist(allow_guest=True)
def convert_to_mp4():
    print("convert_to_mp4 function called")
    logging.debug("convert_to_mp4 function called")

    try:
        if 'file' not in frappe.request.files:
            print("No file part in the request")
            logging.error("No file part in the request")
            return {'error': "No file part"}, 400

        file = frappe.request.files['file']
        print(f"File received: {file.filename}")
        logging.debug(f"File received: {file.filename}")

        if file.filename == '':
            print("No selected file")
            logging.error("No selected file")
            return {'error': "No selected file"}, 400

        filename = secure_filename(file.filename)
        input_path = os.path.join('/tmp', filename)
        output_filename = os.path.splitext(filename)[0] + '.mp4'
        output_path = os.path.join(frappe.get_site_path('public', 'files'), output_filename)

        # Save the input WebM file temporarily
        file.save(input_path)
        print(f"File saved to: {input_path}")
        logging.debug(f"File saved to: {input_path}")

        # Re-encode the video and audio to formats compatible with MP4
        command = ['ffmpeg', '-y', '-v', 'verbose', '-i', input_path, '-c:v', 'libx264', '-c:a', 'aac', output_path]
        print(f"Running command: {' '.join(command)}")
        logging.debug(f"Running command: {' '.join(command)}")

        # Execute the command with a timeout
        process = subprocess.run(command, capture_output=True, text=True, timeout=120)

        print(f"ffmpeg stdout: {process.stdout}")
        print(f"ffmpeg stderr: {process.stderr}")
        logging.debug(f"ffmpeg stdout: {process.stdout}")
        logging.debug(f"ffmpeg stderr: {process.stderr}")

        if process.returncode != 0:
            error_message = f"ffmpeg error: {process.stderr}"
            print(error_message)
            logging.error(error_message)
            raise Exception(error_message)

        # Remove the temporary input file after conversion
        os.remove(input_path)

        # Return the file URL to the frontend
        file_url = f'/files/{output_filename}'
        print(f"Conversion successful, file saved to: {file_url}")
        logging.debug(f"Conversion successful, file saved to: {file_url}")

        return {'file_url': file_url}

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        logging.error(f"Exception occurred: {str(e)}")
        frappe.log_error(message=str(e), title="Video Conversion Error")
        return {'error': str(e)}, 500
