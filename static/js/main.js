// Main JavaScript for RunMix Generator

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize toast
var errorToast = new bootstrap.Toast(document.getElementById('errorToast'));

// Show error message
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorToast.show();
}

// Handle file upload
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const uploadProgress = document.getElementById('uploadProgress');
const uploadProgressBar = document.getElementById('uploadProgressBar');
const uploadStatus = document.getElementById('uploadStatus');

if (dropZone) {
    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('bg-light');
    }

    function unhighlight() {
        dropZone.classList.remove('bg-light');
    }

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    dropZone.addEventListener('click', () => fileInput.click());

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        fileInput.files = files;
        // Trigger form submission
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }
}

// Handle file input change
if (fileInput) {
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            // Show the upload form if it's hidden
            const modal = bootstrap.Modal.getInstance(document.getElementById('uploadModal'));
            if (modal) {
                modal.show();
            }
        }
    });
}

// Handle form submission
if (uploadForm) {
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const files = fileInput.files;
        
        if (files.length === 0) {
            showError('Please select at least one file to upload');
            return;
        }
        
        // Add all files to form data
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }
        
        // Show progress bar
        uploadProgress.style.display = 'block';
        uploadProgressBar.style.width = '0%';
        uploadStatus.textContent = 'Uploading...';
        
        // Upload files
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                uploadStatus.textContent = 'Upload complete!';
                uploadProgressBar.style.width = '100%';
                
                // Reload the page after a short delay to show the new files
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                throw new Error(data.message || 'Upload failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Upload failed: ' + (error.message || 'Unknown error'));
            uploadStatus.textContent = 'Upload failed';
        });
    });
}

// Handle Spotify import
const importSpotifyBtn = document.getElementById('importSpotify');
if (importSpotifyBtn) {
    importSpotifyBtn.addEventListener('click', function() {
        const spotifyUrl = document.getElementById('spotifyUrl').value.trim();
        
        if (!spotifyUrl) {
            showError('Please enter a Spotify playlist URL');
            return;
        }
        
        // Show loading state
        const originalText = importSpotifyBtn.innerHTML;
        importSpotifyBtn.disabled = true;
        importSpotifyBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Importing...';
        
        fetch('/spotify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ playlist_url: spotifyUrl })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'started') {
                showError('Import started. This may take a few minutes. The page will refresh when complete.');
                // Poll for completion
                pollForCompletion();
            } else {
                throw new Error(data.message || 'Import failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Import failed: ' + (error.message || 'Unknown error'));
        })
        .finally(() => {
            // Reset button state
            importSpotifyBtn.disabled = false;
            importSpotifyBtn.innerHTML = originalText;
        });
    });
}

function pollForCompletion() {
    // Reload the page after a delay to check for new files
    setTimeout(() => {
        window.location.reload();
    }, 10000); // Check every 10 seconds
}

// Handle RunMix generation
const generateForm = document.getElementById('generateForm');
if (generateForm) {
    generateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const day = document.getElementById('daySelect').value;
        const generateBtn = document.getElementById('generateBtn');
        const generationStatus = document.getElementById('generationStatus');
        const progressBar = document.getElementById('progressBar');
        const statusMessage = document.getElementById('statusMessage');
        const downloadSection = document.getElementById('downloadSection');
        const downloadLink = document.getElementById('downloadLink');
        
        // Show generation status
        generationStatus.style.display = 'block';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
        statusMessage.textContent = 'Starting generation...';
        downloadSection.style.display = 'none';
        
        // Disable generate button during generation
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
        
        // Start polling for status
        const checkInterval = setInterval(() => {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    // Update progress
                    progressBar.style.width = `${data.progress}%`;
                    progressBar.textContent = `${data.progress}%`;
                    statusMessage.textContent = data.message;
                    
                    // Check if generation is complete
                    if (!data.in_progress) {
                        clearInterval(checkInterval);
                        
                        if (data.error) {
                            showError(data.error);
                            generateBtn.disabled = false;
                            generateBtn.innerHTML = '<i class="bi-lightning-charge-fill me-2"></i>Try Again';
                        } else if (data.output_file) {
                            // Show download link
                            downloadLink.href = `/download/${data.output_file}`;
                            downloadSection.style.display = 'block';
                            generateBtn.disabled = false;
                            generateBtn.innerHTML = '<i class="bi-lightning-charge-fill me-2"></i>Generate Another';
                        }
                    }
                })
                .catch(error => {
                    console.error('Error checking status:', error);
                    showError('Error checking generation status');
                    clearInterval(checkInterval);
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = '<i class="bi-lightning-charge-fill me-2"></i>Try Again';
                });
        }, 1000); // Check every second
        
        // Start generation
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `day=${encodeURIComponent(day)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                throw new Error(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Generation failed: ' + (error.message || 'Unknown error'));
            clearInterval(checkInterval);
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="bi-lightning-charge-fill me-2"></i>Try Again';
        });
    });
}

// Initialize any dropdowns or other UI components
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
});
