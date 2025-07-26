// Chat functionality for #GPT

let isLoading = false;

// Initialize chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    
    // Handle Enter key in message input
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-focus message input
    messageInput.focus();
    
    // Auto-scroll to bottom on page load
    scrollToBottom();
});

// Send message function
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const message = messageInput.value.trim();
    
    if (!message || isLoading) {
        return;
    }
    
    // Set loading state
    isLoading = true;
    messageInput.disabled = true;
    sendButton.disabled = true;
    sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Clear input
    messageInput.value = '';
    
    // Add user message to chat
    addUserMessage(message);
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        if (response.ok && data.success) {
            // Add assistant response
            addAssistantMessage(data.assistant_response);
            
            // Update the user message with redaction info if any
            if (data.redactions && data.redactions.length > 0) {
                updateUserMessageWithRedactions(data.redactions);
            }
        } else {
            // Handle error
            const errorMessage = data.error || 'An error occurred while processing your message.';
            addErrorMessage(errorMessage);
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addErrorMessage('Network error. Please check your connection and try again.');
    } finally {
        // Reset loading state
        isLoading = false;
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        messageInput.focus();
    }
}

// Add user message to chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <i class="fas fa-user"></i> You
            </div>
            <div class="message-text">${escapeHtml(message)}</div>
            <div class="redaction-placeholder"></div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add assistant message to chat
function addAssistantMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <i class="fas fa-robot"></i> Assistant
            </div>
            <div class="message-text">${escapeHtml(message)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add error message to chat
function addErrorMessage(errorText) {
    const chatMessages = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message';
    messageDiv.innerHTML = `
        <div class="message-content error-message">
            <div class="message-header">
                <i class="fas fa-exclamation-triangle"></i> Error
            </div>
            <div class="message-text">${escapeHtml(errorText)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Update user message with redaction info
function updateUserMessageWithRedactions(redactions) {
    const chatMessages = document.getElementById('chat-messages');
    const userMessages = chatMessages.querySelectorAll('.user-message');
    const lastUserMessage = userMessages[userMessages.length - 1];
    
    if (lastUserMessage && redactions.length > 0) {
        const placeholder = lastUserMessage.querySelector('.redaction-placeholder');
        if (placeholder) {
            const redactionTypes = redactions.map(r => r.type);
            const uniqueTypes = [...new Set(redactionTypes)];
            
            const badgesHtml = uniqueTypes.map(type => 
                `<span class="badge bg-warning text-dark">${type}</span>`
            ).join(' ');
            
            placeholder.innerHTML = `
                <div class="redaction-info">
                    <i class="fas fa-shield-alt text-warning"></i>
                    <small>PII detected and replaced with synthetic values: ${badgesHtml}</small>
                </div>
            `;
        }
    }
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    typingIndicator.style.display = 'none';
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Clear chat function
async function clearChat() {
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    try {
        const response = await fetch('/clear_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Clear chat messages
            const chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="text-center text-muted">
                        <i class="fas fa-comments fa-3x mb-3"></i>
                        <h4>Chat Cleared</h4>
                        <p>Your messages have been cleared. Start a new conversation!</p>
                    </div>
                </div>
            `;
            
            // Focus input
            document.getElementById('message-input').focus();
        } else {
            showError('Failed to clear chat history');
        }
        
    } catch (error) {
        console.error('Error clearing chat:', error);
        showError('Network error while clearing chat');
    }
}

// Show error modal
function showError(message) {
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    document.getElementById('error-message').textContent = message;
    errorModal.show();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Handle connection errors and redirect
window.addEventListener('beforeunload', function() {
    // Optional: Add cleanup code here
});

// Auto-resize textarea (if needed for future enhancements)
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}
