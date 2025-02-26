// Low-bandwidth mode logic
let lowBandwidthMode = false;

function toggleLowBandwidthMode() {
    lowBandwidthMode = !lowBandwidthMode;
    if (lowBandwidthMode) {
        // Reduce image quality, disable video streams, etc.
        alert('Low bandwidth mode enabled. Images and videos will be reduced in quality.');
        document.body.classList.add('low-bandwidth');
        applyLowBandwidthMode();
    } else {
        alert('Low bandwidth mode disabled. Images and videos will be displayed in normal quality.');
        document.body.classList.remove('low-bandwidth');
        restoreNormalMode();
    }
}

function applyLowBandwidthMode() {
    // Optimize images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (lowBandwidthMode) {
            img.setAttribute('data-src', img.src); // Store original source
            img.src = 'placeholder.png'; // Replace with a low-quality placeholder image
            img.loading = 'lazy'; // Enable lazy loading
        }
    });

    // Disable videos
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        if (lowBandwidthMode) {
            video.pause(); // Pause video
            video.style.display = 'none'; // Hide videos
        }
    });

    // Reduce font size and simplify styles
    document.body.style.fontSize = '14px';
    document.body.style.fontFamily = 'Arial, sans-serif';
}

function restoreNormalMode() {
    // Restore images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (img.hasAttribute('data-src')) {
            img.src = img.getAttribute('data-src'); // Restore original source
            img.removeAttribute('data-src');
            img.loading = 'auto'; // Disable lazy loading
        }
    });

    // Restore videos
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        video.style.display = 'block'; // Show videos
    });

    // Restore font size and styles
    document.body.style.fontSize = '16px';
    document.body.style.fontFamily = '';
}
