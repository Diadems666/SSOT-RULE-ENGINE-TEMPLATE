/**
 * End of Trade Application
 * Main JavaScript file containing common utility functions
 */

// Wait for document to fully load
document.addEventListener('DOMContentLoaded', function() {
    
    // Set up date-related elements
    setupDateElements();
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Set up the back-to-top button if it exists
    var backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        
        backToTopBtn.addEventListener('click', function() {
            document.body.scrollTop = 0; // For Safari
            document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
        });
    }
});

/**
 * Set up date-related elements such as highlighting the current date
 */
function setupDateElements() {
    // Format today's date
    var today = new Date();
    var todayStr = today.toLocaleDateString('en-AU', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
    });
    
    // Highlight elements with the data-date attribute matching today
    var dateElements = document.querySelectorAll('[data-date]');
    dateElements.forEach(function(el) {
        if (el.getAttribute('data-date') === todayStr) {
            el.classList.add('today');
        }
    });
}

/**
 * Format a number as Australian currency
 * @param {number} value - The numeric value to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(value) {
    if (value === undefined || value === null) {
        return '$0.00';
    }
    
    return '$' + parseFloat(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Calculate the total from an array of numeric values
 * @param {Array} values - Array of numeric values to sum
 * @returns {number} Total sum
 */
function calculateTotal(values) {
    return values.reduce(function(total, value) {
        if (typeof value === 'number' && !isNaN(value)) {
            return total + value;
        }
        return total;
    }, 0);
}

/**
 * Display a notification message to the user
 * @param {string} message - The message to display
 * @param {string} type - Message type ('success', 'error', 'warning', 'info')
 * @param {number} duration - How long to show the message in milliseconds
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Create notification container if it doesn't exist
    var container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.position = 'fixed';
        container.style.top = '10px';
        container.style.right = '10px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    // Create and style the notification
    var notification = document.createElement('div');
    notification.className = 'alert alert-' + type + ' alert-dismissible fade show';
    notification.role = 'alert';
    notification.innerHTML = message + 
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    
    // Add to container
    container.appendChild(notification);
    
    // Remove after duration
    setTimeout(function() {
        notification.classList.remove('show');
        setTimeout(function() {
            container.removeChild(notification);
        }, 150);
    }, duration);
} 