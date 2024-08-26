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
