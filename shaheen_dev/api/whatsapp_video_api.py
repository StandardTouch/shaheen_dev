import frappe
from frappe import _
import requests

# @frappe.whitelist()
# def send_whatsapp_with_video(docname):
#     # Enqueue the background job
#     # frappe.enqueue('shaheen_dev.whatsapp_video_api.api.process_whatsapp_video_sending', docname=docname)
#     frappe.enqueue(
#     method=process_whatsapp_video_sending,
#     queue="short",
#     timeout=200,
#     doc=docname,
#     enqueue_after_commit=True
# )

@frappe.whitelist()
def send_whatsapp_with_video(docname):
    doc = frappe.get_doc("Weekly Student Progress", docname)  # Replace with your actual Doctype name
    token = frappe.get_doc('Shaheen Whatsapp Settings').get('token')
    msg1 = frappe.get_doc('Shaheen Whatsapp Settings').get('message')
    video_url = frappe.get_doc('Shaheen Whatsapp Settings').get('video_url')
    
    recipients = doc.custom_phone  # Customize this list

    video_files = frappe.get_all('File', filters={"attached_to_name": doc.name, "attached_to_doctype": doc.doctype}, fields=["file_url"])
    if not video_files:
        frappe.throw(_("No video files found attached to the document."))
    
    site_url = frappe.utils.get_url()
    print(video_url)
    for url in video_files:
        video_file_url = f"{site_url}{url.file_url}"
        mp4_url = convert_webm_to_mp4(video_file_url)  # Assume you have this function implemented as before
        
        if not mp4_url:
            frappe.throw(_("Failed to convert video to MP4."))
        
        payload = {
            'token': token,
            'to': doc.custom_number,
            'video': mp4_url,
            'caption': msg1
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(video_url, data=payload, headers=headers)
        
        print(response.json())
        
        if response.status_code == 200:
            print('Sent')
        else:
            frappe.log_error("WhatsApp API returned an error", response.text)

def convert_webm_to_mp4(webm_url):
    try:
        # Construct the URL for the Frappe API method
        conversion_url = frappe.utils.get_url() + '/api/method/shaheen_dev.api.video_converter.convert_to_mp4'
        
        # Send a POST request to the API method with the WebM file URL
        conversion_response = requests.post(
            conversion_url,
            data={'file_url': webm_url},
            headers={'X-Frappe-CSRF-Token': frappe.session.csrf_token}
        )
        
        print(conversion_response)

        # Check if the conversion was successful
        if conversion_response.status_code == 200:
            response_json = conversion_response.json()
            print(response_json)
            mp4_url = response_json.get('message', {}).get('file_url')
            print(f"Conversion successful: {mp4_url}")
            return mp4_url
        else:
            print(f"Failed to convert video: {conversion_response.content}")
            return None

    except Exception as e:
        print(f"Exception during conversion: {str(e)}")
        return None

