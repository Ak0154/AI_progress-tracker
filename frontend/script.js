window.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'http://127.0.0.1:8000';
    const token = localStorage.getItem('access_token');
    
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const authMessage = document.getElementById('auth-message');

    const progressForm = document.getElementById('progress-form');
    const logoutBtn = document.getElementById('logout-btn');
    const getSummaryBtn = document.getElementById('get-summary-btn');
    if (loginForm || registerForm) {
        
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(loginForm);
                
                try {
                    const response = await fetch(`${API_URL}/auth/token`, {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        localStorage.setItem('access_token', data.access_token);
                        window.location.href = 'dashboard.html';
                    } else {
                        showAuthMessage(data.detail || 'An error occurred.', 'error');
                    }
                } catch (err) {
                    showAuthMessage('Could not connect to server.', 'error');
                }
            });
        }

        if (registerForm) {
            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('reg-username').value;
                const password = document.getElementById('reg-password').value;

                try {
                    const response = await fetch(`${API_URL}/auth/register`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        showAuthMessage('Registration successful! Please log in.', 'success');
                        registerForm.reset();
                    } else {
                        showAuthMessage(data.detail || 'Registration failed.', 'error');
                    }
                } catch (err) {
                    showAuthMessage('Could not connect to server.', 'error');
                }
            });
        }

        function showAuthMessage(message, type) {
            authMessage.textContent = message;
            authMessage.className = type;
        }
    }
    if (progressForm) {

        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
        });

        progressForm.addEventListener('submit', handleAddProgress);
        getSummaryBtn.addEventListener('click', handleGetSummary);

        async function handleAddProgress(e) {
            e.preventDefault();
            
            const entry = {
                date: document.getElementById('date').value,
                subject: document.getElementById('subject').value,
                time_spent_minutes: parseInt(document.getElementById('time').value),
                marks: parseFloat(document.getElementById('marks').value) || null,
                notes: document.getElementById('notes').value || null
            };

            try {
                const response = await fetch(`${API_URL}/progress/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(entry)
                });

                if (response.ok) {
                    alert("✅ Progress entry added successfully!");
                    progressForm.reset();
                } else {
                    alert('❌ Failed to add progress.');
                }
            } catch (err) {
                alert('⚠️ Error connecting to server.');
            }
        }

        /* 🧠 Redirect to AI Summary page */
        async function handleGetSummary() {
            window.location.href = 'ai_summary.html';
        }
    }
});
