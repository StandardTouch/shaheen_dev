// document.addEventListener('DOMContentLoaded', function () {
//     // Load Vue
//     const vueScript = document.createElement('script');
//     vueScript.src = 'https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js';
//     document.head.appendChild(vueScript);

//     vueScript.onload = function () {
//         initializeVueApp();
//     };
// });

// function initializeVueApp() {
//     Vue.component('video-recorder', {
//         template: `
//         <div id="videoRecorderModal" class="modal fade" tabindex="-1" role="dialog">
//             <div class="modal-dialog" role="document">
//                 <div class="modal-content">
//                     <div class="modal-header">
//                         <h5 class="modal-title">Record Video</h5>
//                         <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="closeModal">
//                             <span aria-hidden="true">&times;</span>
//                         </button>
//                     </div>
//                     <div class="modal-body">
//                         <div class="video-container">
//                             <video ref="videoPreview" autoplay muted playsinline></video>
//                             <div class="controls">
//                                 <button @click="switchCamera" class="button switch">🔄 Switch Camera</button>
//                                 <button @click="startRecording" class="button start" :disabled="isRecording">🔴 Start Recording</button>
//                                 <button @click="stopRecording" class="button stop" :disabled="!isRecording">⏹️ Stop Recording</button>
//                                 <button @click="recordAgain" class="button record-again" v-show="showRecordAgain">🔄 Record Again</button>
//                             </div>
//                             <a v-if="videoUrl" :href="videoUrl" download="recorded-video.webm" class="download-link">⬇️ Download Video</a>
//                             <div class="recording-time">{{ recordingTime }}</div>
//                             <div class="video-duration" v-if="videoDuration">Duration: {{ videoDuration }}</div>
//                             <div class="camera-mode-label">{{ cameraModeLabel }}</div>
//                             <!-- Loading Screen -->
//                             <div v-if="loading" class="loading-overlay">
//                                 <div class="spinner-border text-primary" role="status">
//                                     <span class="sr-only">Loading...</span>
//                                 </div>
//                                 <p>Processing, please wait...</p>
//                             </div>
//                         </div>
//                     </div>
//                     <div class="modal-footer">
//                         <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
//                         <button class="btn btn-success" @click="attachVideo" :disabled="!videoUrl || loading">Attach Video</button>
//                     </div>
//                 </div>
//             </div>
//         </div>
//         `,
//         data() {
//             return {
//                 stream: null,
//                 mediaRecorder: null,
//                 recordedBlobs: [],
//                 isRecording: false,
//                 videoUrl: null,
//                 recordingTime: '00:00',
//                 videoDuration: '',
//                 cameraModeLabel: 'Back Camera',
//                 currentFacingMode: 'environment',
//                 startTime: null,
//                 recordingTimeInterval: null,
//                 showRecordAgain: false,
//                 loading: false,
//                 currentFieldName: null,
//             };
//         },
//         methods: {
//             async initializeCamera(facingMode = 'environment') {
//                 try {
//                     if (this.stream) {
//                         this.stream.getTracks().forEach(track => track.stop());
//                     }
//                     this.stream = await navigator.mediaDevices.getUserMedia({
//                         video: { facingMode: facingMode },
//                         audio: true
//                     });
//                     this.$refs.videoPreview.srcObject = this.stream;
//                     this.cameraModeLabel = facingMode === 'user' ? 'Front Camera' : 'Back Camera';
//                 } catch (error) {
//                     console.error("Error accessing media devices.", error);
//                     alert('Could not access camera and microphone. Please check your permissions.');
//                 }
//             },
//             startRecording() {
//                 try {
//                     this.recordedBlobs = [];
//                     this.mediaRecorder = new MediaRecorder(this.stream, {
//                         mimeType: 'video/webm;codecs=vp8,opus',
//                         videoBitsPerSecond: 200000,  // Adjusted video bitrate to 0.5 Mbps (512 kbps)
//                         audioBitsPerSecond: 64000    // Adjusted audio bitrate to 64 kbps
//                     });
//                     this.mediaRecorder.ondataavailable = (event) => {
//                         if (event.data && event.data.size > 0) {
//                             this.recordedBlobs.push(event.data);
//                         }
//                     };
//                     this.mediaRecorder.start(100); // Collect data in 100ms chunks
//                     this.startTime = Date.now();
//                     this.recordingTime = "00:00";
//                     this.recordingTimeInterval = setInterval(this.updateRecordingTime, 1000);
//                     this.isRecording = true;
//                     this.showRecordAgain = false;
//                 } catch (error) {
//                     console.error("Error starting recording:", error);
//                     alert('Could not start recording. Please try again.');
//                 }
//             }
//             ,
//             async stopRecording() {
//                 try {
//                     this.mediaRecorder.stop();
//                     clearInterval(this.recordingTimeInterval);
//                     this.loading = true;

//                     this.mediaRecorder.onstop = () => {
//                         const videoBlob = new Blob(this.recordedBlobs, { type: 'video/webm' });
//                         this.videoUrl = URL.createObjectURL(videoBlob);
//                         this.loading = false;
//                         this.showRecordAgain = true;
//                         this.isRecording = false;
//                     };
//                 } catch (error) {
//                     console.error("Error stopping recording:", error);
//                     alert('Could not stop recording. Please try again.');
//                     this.loading = false;
//                 }
//             },
//             async uploadToServer(videoBlob) {
//                 try {
//                     const randomNumber = Math.floor(Math.random() * 1000000);
//                     const fileName = `recorded-video-${randomNumber}.webm`; // Generate a name if needed
            
//                     const formData = new FormData();
//                     formData.append('file', videoBlob, fileName); // Attach the Blob directly
            
//                     const response = await fetch('/api/method/upload_file', {
//                         method: 'POST',
//                         body: formData,
//                         headers: {
//                             'X-Frappe-CSRF-Token': frappe.csrf_token
//                         }
//                     });
            
//                     if (!response.ok) {
//                         throw new Error('Failed to upload video: ' + await response.text());
//                     }
            
//                     const result = await response.json();
//                     return result.message.file_url;
//                 } catch (error) {
//                     console.error("Error uploading video:", error);
//                     throw error;
//                 }
//             }
//             ,
//             async attachVideo() {
//                 try {
//                     // Show loading screen
//                     this.loading = true;
            
//                     // Upload the video and get the file URL
//                     this.frappe_file_url = await this.uploadToServer(new Blob(this.recordedBlobs, { type: 'video/webm' }));
            
//                     if (!this.frappe_file_url) {
//                         throw new Error('Failed to upload the video to the server');
//                     }
            
//                     // Attach the file URL to the specific field in the Frappe document
//                     const doc = cur_frm.doc;
//                     doc[this.currentFieldName] = this.frappe_file_url; // Use the captured field name here
            
//                     await frappe.call({
//                         method: "frappe.desk.form.save.savedocs",
//                         args: {
//                             doc: doc,
//                             action: "Save"
//                         },
//                         callback: function(r) {
//                             if (!r.exc) {
//                                 frappe.show_alert({ message: 'Document updated with video attachment', indicator: 'green' });
//                                 cur_frm.reload_doc();
//                             } else {
//                                 throw new Error('Failed to save the document with the video URL');
//                             }
//                         }
//                     });
            
//                     // Hide the modal and stop the camera stream
//                     $('#videoRecorderModal').modal('hide');
//                     this.stream.getTracks().forEach(track => track.stop());
            
//                     // Clean up the modal backdrop and any other modals
//                     $('.modal-backdrop').remove();
//                     if (window.parent) {
//                         window.parent.$('.modal').modal('hide');
//                     }
            
//                     // Hide loading screen
//                     this.loading = false;
//                 } catch (error) {
//                     console.error("Error attaching video:", error);
//                     frappe.show_alert({ message: 'Video attachment failed', indicator: 'red' });
//                     this.loading = false; // Ensure loading screen is hidden in case of error
//                 }
//             }
//             ,
//             recordAgain() {
//                 this.initializeCamera(this.currentFacingMode);
//                 this.videoUrl = null;
//                 this.videoDuration = '';
//                 this.recordingTime = '00:00';
//                 this.showRecordAgain = false;
//                 this.$refs.videoPreview.controls = false;
//             },
//             switchCamera() {
//                 this.currentFacingMode = this.currentFacingMode === 'user' ? 'environment' : 'user';
//                 this.initializeCamera(this.currentFacingMode);
//             },
//             updateRecordingTime() {
//                 const elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
//                 const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
//                 const seconds = String(elapsedTime % 60).padStart(2, '0');
//                 this.recordingTime = `${minutes}:${seconds}`;
//             },
//             closeModal() {
//                 $('#videoRecorderModal').modal('hide');
//                 if (this.stream) {
//                     this.stream.getTracks().forEach(track => track.stop());
//                 }
//                 this.resetData();
//             },
//             resetData() {
//                 this.recordedBlobs = [];
//                 this.isRecording = false;
//                 this.videoUrl = null;
//                 this.recordingTime = '00:00';
//                 this.videoDuration = '';
//                 this.showRecordAgain = false;
//                 this.loading = false;
//             }
//         },
//         mounted() {
//             this.initializeCamera(this.currentFacingMode);
//         }
//     });
//     const appDiv = document.createElement('div');
//     appDiv.id = 'app';
//     document.body.appendChild(appDiv);

//     // Initialize the main Vue instance
//     const app = new Vue({
//         el: '#app',
//         template: `
//         <div>
//             <video-recorder ref="videoRecorder"></video-recorder>
//         </div>
//         `,
//         methods: {
//             openCameraModal() {
//                 console.log("Opening camera modal for field:", this.$refs.videoRecorder.currentFieldName);
//                 $('#videoRecorderModal').modal('show');
//             }
//         },
//     });

//     // Function to dynamically add a "Record Video" button next to file upload buttons
//     function addVideoButton() {
//         $('.btn-file-upload').each(function() {
//             if (!$(this).siblings('.btn-video-upload').length) {
//                 let video_btn = $('<button class="btn btn-video-upload"><i class="fa fa-video-camera"></i><span> Record Video</span></button>');
//                 $(this).after(video_btn);

//                 video_btn.on('click', function() {
//                     $('.modal-backdrop').remove();

//                     if (window.parent) {
//                         window.parent.$('.modal').modal('hide');
//                     }
//                     app.$refs.videoRecorder.currentFieldName = currentFieldName; // Set the current field name in the Vue component
//                     app.openCameraModal(); // Open the modal with the correct field name
//                 });
//             }
//         });
//     }
   
    

//     // Event listener for attach buttons
//     $(document).on('click', '.btn-attach', function() {
//         currentFieldName = $(this).data('fieldname'); // Store the field name globally
//     });

//     // Call addVideoButton when the DOM is ready
//     addVideoButton();

//     // Monitor DOM changes to dynamically add video buttons when new file upload buttons are added
//     $(document).on('DOMNodeInserted', function(e) {
//         if ($(e.target).hasClass('btn-file-upload') || $(e.target).find('.btn-file-upload').length) {
//             addVideoButton();
//         }
//     });
// }
