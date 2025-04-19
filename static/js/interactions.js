/**
 * SocialStarter Interactions JS
 * Handles AJAX interactions for posts including likes, comments, etc.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Setup like button handlers
    setupLikeButtons();
    
    // Setup tab switching for profile page
    setupProfileTabs();
});

/**
 * Set up click handlers for all like buttons on the page
 */
function setupLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const postId = this.dataset.postId;
            const likeUrl = this.getAttribute('href');
            const likeCountElement = this.querySelector('.like-count');
            const likeIcon = this.querySelector('i');
            
            // Send AJAX request
            fetch(likeUrl, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the like count
                    likeCountElement.textContent = data.likes_count;
                    
                    // Update the like icon
                    if (data.liked) {
                        likeIcon.classList.remove('far');
                        likeIcon.classList.add('fas');
                        likeIcon.classList.add('text-red-500');
                    } else {
                        likeIcon.classList.remove('fas');
                        likeIcon.classList.remove('text-red-500');
                        likeIcon.classList.add('far');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
}

/**
 * Setup tabs functionality on profile page
 */
function setupProfileTabs() {
    const profileTabs = document.querySelector('[x-data="{ activeTab: \'posts\' }"]');
    
    // If we're on the profile page with tabs
    if (profileTabs) {
        // Find the Likes tab button
        const likesTabButton = Array.from(profileTabs.querySelectorAll('button'))
            .find(btn => btn.textContent.trim() === 'Likes');
        
        if (likesTabButton) {
            // When likes tab is clicked, load liked posts if needed
            likesTabButton.addEventListener('click', function() {
                const likesTabContent = document.querySelector('[x-show="activeTab === \'likes\'"]');
                
                // Check if we've already loaded the content
                if (likesTabContent && !likesTabContent.querySelector('.post-card')) {
                    const username = window.location.pathname.split('/').filter(Boolean).pop();
                    
                    // Display loading state
                    likesTabContent.innerHTML = `
                        <div class="text-center py-10">
                            <div class="mb-4">
                                <i class="fas fa-spinner fa-spin text-5xl text-text-muted"></i>
                            </div>
                            <h3 class="text-xl font-bold mb-2">Loading liked posts...</h3>
                        </div>
                    `;
                    
                    // Fetch liked posts via AJAX
                    fetch(`/interactions/ajax/liked-posts/${username}/`, {
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Update the content
                        likesTabContent.innerHTML = data.html;
                        
                        // Re-setup like buttons for the newly added content
                        setupLikeButtons();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        likesTabContent.innerHTML = `
                            <div class="text-center py-10">
                                <div class="mb-4">
                                    <i class="fas fa-exclamation-triangle text-5xl text-red-500 opacity-40"></i>
                                </div>
                                <h3 class="text-xl font-bold mb-2">Error loading liked posts</h3>
                                <p class="text-text-muted">Please try again later.</p>
                            </div>
                        `;
                    });
                }
            });
        }
    }
} 