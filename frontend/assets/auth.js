// Authentication API base URL
const API_BASE_URL = 'http://127.0.0.1:5000/api/auth';

// Tab switching
const loginTab = document.getElementById('loginTab');
const registerTab = document.getElementById('registerTab');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

if (loginTab && registerTab) {
    loginTab.addEventListener('click', () => {
        loginTab.classList.add('text-purple-400', 'border-b-2', 'border-purple-400');
        loginTab.classList.remove('text-gray-400');
        registerTab.classList.remove('text-purple-400', 'border-b-2', 'border-purple-400');
        registerTab.classList.add('text-gray-400');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        clearMessages();
    });

    registerTab.addEventListener('click', () => {
        registerTab.classList.add('text-purple-400', 'border-b-2', 'border-purple-400');
        registerTab.classList.remove('text-gray-400');
        loginTab.classList.remove('text-purple-400', 'border-b-2', 'border-purple-400');
        loginTab.classList.add('text-gray-400');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        clearMessages();
    });
}

// Password visibility toggles
(function initPasswordToggles() {
    const toggleButtons = document.querySelectorAll('[data-toggle-password]');
    toggleButtons.forEach((button) => {
        const targetId = button.getAttribute('data-toggle-password');
        const targetInput = document.getElementById(targetId);
        if (!targetInput) return;

        const showLabel = button.getAttribute('data-label-show') || 'Show';
        const hideLabel = button.getAttribute('data-label-hide') || 'Hide';

        // Ensure initial label matches the input state
        button.textContent = targetInput.type === 'password' ? showLabel : hideLabel;
        button.setAttribute('aria-label', targetInput.type === 'password' ? 'Show password' : 'Hide password');

        button.addEventListener('click', () => {
            const showPassword = targetInput.type === 'password';
            targetInput.type = showPassword ? 'text' : 'password';
            button.textContent = showPassword ? hideLabel : showLabel;
            button.setAttribute('aria-label', showPassword ? 'Hide password' : 'Show password');
            button.setAttribute('aria-pressed', String(showPassword));
        });
    });
})();

function clearMessages() {
    const loginError = document.getElementById('loginError');
    const registerError = document.getElementById('registerError');
    const registerSuccess = document.getElementById('registerSuccess');
    if (loginError) loginError.classList.add('hidden');
    if (registerError) registerError.classList.add('hidden');
    if (registerSuccess) registerSuccess.classList.add('hidden');
}

// Login functionality
const loginButton = document.getElementById('loginButton');
if (loginButton) {
    loginButton.addEventListener('click', async () => {
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        const errorDiv = document.getElementById('loginError');

        if (!username || !password) {
            errorDiv.textContent = 'Please fill in all fields';
            errorDiv.classList.remove('hidden');
            return;
        }

        loginButton.disabled = true;
        loginButton.textContent = 'Logging in...';
        errorDiv.classList.add('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/signin`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Store token in localStorage
                localStorage.setItem('tripster_token', data.accessToken);
                localStorage.setItem('tripster_username', username);
                
                // Redirect to home page
                window.location.href = 'index.html';
            } else {
                errorDiv.textContent = data.message || 'Login failed. Please check your credentials.';
                errorDiv.classList.remove('hidden');
                loginButton.disabled = false;
                loginButton.textContent = 'Login';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorDiv.textContent = 'Could not connect to server. Please ensure the backend is running.';
            errorDiv.classList.remove('hidden');
            loginButton.disabled = false;
            loginButton.textContent = 'Login';
        }
    });
}

// Register functionality
const registerButton = document.getElementById('registerButton');
if (registerButton) {
    registerButton.addEventListener('click', async () => {
        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const passwordConfirm = document.getElementById('registerPasswordConfirm').value;
        const errorDiv = document.getElementById('registerError');
        const successDiv = document.getElementById('registerSuccess');

        // Clear previous messages
        errorDiv.classList.add('hidden');
        successDiv.classList.add('hidden');

        // Validation
        if (!username || !email || !password || !passwordConfirm) {
            errorDiv.textContent = 'Please fill in all fields';
            errorDiv.classList.remove('hidden');
            return;
        }

        if (password !== passwordConfirm) {
            errorDiv.textContent = 'Passwords do not match';
            errorDiv.classList.remove('hidden');
            return;
        }

        if (password.length < 6) {
            errorDiv.textContent = 'Password must be at least 6 characters long';
            errorDiv.classList.remove('hidden');
            return;
        }

        registerButton.disabled = true;
        registerButton.textContent = 'Registering...';

        try {
            const response = await fetch(`${API_BASE_URL}/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                successDiv.textContent = data.message || 'Registration successful! You can now login.';
                successDiv.classList.remove('hidden');
                
                // Clear form
                document.getElementById('registerUsername').value = '';
                document.getElementById('registerEmail').value = '';
                document.getElementById('registerPassword').value = '';
                document.getElementById('registerPasswordConfirm').value = '';

                // Switch to login tab after 2 seconds
                setTimeout(() => {
                    loginTab.click();
                }, 2000);
            } else {
                errorDiv.textContent = data.message || 'Registration failed. Please try again.';
                errorDiv.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Registration error:', error);
            errorDiv.textContent = 'Could not connect to server. Please ensure the backend is running.';
            errorDiv.classList.remove('hidden');
        } finally {
            registerButton.disabled = false;
            registerButton.textContent = 'Register';
        }
    });
}

// Allow Enter key to submit forms
if (document.getElementById('loginPassword')) {
    document.getElementById('loginPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            loginButton.click();
        }
    });
}

if (document.getElementById('registerPasswordConfirm')) {
    document.getElementById('registerPasswordConfirm').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            registerButton.click();
        }
    });
}

// Utility functions for other pages
window.authUtils = {
    getToken: () => localStorage.getItem('tripster_token'),
    getUsername: () => localStorage.getItem('tripster_username'),
    isAuthenticated: () => !!localStorage.getItem('tripster_token'),
    logout: () => {
        localStorage.removeItem('tripster_token');
        localStorage.removeItem('tripster_username');
        window.location.href = 'login.html';
    }
};




