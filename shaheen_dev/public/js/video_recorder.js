document.addEventListener('DOMContentLoaded', function () {
    // Load Vue
    const vueScript = document.createElement('script');
    vueScript.src = 'https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js';
    document.head.appendChild(vueScript);

    vueScript.onload = function () {
        initializeVueApp();
    };
});

function initializeVueApp() {
    Vue.component('video-recorder', {
        template: `
        <div id="videoRecorderModal" class="modal fade" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Record Video</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="video-container">
                            <video ref="videoPreview" autoplay muted playsinline></video>
                            <div class="controls">
                                <button @click="switchCamera" class="button switch">🔄 Switch Camera</button>
                                <button @click="startRecording" class="button start" :disabled="isRecording">🔴 Start Recording</button>
                                <button @click="stopRecording" class="button stop" :disabled="!isRecording">⏹️ Stop Recording</button>
                                <button @click="recordAgain" class="button record-again" v-show="showRecordAgain">🔄 Record Again</button>
                            </div>
                            <a v-if="videoUrl" :href="videoUrl" download="recorded-video.mp4" class="download-link">⬇️ Download Video</a>
                            <div class="recording-time">{{ recordingTime }}</div>
                            <div class="video-duration" v-if="videoDuration">Duration: {{ videoDuration }}</div>
                            <div class="camera-mode-label">{{ cameraModeLabel }}</div>
                            <!-- This div is always present, but hidden unless loading is true -->
                            <div ref="loadingScreen" class="loading-screen" v-if="loading">Processing, please wait...</div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="attachVideo" :disabled="!videoUrl">Attach Video</button>
                    </div>
                </div>
            </div>
        </div>
        `,
        data() {
            return {
                stream: null,
                mediaRecorder: null,
                recordedBlobs: [],
                isRecording: false,
                videoUrl: null,
                recordingTime: '00:00',
                videoDuration: '',
                cameraModeLabel: 'Back Camera',
                currentFacingMode: 'environment',
                startTime: null,
                recordingTimeInterval: null,
                showRecordAgain: false,
                loading: false,
                currentFieldName: null, // The current field name to attach the video
            };
        },
        methods: {
            async initializeCamera(facingMode = 'environment') {
                try {
                    if (this.stream) {
                        this.stream.getTracks().forEach(track => track.stop());
                    }
                    this.stream = await navigator.mediaDevices.getUserMedia({
                        video: { facingMode: facingMode },
                        audio: true
                    });
                    this.$refs.videoPreview.srcObject = this.stream;
                    this.cameraModeLabel = facingMode === 'user' ? 'Front Camera' : 'Back Camera';
                } catch (error) {
                    console.error("Error accessing media devices.", error);
                    alert('Could not access camera and microphone. Please check your permissions.');
                }
            },
            startRecording() {
                try {
                    this.recordedBlobs = [];
                    this.mediaRecorder = new MediaRecorder(this.stream, {
                        mimeType: 'video/webm',
                        videoBitsPerSecond: 0.25 * 1000 * 1000
                    });
                    this.mediaRecorder.ondataavailable = (event) => {
                        if (event.data && event.data.size > 0) {
                            this.recordedBlobs.push(event.data);
                        }
                    };
                    this.mediaRecorder.start();
                    this.startTime = Date.now();
                    this.recordingTime = "00:00";
                    this.recordingTimeInterval = setInterval(this.updateRecordingTime, 1000);
                    this.isRecording = true;
                    this.showRecordAgain = false;
                } catch (error) {
                    console.error("Error starting recording:", error);
                    alert('Could not start recording. Please try again.');
                }
            },
            async stopRecording() {
                try {
                    this.mediaRecorder.stop();
                    clearInterval(this.recordingTimeInterval);
                    this.loading = true;

                    this.mediaRecorder.onstop = () => {
                        const videoBlob = new Blob(this.recordedBlobs, { type: 'video/webm' });
                        this.videoUrl = URL.createObjectURL(videoBlob);

                        this.$refs.videoPreview.srcObject = null;
                        this.$refs.videoPreview.src = this.videoUrl;
                        this.$refs.videoPreview.controls = true;
                        this.$refs.videoPreview.play();

                        const videoElement = document.createElement('video');
                        videoElement.src = this.videoUrl;
                        videoElement.addEventListener('loadedmetadata', () => {
                            const duration = videoElement.duration;
                            const minutes = String(Math.floor(duration / 60)).padStart(2, '0');
                            const seconds = String(Math.floor(duration % 60)).padStart(2, '0');
                            this.videoDuration = `Duration: ${minutes}:${seconds}`;
                        });

                        this.loading = false;
                        this.showRecordAgain = true;
                        this.isRecording = false;
                    };
                } catch (error) {
                    console.error("Error stopping recording:", error);
                    alert('Could not stop recording. Please try again.');
                }
            },
            async attachVideo() {
                try {
                    // Show loading screen
                    this.loading = true;

                    // Simulate delay for attachment process
                    setTimeout(async () => {
                        const fileURL = await this.uploadBlobToServer(new Blob(this.recordedBlobs, { type: 'video/webm' }), "recorded_video.mp4");

                        const doc = cur_frm.doc;
                        doc[this.currentFieldName] = fileURL; // Use the captured field name here

                        await frappe.call({
                            method: "frappe.desk.form.save.savedocs",
                            args: {
                                doc: doc,
                                action: "Save"
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.show_alert({ message: 'Document updated with video attachment', indicator: 'green' });
                                    cur_frm.reload_doc();
                                }
                            }
                        });

                        $('#videoRecorderModal').modal('hide');
                        $('#videoRecorderModal').remove();
                        this.stream.getTracks().forEach(track => track.stop());

                        $('.modal-backdrop').remove();

                        if (window.parent) {
                            window.parent.$('.modal').modal('hide');
                        }

                        // Hide loading screen
                        this.loading = false;
                    }, 3000); // Simulate a 3-second delay
                } catch (error) {
                    console.error("Error attaching video:", error);
                    frappe.show_alert({ message: 'Video attachment failed', indicator: 'red' });
                    this.loading = false; // Ensure loading screen is hidden in case of error
                }
            },
            recordAgain() {
                this.$refs.videoPreview.srcObject = this.stream;
                this.$refs.videoPreview.controls = false;
                this.$refs.videoPreview.play();
                this.recordingTime = "00:00";
                this.videoDuration = '';
                this.videoUrl = null;
                this.showRecordAgain = false;
            },
            switchCamera() {
                this.currentFacingMode = this.currentFacingMode === 'user' ? 'environment' : 'user';
                this.initializeCamera(this.currentFacingMode);
            },
            updateRecordingTime() {
                const elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
                const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
                const seconds = String(elapsedTime % 60).padStart(2, '0');
                this.recordingTime = `${minutes}:${seconds}`;
            },
            async uploadBlobToServer(blob, filename) {
                const formData = new FormData();
                formData.append('file', blob, filename);

                try {
                    const response = await fetch('/api/method/upload_file', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Frappe-CSRF-Token': frappe.csrf_token
                        }
                    });

                    if (!response.ok) {
                        throw new Error('Failed to upload video: ' + await response.text());
                    }

                    const result = await response.json();
                    return result.message.file_url;
                } catch (error) {
                    console.error("Error uploading video:", error);
                    throw error;
                }
            }
        },
        mounted() {
            this.initializeCamera(this.currentFacingMode);
        }
    });

    const appDiv = document.createElement('div');
    appDiv.id = 'app';
    document.body.appendChild(appDiv);

    // Initialize the main Vue instance
    const app = new Vue({
        el: '#app',
        template: `
        <div>
            <video-recorder ref="videoRecorder"></video-recorder>
        </div>
        `,
        methods: {
            openCameraModal() {
                $('#videoRecorderModal').modal('show');
            },
        },
    });

    // Function to dynamically add a "Record Video" button next to file upload buttons
    function addVideoButton() {
        $('.btn-file-upload').each(function() {
            if (!$(this).siblings('.btn-video-upload').length) {
                let video_btn = $('<button class="btn btn-video-upload"><i class="fa fa-video-camera"></i><span> Record Video</span></button>');
                $(this).after(video_btn);

                video_btn.on('click', function() {
                    $('.modal-backdrop').remove();

                    if (window.parent) {
                        window.parent.$('.modal').modal('hide');
                    }

                    app.$refs.videoRecorder.initializeCamera();  // Initialize the camera
                    app.openCameraModal(); // Open the modal
                });
            }
        });
    }

    // // Set currentFieldName when .btn-attach is clicked and open the camera modal
    // $(document).on('click', '.btn-attach', function() {
    //     app.$refs.videoRecorder.currentFieldName = $(this).data('fieldname'); // Set the current field name
    //     app.$refs.videoRecorder.initializeCamera(); // Initialize the camera
    //     app.openCameraModal(); // Open the modal
    // });

    // Call the function to add video buttons on page load
    addVideoButton();

    // Monitor DOM changes to dynamically add video buttons when new file upload buttons are added
    $(document).on('DOMNodeInserted', function(e) {
        if ($(e.target).hasClass('btn-file-upload') || $(e.target).find('.btn-file-upload').length) {
            addVideoButton();
        }
    });
}
