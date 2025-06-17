document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatMessages = document.getElementById('chatMessages');
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');
    const toggleSidebarBtn = document.getElementById('toggleSidebar');
    const newConversationBtn = document.getElementById('newConversation');
    const newConversationMobileBtn = document.getElementById('newConversationMobile');
    const startNewConversationBtn = document.getElementById('startNewConversation');
    const chatSidebar = document.querySelector('.chat-sidebar');
    const conversationListItems = document.querySelectorAll('.conversation-list-item');
    const deleteConversationBtns = document.querySelectorAll('.delete-conversation');
    
    // Current conversation ID
    let currentConversationId = null;
    
    // Get conversation ID from URL if available
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('id')) {
        currentConversationId = urlParams.get('id');
    }
    
    // Initialize
    initializeChat();
    
    // Initialize chat
    function initializeChat() {
        // Auto-resize textarea
        if (messageInput) {
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        }
        
        // Scroll chat to bottom
        if (chatMessages) {
            scrollToBottom(chatMessages);
        }
        
        // Mobile sidebar toggle
        if (toggleSidebarBtn) {
            toggleSidebarBtn.addEventListener('click', function() {
                chatSidebar.classList.toggle('show');
            });
        }
        
        // New conversation buttons
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', createNewConversation);
        }
        
        if (newConversationMobileBtn) {
            newConversationMobileBtn.addEventListener('click', createNewConversation);
        }
        
        if (startNewConversationBtn) {
            startNewConversationBtn.addEventListener('click', createNewConversation);
        }
        
        // Message form submission
        if (messageForm) {
            messageForm.addEventListener('submit', function(e) {
                e.preventDefault();
                sendMessage();
            });
        }
        
        // Conversation list item click
        conversationListItems.forEach(item => {
            item.addEventListener('click', function() {
                const conversationId = this.getAttribute('data-id');
                window.location.href = `/chat?id=${conversationId}`;
            });
        });
        
        // Delete conversation button click
        deleteConversationBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const conversationId = this.getAttribute('data-id');
                deleteConversation(conversationId);
            });
        });
    }
    
    // Create new conversation
    function createNewConversation() {
        fetch('/api/conversations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to create new conversation');
            }
            return response.json();
        })
        .then(data => {
            window.location.href = `/chat?id=${data.id}`;
        })
        .catch(error => {
            console.error('Error creating conversation:', error);
            showErrorToast('Failed to create new conversation. Please try again.');
        });
    }
    
    // Delete conversation
    function deleteConversation(conversationId) {
        if (confirm("Are you sure you want to delete this conversation?")) {
            fetch(`/api/conversations/${conversationId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete conversation');
                }
                
                // Redirect to chat page without ID if we're deleting the current conversation
                if (currentConversationId === conversationId) {
                    window.location.href = '/chat';
                } else {
                    // Just remove the conversation from the list
                    const conversationElement = document.querySelector(`.conversation-list-item[data-id="${conversationId}"]`);
                    if (conversationElement) {
                        conversationElement.remove();
                    }
                }
            })
            .catch(error => {
                console.error('Error deleting conversation:', error);
                showErrorToast('Failed to delete conversation. Please try again.');
            });
        }
    }
    
    // Send message
    function sendMessage() {
        const messageContent = messageInput.value.trim();
        if (!messageContent) return;
        
        // Clear input and reset height
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Add message to UI
        addMessage(messageContent, true);
        
        // Create typing indicator
        const typingIndicator = createTypingIndicator();
        chatMessages.appendChild(typingIndicator);
        scrollToBottom(chatMessages);
        
        // Send to server
        fetch(`/api/conversations/${currentConversationId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: messageContent
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to send message');
            }
            return response.json();
        })
        .then(data => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add AI response
            addMessage(data.content, false);
            
            // Scroll to bottom
            scrollToBottom(chatMessages);
        })
        .catch(error => {
            console.error('Error sending message:', error);
            
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add error message
            addErrorMessage('Failed to get a response. Please try again.');
            
            // Scroll to bottom
            scrollToBottom(chatMessages);
        });
    }
    
    // Add message to UI
    function addMessage(content, isUser) {
        const message = document.createElement('div');
        message.className = `message ${isUser ? 'message-user' : 'message-ai'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        message.appendChild(messageContent);
        message.appendChild(messageTime);
        
        chatMessages.appendChild(message);
        scrollToBottom(chatMessages);
    }
    
    // Add error message to UI
    function addErrorMessage(content) {
        const message = document.createElement('div');
        message.className = 'message message-error';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content text-danger';
        messageContent.innerHTML = `<i class="fas fa-exclamation-circle me-2"></i>${content}`;
        
        message.appendChild(messageContent);
        chatMessages.appendChild(message);
    }
    
    // Helper function to scroll to bottom
    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }
});
