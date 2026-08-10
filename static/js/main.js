// ============================================================
// SmartCurriculum - Main JavaScript
// SIH 2026
// ============================================================

// Theme Management
const getStoredTheme = () => localStorage.getItem('theme') || 'dark';
const setStoredTheme = (theme) => localStorage.setItem('theme', theme);

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

function toggleTheme() {
    const current = getStoredTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    setStoredTheme(next);
    applyTheme(next);
}

// Apply theme on load
applyTheme(getStoredTheme());

// Sidebar Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    if (window.innerWidth <= 992) {
        sidebar.classList.toggle('mobile-open');
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            overlay.onclick = () => {
                sidebar.classList.remove('mobile-open');
                overlay.classList.remove('active');
            };
            document.body.appendChild(overlay);
        }
        overlay.classList.toggle('active', sidebar.classList.contains('mobile-open'));
    } else {
        sidebar.classList.toggle('collapsed');
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.marginLeft = sidebar.classList.contains('collapsed') ? '70px' : '260px';
        }
    }
}

// Live Clock
function updateClock() {
    const el = document.getElementById('topbarTime');
    if (!el) return;
    const now = new Date();
    el.textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
setInterval(updateClock, 1000);
updateClock();

// Animate stat cards on load
function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.getAttribute('data-count'));
        const duration = 1500;
        const start = performance.now();
        const animate = (time) => {
            const elapsed = time - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target);
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    });
}

// Animate progress bars
function animateProgressBars() {
    document.querySelectorAll('[data-progress]').forEach(bar => {
        const target = parseFloat(bar.getAttribute('data-progress'));
        setTimeout(() => { bar.style.width = target + '%'; }, 200);
    });
}

// Toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    toast.style.cssText = `
        position: fixed; bottom: 24px; right: 24px;
        background: var(--bg-card); border: 1px solid var(--border-color);
        border-left: 4px solid ${type === 'success' ? 'var(--accent-success)' : 'var(--accent-danger)'};
        color: var(--text-primary); padding: 14px 20px;
        border-radius: 12px; display: flex; align-items: center; gap: 10px;
        box-shadow: var(--shadow-lg); z-index: 9999;
        animation: fadeInUp 0.3s ease forwards; font-size: 14px; font-weight: 500;
        max-width: 360px;
    `;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3500);
}

// QR Code Scanner using jsQR
let scannerActive = false;
let videoStream = null;

function startQRScanner() {
    const scanBtn = document.getElementById('scanBtn');
    const video = document.getElementById('qrVideo');
    const canvas = document.getElementById('qrCanvas');
    const status = document.getElementById('scanStatus');

    if (!video) return;

    if (scannerActive) {
        stopQRScanner();
        return;
    }

    scannerActive = true;
    if (scanBtn) {
        scanBtn.innerHTML = '<i class="fas fa-stop-circle"></i> Stop Scanner';
        scanBtn.classList.add('btn-danger-grad');
        scanBtn.classList.remove('btn-primary-grad');
    }
    if (status) status.textContent = 'Initializing camera...';

    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            videoStream = stream;
            video.srcObject = stream;
            video.play();
            video.style.display = 'block';
            if (status) status.textContent = 'Point camera at QR code';
            requestAnimationFrame(() => scanFrame(video, canvas, status));
        })
        .catch(err => {
            if (status) status.textContent = 'Camera access denied. Use manual input.';
            console.error('Camera error:', err);
            scannerActive = false;
        });
}

function scanFrame(video, canvas, status) {
    if (!scannerActive || !video.readyState === video.HAVE_ENOUGH_DATA) {
        if (scannerActive) requestAnimationFrame(() => scanFrame(video, canvas, status));
        return;
    }

    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    try {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        if (typeof jsQR !== 'undefined') {
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            if (code) {
                stopQRScanner();
                submitAttendance(code.data, status);
                return;
            }
        }
    } catch(e) {}

    if (scannerActive) requestAnimationFrame(() => scanFrame(video, canvas, status));
}

function stopQRScanner() {
    scannerActive = false;
    if (videoStream) {
        videoStream.getTracks().forEach(t => t.stop());
        videoStream = null;
    }
    const video = document.getElementById('qrVideo');
    if (video) video.style.display = 'none';
    const scanBtn = document.getElementById('scanBtn');
    if (scanBtn) {
        scanBtn.innerHTML = '<i class="fas fa-camera"></i> Start Camera';
        scanBtn.classList.remove('btn-danger-grad');
        scanBtn.classList.add('btn-primary-grad');
    }
}

// Drag & Drop / File Upload QR Image scan
function handleQRDrop(e) {
    e.preventDefault();
    const zone = document.getElementById('dropZone');
    if (zone) {
        zone.style.borderColor = 'var(--border-color)';
        zone.style.background = 'rgba(255,255,255,0.02)';
    }
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        scanQRImage(files[0]);
    }
}

function handleQRFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        scanQRImage(files[0]);
    }
}

function scanQRImage(file) {
    const status = document.getElementById('scanStatus');
    if (status) status.textContent = 'Processing image...';
    
    if (!file.type.startsWith('image/')) {
        showToast('Please upload an image file.', 'error');
        if (status) status.textContent = 'Invalid file type.';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            
            try {
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                if (typeof jsQR !== 'undefined') {
                    const code = jsQR(imageData.data, imageData.width, imageData.height);
                    if (code) {
                        submitAttendance(code.data, status);
                    } else {
                        showToast('No QR code found in this image.', 'error');
                        if (status) status.textContent = 'Scanning failed. Try another image.';
                    }
                } else {
                    showToast('QR scanning library not loaded yet.', 'error');
                }
            } catch (err) {
                console.error(err);
                showToast('Error reading image data.', 'error');
            }
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
}

// Copy Share Link Helper
function copyShareLink() {
    const input = document.getElementById('shareLink');
    if (!input) return;
    input.select();
    input.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(input.value)
        .then(() => {
            showToast('Share link copied to clipboard!', 'success');
            const icon = document.getElementById('copyIcon');
            if (icon) {
                icon.className = 'fas fa-check';
                setTimeout(() => { icon.className = 'fas fa-copy'; }, 2000);
            }
        })
        .catch(() => {
            showToast('Failed to copy. Copy manually.', 'error');
        });
}

function submitAttendance(sessionData, statusEl) {
    if (statusEl) statusEl.textContent = 'Processing...';
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');

    fetch('/attendance/mark/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams({ session_id: sessionData })
    })
    .then(r => r.json())
    .then(data => {
        if (statusEl) statusEl.textContent = data.message;
        showToast(data.message, data.success ? 'success' : 'error');
        if (data.success) {
            document.getElementById('successOverlay')?.classList.remove('d-none');
        }
    })
    .catch(() => {
        showToast('Network error. Try again.', 'error');
    });
}

function submitManualQR() {
    const input = document.getElementById('manualQRInput');
    if (!input || !input.value.trim()) {
        showToast('Please enter QR code data.', 'error');
        return;
    }
    const status = document.getElementById('scanStatus');
    submitAttendance(input.value.trim(), status);
}

// Countdown timer for QR sessions
function startCountdown(expiresAt) {
    const el = document.getElementById('sessionCountdown');
    if (!el) return;

    function update() {
        const now = new Date().getTime();
        const expires = new Date(expiresAt).getTime();
        const diff = expires - now;

        if (diff <= 0) {
            el.innerHTML = '<span class="text-danger">Session Expired</span>';
            return;
        }

        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        el.innerHTML = `<span class="${diff < 60000 ? 'text-danger' : 'text-warning'}">${minutes}m ${seconds}s remaining</span>`;
        setTimeout(update, 1000);
    }
    update();
}

// Auto-refresh session status
function autoRefreshSession(sessionId) {
    setInterval(() => {
        fetch(`/api/session/${sessionId}/status/`)
            .then(r => r.json())
            .then(data => {
                const countEl = document.getElementById('liveCount');
                if (countEl) countEl.textContent = data.present_count;
            });
    }, 5000);
}

// Chart utilities
function createDonutChart(canvas, value, max, colors) {
    if (!canvas) return;
    const pct = max > 0 ? (value / max) * 100 : 0;
    return new Chart(canvas, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, max - value],
                backgroundColor: colors || ['#6c63ff', 'rgba(255,255,255,0.05)'],
                borderWidth: 0,
                hoverOffset: 4,
            }]
        },
        options: {
            cutout: '75%',
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
            animation: { duration: 1200, easing: 'easeInOutQuart' },
        }
    });
}

function createLineChart(canvas, labels, data, label) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(108, 99, 255, 0.3)');
    gradient.addColorStop(1, 'rgba(108, 99, 255, 0)');

    return new Chart(canvas, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label,
                data,
                borderColor: '#6c63ff',
                backgroundColor: gradient,
                borderWidth: 2.5,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#6c63ff',
                pointRadius: 4,
                pointHoverRadius: 7,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(18,18,42,0.95)',
                    borderColor: 'rgba(108,99,255,0.3)',
                    borderWidth: 1,
                    titleColor: '#f0f0ff',
                    bodyColor: '#a0a0c0',
                    padding: 12,
                }
            },
            scales: {
                x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#606080', maxTicksLimit: 7 } },
                y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#606080' }, min: 0, max: 100 }
            },
            animation: { duration: 1500, easing: 'easeInOutQuart' }
        }
    });
}

function createBarChart(canvas, labels, data) {
    if (!canvas) return;
    return new Chart(canvas, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Attendance %',
                data,
                backgroundColor: data.map(v => v >= 75 ? 'rgba(0,230,118,0.7)' : v >= 60 ? 'rgba(255,215,64,0.7)' : 'rgba(255,82,82,0.7)'),
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(18,18,42,0.95)',
                    borderColor: 'rgba(108,99,255,0.3)',
                    borderWidth: 1,
                    titleColor: '#f0f0ff',
                    bodyColor: '#a0a0c0',
                    padding: 12,
                }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#606080' } },
                y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#606080' }, min: 0, max: 100 }
            },
            animation: { duration: 1200, easing: 'easeInOutQuart' }
        }
    });
}

// Cookie utility
function getCookie(name) {
    let value = '; ' + document.cookie;
    let parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    animateCounters();
    animateProgressBars();

    // Auto-dismiss alerts
    document.querySelectorAll('.custom-alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Add stagger animation to cards
    document.querySelectorAll('.stat-card, .card-premium').forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.4s ease ${i * 0.08}s, transform 0.4s ease ${i * 0.08}s`;
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 50);
    });
});
