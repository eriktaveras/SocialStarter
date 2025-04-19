/**
 * SocialStarter Notifications JS
 * Handles real-time notifications using WebSockets
 */

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos DOM
    const notificationCounter = document.getElementById('notification-counter');
    const notificationBell = document.getElementById('notification-bell');
    const notificationDropdown = document.getElementById('notification-dropdown');
    const notificationList = document.getElementById('notification-list');
    
    // Contador para seguimiento del número actual de notificaciones
    let currentNotificationCount = 0;
    
    // WebSocket connection
    let notificationSocket = null;
    
    // Function to connect to WebSocket
    function connectWebSocket() {
        // Close any existing connection
        if (notificationSocket) {
            notificationSocket.close();
        }
        
        // Create WebSocket connection
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsPath = `${wsProtocol}//${window.location.host}/ws/notifications/`;
        
        notificationSocket = new WebSocket(wsPath);
        
        // Connection opened
        notificationSocket.onopen = function(e) {
            console.log('WebSocket connection established');
        };
        
        // Listen for messages
        notificationSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            if (data.type === 'notification_message') {
                // A new notification has arrived
                currentNotificationCount = data.count;
                updateNotificationCounter(data.count);
                
                // Add the new notification to the dropdown
                const notification = data.notification;
                addNotificationToDropdown(notification);
                
                // Show browser notification
                if (Notification.permission === 'granted') {
                    showBrowserNotification(notification);
                }
                
                // Play notification sound
                playNotificationSound();
            } else if (data.type === 'notification_count') {
                // Just updating the count
                currentNotificationCount = data.count;
                updateNotificationCounter(data.count);
            }
        };
        
        // Connection closed
        notificationSocket.onclose = function(e) {
            console.log('WebSocket connection closed');
            // Try to reconnect after 5 seconds
            setTimeout(connectWebSocket, 5000);
        };
        
        // Connection error
        notificationSocket.onerror = function(err) {
            console.error('WebSocket error:', err);
            notificationSocket.close();
        };
    }
    
    // Función para actualizar el contador visual de notificaciones
    function updateNotificationCounter(count) {
        if (notificationCounter) {
            if (count > 0) {
                notificationCounter.textContent = count > 99 ? '99+' : count;
                notificationCounter.classList.remove('hidden');
            } else {
                notificationCounter.classList.add('hidden');
            }
        }
    }
    
    // Function to add a new notification to the dropdown
    function addNotificationToDropdown(notification) {
        if (!notificationList) return;
        
        // Create notification item
        const item = document.createElement('a');
        item.href = notification.url || '#';
        item.className = 'block p-4 hover:bg-dark-light border-b border-gray-700 first:border-t border-gray-700';
        
        let iconClass = 'fas fa-bell';
        let iconColor = 'text-blue-500';
        
        switch (notification.type) {
            case 'like':
                iconClass = 'fas fa-heart';
                iconColor = 'text-red-500';
                break;
            case 'comment':
                iconClass = 'fas fa-comment';
                iconColor = 'text-blue-500';
                break;
            case 'follow':
                iconClass = 'fas fa-user-plus';
                iconColor = 'text-green-500';
                break;
            case 'message':
                iconClass = 'fas fa-envelope';
                iconColor = 'text-yellow-500';
                break;
        }
        
        item.innerHTML = `
            <div class="flex items-start space-x-3">
                <img src="${notification.sender_avatar || 'https://via.placeholder.com/150'}" 
                     class="w-8 h-8 rounded-full" alt="${notification.sender}">
                <div class="flex-1">
                    <p class="text-sm text-text-light">
                        <span class="font-semibold">${notification.sender}</span>
                        ${notification.text}
                    </p>
                    <span class="text-xs text-text-muted">${notification.created_at}</span>
                </div>
                <i class="${iconClass} ${iconColor}"></i>
            </div>
        `;
        
        item.addEventListener('click', function(e) {
            // Mark as read on click
            markNotificationAsRead(notification.id);
        });
        
        // Add to the top of the list
        const existingItems = notificationList.querySelectorAll('a');
        if (existingItems.length > 0) {
            notificationList.insertBefore(item, existingItems[0]);
        } else {
            notificationList.appendChild(item);
        }
        
        // Remove "No notifications" message if it exists
        const emptyMessage = notificationList.querySelector('.text-center');
        if (emptyMessage) {
            notificationList.removeChild(emptyMessage);
        }
    }
    
    // Function to mark a notification as read
    function markNotificationAsRead(notificationId) {
        if (notificationSocket && notificationSocket.readyState === WebSocket.OPEN) {
            notificationSocket.send(JSON.stringify({
                type: 'mark_as_read',
                notification_id: notificationId
            }));
        } else {
            // Fallback to traditional AJAX if WebSocket is not available
            fetch(`/notifications/mark-as-read/${notificationId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).catch(err => console.error('Error marking notification as read:', err));
        }
    }
    
    // Function to mark all notifications as read
    function markAllAsRead() {
        if (notificationSocket && notificationSocket.readyState === WebSocket.OPEN) {
            notificationSocket.send(JSON.stringify({
                type: 'mark_as_read'
            }));
        } else {
            // Fallback to traditional AJAX if WebSocket is not available
            fetch('/notifications/mark-as-read/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(() => {
                // Update UI
                currentNotificationCount = 0;
                updateNotificationCounter(0);
            })
            .catch(err => console.error('Error marking all as read:', err));
        }
    }
    
    // Función para mostrar notificaciones del navegador
    function showBrowserNotification(notification) {
        if (!notification) return;
        
        const title = 'SocialStarter';
        const options = {
            body: `${notification.sender}: ${notification.text}`,
            icon: notification.sender_avatar || '/static/img/logo.png'
        };
        
        const browserNotification = new Notification(title, options);
        
        browserNotification.onclick = function() {
            window.open(notification.url || window.location.origin, '_blank');
        };
    }
    
    // Función para reproducir sonido de notificación
    function playNotificationSound() {
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.play().catch(err => console.log('Error playing notification sound'));
    }
    
    // Solicitar permiso para notificaciones del navegador
    function requestNotificationPermission() {
        if (Notification && Notification.permission !== 'granted' && Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }
    
    // Initial setup
    if (notificationBell) {
        notificationBell.addEventListener('click', function() {
            // Mark all as read when opening the dropdown
            if (currentNotificationCount > 0) {
                markAllAsRead();
            }
        });
    }
    
    // Only connect if user is authenticated (check if notification elements exist)
    if (notificationCounter || notificationBell) {
        requestNotificationPermission();
        connectWebSocket();
    }
}); 