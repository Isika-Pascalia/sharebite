// ShareBite JavaScript Functionality

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('ShareBite app loaded successfully!');
    
    // Initialize search functionality
    initializeSearch();
});

// Search and Filter Functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', filterFood);
    }
}

function filterFood() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const foodCards = document.querySelectorAll('.food-card');
    const noResults = document.getElementById('noResults');
    let visibleCount = 0;
    
    foodCards.forEach(card => {
        const foodName = card.getAttribute('data-food-name') || '';
        const location = card.getAttribute('data-location') || '';
        
        // Check if search term matches food name or location
        const isMatch = foodName.includes(searchTerm) || location.includes(searchTerm);
        
        if (isMatch) {
            card.style.display = 'block';
            card.style.animation = 'slideIn 0.3s ease-out';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide "no results" message
    if (noResults) {
        noResults.style.display = visibleCount === 0 && searchTerm !== '' ? 'block' : 'none';
    }
}

function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = '';
        filterFood(); // Reset the filter
    }
}

// Claim Food Functionality
function claimFood(foodId) {
    const claimBtn = document.getElementById(`claim-btn-${foodId}`);
    
    if (!claimBtn || claimBtn.disabled) {
        return;
    }
    
    // Disable button and show loading state
    claimBtn.disabled = true;
    claimBtn.textContent = 'Claiming...';
    claimBtn.classList.add('loading');
    
    // Send claim request to server
    fetch(`/claim/${foodId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Success - update button and card appearance
            claimBtn.textContent = 'Claimed!';
            claimBtn.classList.remove('loading');
            claimBtn.classList.add('claimed');
            
            // Mark the entire card as claimed
            const card = claimBtn.closest('.food-card');
            card.classList.add('claimed-card');
            
            // Show success message
            showNotification('Food claimed successfully! Contact the donor to arrange pickup.', 'success');
            
            // Remove the card after a short delay
            setTimeout(() => {
                card.style.animation = 'slideOut 0.3s ease-in';
                setTimeout(() => {
                    card.remove();
                    // Check if no cards remain
                    checkEmptyState();
                }, 300);
            }, 2000);
            
        } else {
            // Error - reset button
            claimBtn.disabled = false;
            claimBtn.textContent = 'Claim This Food';
            claimBtn.classList.remove('loading');
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error claiming food:', error);
        claimBtn.disabled = false;
        claimBtn.textContent = 'Claim This Food';
        claimBtn.classList.remove('loading');
        showNotification('Error claiming food. Please try again.', 'error');
    });
}

// Check if no food cards remain and show empty state
function checkEmptyState() {
    const foodContainer = document.getElementById('foodContainer');
    const visibleCards = foodContainer.querySelectorAll('.food-card:not([style*="display: none"])');
    
    if (visibleCards.length === 0) {
        foodContainer.innerHTML = `
            <div class="no-food">
                <p>No food donations available at the moment.</p>
                <a href="/donate" class="donate-link">Be the first to donate!</a>
            </div>
        `;
    }
}

// Show notification messages
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `flash flash-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.animation = 'slideIn 0.3s ease-out';
    notification.style.maxWidth = '350px';
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Form validation for donation form
function validateDonationForm() {
    const form = document.querySelector('.donate-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const foodName = document.getElementById('food_name').value.trim();
        const quantity = document.getElementById('quantity').value.trim();
        const location = document.getElementById('location').value.trim();
        const contactInfo = document.getElementById('contact_info').value.trim();
        
        if (!foodName || !quantity || !location || !contactInfo) {
            e.preventDefault();
            showNotification('Please fill in all fields.', 'error');
            return false;
        }
        
        if (foodName.length < 3) {
            e.preventDefault();
            showNotification('Food name must be at least 3 characters long.', 'error');
            return false;
        }
        
        return true;
    });
}

// Initialize donation form validation when page loads
document.addEventListener('DOMContentLoaded', validateDonationForm);

// Add slideOut animation for CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);