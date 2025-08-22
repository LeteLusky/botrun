// Discord Bot Runner JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeTokenToggle();
    initializeFormValidation();
    initializeStatusUpdater();
});

function initializeTokenToggle() {
    const toggleButton = document.getElementById('toggle-token');
    const tokenInput = document.getElementById('token');
    
    if (toggleButton && tokenInput) {
        toggleButton.addEventListener('click', function() {
            const isPassword = tokenInput.type === 'password';
            tokenInput.type = isPassword ? 'text' : 'password';
            
            const icon = toggleButton.querySelector('i');
            icon.className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
        });
    }
}

function initializeFormValidation() {
    const form = document.getElementById('token-form');
    const tokenInput = document.getElementById('token');
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (form && tokenInput && submitButton) {
        // Real-time token validation
        tokenInput.addEventListener('input', function() {
            const token = this.value.trim();
            const isValid = validateToken(token);
            
            // Update input styling
            if (token.length === 0) {
                this.classList.remove('is-valid', 'is-invalid');
            } else if (isValid) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            }
            
            // Update submit button
            submitButton.disabled = !isValid && token.length > 0;
        });
        
        // Form submission handling
        form.addEventListener('submit', function(e) {
            const token = tokenInput.value.trim();
            
            if (!validateToken(token)) {
                e.preventDefault();
                showAlert('Please enter a valid Discord bot token', 'error');
                return;
            }
            
            // Add loading state
            submitButton.classList.add('loading');
            submitButton.disabled = true;
            
            // Show loading message
            showAlert('Starting bot... This may take a few seconds.', 'info');
        });
    }
}

function initializeStatusUpdater() {
    // Update bot status every 10 seconds
    setInterval(updateBotStatus, 10000);
}

function validateToken(token) {
    // Basic Discord token validation
    if (!token || typeof token !== 'string') return false;
    
    // Discord tokens are typically 59+ characters long
    if (token.length < 50) return false;
    
    // Discord tokens should not contain spaces
    if (token.includes(' ')) return false;
    
    // Basic format check (should contain dots for JWT-like structure)
    const parts = token.split('.');
    if (parts.length < 2) return false;
    
    return true;
}

function stopBot() {
    if (confirm('Are you sure you want to stop the bot?')) {
        const stopForm = document.getElementById('stop-form');
        if (stopForm) {
            showAlert('Stopping bot...', 'info');
            stopForm.submit();
        }
    }
}

function updateBotStatus() {
    fetch('/bot_status')
        .then(response => response.json())
        .then(data => {
            updateStatusDisplay(data);
        })
        .catch(error => {
            console.error('Error fetching bot status:', error);
        });
}

function updateStatusDisplay(status) {
    const statusCard = document.getElementById('status-card');
    const statusBadge = statusCard.querySelector('.status-badge');
    const cardBody = statusCard.querySelector('.card-body');
    
    if (statusBadge) {
        // Update badge
        statusBadge.className = `badge bg-${status.running ? 'success' : 'secondary'} status-badge`;
        statusBadge.innerHTML = `<i class="fas fa-circle pulse me-1" style="font-size: 0.7em;"></i>${status.running ? 'Running' : 'Stopped'}`;
        
        // Update card body content
        if (status.running && status.info && Object.keys(status.info).length > 0) {
            cardBody.innerHTML = `
                <div class="row g-3">
                    <div class="col-md-6">
                        <small class="text-muted">Bot Name</small>
                        <div class="fw-bold">${status.info.name || 'Unknown'}</div>
                    </div>
                    <div class="col-md-6">
                        <small class="text-muted">Bot ID</small>
                        <div class="fw-bold font-monospace">${status.info.id || 'Unknown'}</div>
                    </div>
                    <div class="col-md-6">
                        <small class="text-muted">Servers</small>
                        <div class="fw-bold">${status.info.guilds || 0}</div>
                    </div>
                    <div class="col-md-6">
                        <small class="text-muted">Total Users</small>
                        <div class="fw-bold">${status.info.users || 0}</div>
                    </div>
                </div>
            `;
        } else {
            cardBody.innerHTML = `
                <p class="text-muted mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    No bot is currently running. Enter a token below to get started.
                </p>
            `;
        }
    }
    
    // Update form state
    const tokenInput = document.getElementById('token');
    const toggleButton = document.getElementById('toggle-token');
    const form = document.getElementById('token-form');
    
    if (tokenInput && toggleButton && form) {
        const isRunning = status.running;
        tokenInput.disabled = isRunning;
        toggleButton.disabled = isRunning;
        
        // Update form buttons
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            if (isRunning) {
                submitButton.innerHTML = '<i class="fas fa-stop me-2"></i>Stop Bot';
                submitButton.className = 'btn btn-danger';
                submitButton.type = 'button';
                submitButton.onclick = stopBot;
            } else {
                submitButton.innerHTML = '<i class="fas fa-play me-2"></i>Start Bot';
                submitButton.className = 'btn btn-primary';
                submitButton.type = 'submit';
                submitButton.onclick = null;
            }
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
        }
    }
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : (type === 'warning' ? 'warning' : (type === 'info' ? 'info' : 'success'))} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    const icon = type === 'error' ? 'exclamation-triangle' : 
                 type === 'warning' ? 'exclamation-circle' : 
                 type === 'info' ? 'info-circle' : 'check-circle';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main container
    const container = document.querySelector('.container .col-lg-8');
    const firstCard = container.querySelector('.card');
    if (firstCard) {
        container.insertBefore(alertDiv, firstCard);
    } else {
        container.appendChild(alertDiv);
    }
    
    // Auto-dismiss after 5 seconds
    if (type === 'info') {
        setTimeout(() => {
            const alert = bootstrap.Alert.getInstance(alertDiv);
            if (alert) {
                alert.close();
            }
        }, 5000);
    }
}

// Utility functions for better UX
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        return new Promise((resolve, reject) => {
            document.execCommand('copy') ? resolve() : reject();
            textArea.remove();
        });
    }
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, update status
        updateBotStatus();
    }
});
