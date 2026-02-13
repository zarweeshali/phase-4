// Phase 4 AI Chatbot Frontend JavaScript
// Stateless client-side interface for Phase 4 AI Todo Assistant

class Phase4Chatbot {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userId = localStorage.getItem('userId');
        this.userEmail = localStorage.getItem('userEmail');
        this.currentConversationId = null;
        this.init();
    }

    init() {
        // Authentication elements
        this.loginForm = document.getElementById('login-form');
        this.signupForm = document.getElementById('signup-form');
        this.logoutSection = document.getElementById('logout-section');
        this.authToggle = document.getElementById('auth-toggle');
        
        // Chat elements
        this.chatSection = document.getElementById('chat-section');
        this.messagesContainer = document.getElementById('messages-container');
        this.messageInput = document.getElementById('message-input');
        
        // Auth buttons
        document.getElementById('show-login').addEventListener('click', () => this.showLoginForm());
        document.getElementById('show-signup').addEventListener('click', () => this.showSignupForm());
        document.getElementById('login-btn').addEventListener('click', () => this.login());
        document.getElementById('signup-btn').addEventListener('click', () => this.signup());
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
        
        // Chat buttons
        document.getElementById('send-message').addEventListener('click', () => this.sendMessage());
        
        // Allow Enter key to submit forms
        document.getElementById('login-password').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.login();
        });
        
        document.getElementById('signup-password').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.signup();
        });
        
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        // Check if user is already logged in
        if (this.token) {
            this.showLoggedInView();
        } else {
            this.showAuthView();
        }
    }

    showLoginForm() {
        document.getElementById('show-login').classList.add('active');
        document.getElementById('show-signup').classList.remove('active');
        this.loginForm.classList.remove('hidden');
        this.signupForm.classList.add('hidden');
    }

    showSignupForm() {
        document.getElementById('show-signup').classList.add('active');
        document.getElementById('show-login').classList.remove('active');
        this.signupForm.classList.remove('hidden');
        this.loginForm.classList.add('hidden');
    }

    async signup() {
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value;

        if (!email || !password) {
            this.showMessage('Please enter both email and password', 'error');
            return;
        }

        try {
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Signup failed');
            }

            this.showMessage('Account created successfully! Please log in.', 'success');

            // Switch to login form
            this.showLoginForm();
            
            // Clear signup form
            document.getElementById('signup-email').value = '';
            document.getElementById('signup-password').value = '';

        } catch (error) {
            console.error('Error signing up:', error);
            this.showMessage('Signup failed: ' + error.message, 'error');
        }
    }

    async login() {
        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;

        if (!email || !password) {
            this.showMessage('Please enter both email and password', 'error');
            return;
        }

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            // Store token and user info
            this.token = data.access_token;
            this.userId = data.user_id;
            this.userEmail = data.email;
            
            localStorage.setItem('token', this.token);
            localStorage.setItem('userId', this.userId);
            localStorage.setItem('userEmail', this.userEmail);

            this.showMessage('Login successful!', 'success');
            
            // Show logged in view
            this.showLoggedInView();
        } catch (error) {
            console.error('Error logging in:', error);
            this.showMessage('Login failed: ' + error.message, 'error');
        }
    }

    logout() {
        // Clear stored data
        this.token = null;
        this.userId = null;
        this.userEmail = null;
        this.currentConversationId = null;
        
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('userEmail');

        this.showMessage('Logged out successfully', 'success');

        // Show auth view
        this.showAuthView();
    }

    showAuthView() {
        // Hide chat section
        this.chatSection.classList.add('hidden');
        
        // Show auth section
        this.authToggle.classList.remove('hidden');
        this.loginForm.classList.remove('hidden');
        this.signupForm.classList.add('hidden');
        this.logoutSection.classList.add('hidden');
        
        // Reset auth buttons
        document.getElementById('show-login').classList.add('active');
        document.getElementById('show-signup').classList.remove('active');
    }

    showLoggedInView() {
        // Hide auth section
        this.authToggle.classList.add('hidden');
        this.loginForm.classList.add('hidden');
        this.signupForm.classList.add('hidden');
        
        // Show logout section with user info
        document.getElementById('user-email').textContent = this.userEmail;
        this.logoutSection.classList.remove('hidden');
        
        // Show chat section
        this.chatSection.classList.remove('hidden');
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();

        if (!this.token) {
            this.showMessage('Please log in to chat with the AI assistant', 'error');
            return;
        }

        if (!message) {
            this.showMessage('Please enter a message', 'error');
            return;
        }

        // Add user message to UI
        this.addMessageToUI('user', message);
        
        // Clear input
        this.messageInput.value = '';
        
        // Disable input while waiting for response
        this.messageInput.disabled = true;
        document.getElementById('send-message').disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    conversation_id: this.currentConversationId || null,
                    message: message
                })
            });

            if (!response.ok) {
                if (response.status === 401) {
                    this.showMessage('Session expired. Please log in again.', 'error');
                    this.logout();
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Update conversation ID if it's the first message
            if (!this.currentConversationId) {
                this.currentConversationId = data.conversation_id;
            }
            
            // Add assistant response to UI
            this.addMessageToUI('assistant', data.response);
            
            // Log tool calls if any
            if (data.tool_calls && data.tool_calls.length > 0) {
                console.log('Tool calls executed:', data.tool_calls);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            if (error.message.includes('401')) {
                this.showMessage('Authentication required. Please log in.', 'error');
                this.logout();
            } else {
                this.showMessage('Failed to send message: ' + error.message, 'error');
            }
        } finally {
            // Re-enable input
            this.messageInput.disabled = false;
            document.getElementById('send-message').disabled = false;
            this.messageInput.focus();
        }
    }

    addMessageToUI(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.textContent = content;
        
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showMessage(message, type) {
        // Remove any existing message
        const existingMessage = document.querySelector('.status-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `status-message ${type}`;
        messageDiv.textContent = message;

        const app = document.getElementById('app');
        app.insertBefore(messageDiv, app.firstChild);

        // Auto-remove the message after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Phase4Chatbot();
});