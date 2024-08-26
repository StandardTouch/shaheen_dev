import subprocess
import os
import frappe
import requests
import subprocess
import os
import frappe

import subprocess
import os
import frappe

def convert_webm_to_mp4_target_size(webm_url, target_size_mb, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Download the WebM file
            webm_file_path = frappe.get_site_path('public', 'files', os.path.basename(webm_url))
            mp4_file_path = os.path.splitext(webm_file_path)[0] + '.mp4'
            
            # Get video duration in seconds
            duration_command = [
                'ffprobe', 
                '-v', 'error', 
                '-show_entries', 'format=duration', 
                '-of', 'default=noprint_wrappers=1:nokey=1', 
                webm_file_path
            ]
            duration = float(subprocess.check_output(duration_command).strip())
            
            # Calculate target bitrate
            target_size_bytes = target_size_mb * 1024 * 1024
            target_bitrate = (target_size_bytes * 8) / duration
            
            # Allocate 10% of bitrate for audio, 90% for video
            audio_bitrate = int(target_bitrate * 0.1)
            video_bitrate = int(target_bitrate * 0.9)
            
            # Command to convert WebM to MP4 using FFmpeg
            command = [
                'ffmpeg',
                '-y',  # Automatically overwrite existing files
                '-i', webm_file_path,
                '-c:v', 'libx264',
                '-b:v', f'{video_bitrate}bps',
                '-c:a', 'aac',
                '-b:a', f'{audio_bitrate}bps',
                '-strict', 'experimental',
                mp4_file_path
            ]
            
            subprocess.run(command, check=True)
            
            mp4_url = frappe.utils.get_url() + f'/files/{os.path.basename(mp4_file_path)}'
            return mp4_url

        except subprocess.CalledProcessError as e:
            frappe.log_error(f"FFmpeg error on attempt {attempt + 1}: {str(e)}")
        except Exception as e:
            frappe.log_error(f"Exception during conversion on attempt {attempt + 1}: {str(e)}")

    return None


def send_video_after_conversion(mp4_url, token, msg1, recipients, video_url,docname):
    
    doc = frappe.get_doc("Weekly Student Progress", docname)
    # Prepare the payload for the WhatsApp API request
    payload = {
        'token': token,
        'to': recipients,
        'video': mp4_url,
        'caption': msg1
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    # Send the video via WhatsApp with retries
    for attempt in range(3):
        response = requests.post(video_url, data=payload, headers=headers)
        
        if response.status_code == 200:
            print(f'WhatsApp message sent successfully for video: {mp4_url}')
            break  # Exit the retry loop on success
        else:
            frappe.log_error(f"WhatsApp API error on attempt {attempt + 1} for video {mp4_url}: {response.text}")
            print(f"WhatsApp API error on attempt {attempt + 1} for video {mp4_url}: {response.text}")
            if attempt == 2:  # If this was the last attempt, log the failure
                frappe.log_error(f"Failed to send WhatsApp message after several attempts for video: {mp4_url}")

def process_and_send_video(docname, video_file_url, token, msg1, recipients, video_url):
    # Convert WebM to MP4 with retries and logging
    mp4_url = convert_webm_to_mp4_with_logging(video_file_url)
    
    if mp4_url:
        # Enqueue sending the video after conversion
        frappe.enqueue(
            send_video_after_conversion,
            queue='long',
            timeout=6000,
            mp4_url=mp4_url,
            token=token,
            msg1=msg1,
            recipients=recipients,
            video_url=video_url,
            docname=docname,
            
        )
    else:
        frappe.log_error(f"Failed to convert video to MP4 after several attempts: {video_file_url}")

@frappe.whitelist()
def send_whatsapp_with_video(docname):
    frappe.enqueue(
        process_videos_and_send,
        queue='long',
        timeout=6000,
        docname=docname
    )

def process_videos_and_send(docname):
    # Fetch the document
    doc = frappe.get_doc("Weekly Student Progress", docname)  # Replace with your actual Doctype name
    
    # Fetch settings
    settings = frappe.get_doc('Shaheen Whatsapp Settings')
    token = settings.get('token')
    msg1 = settings.get('message')
    video_url = settings.get('video_url')
    
    # Get the recipient's phone number
    recipients = doc.contact_number  # Customize this list if needed
    
    # Fetch video files attached to the document
    video_files = frappe.get_all('File', filters={"attached_to_name": doc.name, "attached_to_doctype": doc.doctype}, fields=["file_url"])
    if not video_files:
        frappe.throw(("No video files found attached to the document."))
    
    # Get the site URL
    site_url = frappe.utils.get_url()

    # Enqueue processing and sending each video
    for url in video_files:
        video_file_url = f"{site_url}{url.file_url}"
        frappe.enqueue(
            process_and_send_video,
            queue='long',
            timeout=6000,
            docname=docname,
            video_file_url=video_file_url,
            token=token,
            msg1=msg1,
            recipients=recipients,
            video_url=video_url
        )
