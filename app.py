from flask import Flask, request, redirect, render_template_string, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy data (can be connected to a database later)
STORED_SESSION = {}
ALLOWED_USER = 'kader11000'
ADMIN_PASSWORD = 'kader11000pass'
CONNECTED_API = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TikTok Tool Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite;
            color: #f5f5f5;
        }
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .card, .alert, .btn, .form-control {
            border-radius: 12px !important;
        }
        .card {
            background-color: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .form-control {
            background-color: rgba(255, 255, 255, 0.07);
            color: #fff;
            border: none;
        }
        .btn-primary, .btn-success, .btn-warning {
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        @keyframes fadeInSlide {
            0% {
                opacity: 0;
                transform: translateY(-30px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes floatLogo {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
        .animate-logo {
            animation: fadeInSlide 1.2s ease-out;
            color: #007bff;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        .logo-animated {
            animation: floatLogo 2.5s ease-in-out infinite;
        }
    </style>
</head>
<body class="container mt-5">
    <div class="text-center mb-4">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/0/09/TikTok_logo.svg/800px-TikTok_logo.svg.png"
             alt="TikTok Logo" width="80" class="mb-2 logo-animated">
        <h1 class="display-4 fw-bold animate-logo">kader11000</h1>
        <p class="text-muted">TikTok Tool Dashboard</p>
    </div>

    <div class="card p-4 mb-4">
        <h4>Login to TikTok</h4>
        <form method="POST" action="/login">
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <p class="mt-2 text-info">Automatic session will be saved after login.</p>
    </div>

    <div class="card p-4 mb-4">
        <h4>Settings</h4>
        <form method="POST" action="/settings">
            <div class="mb-3">
                <label class="form-label">Allowed TikTok Username</label>
                <input type="text" name="allowed_username" class="form-control" value="kader11000">
            </div>
            <div class="mb-3">
                <label class="form-label">Admin Password</label>
                <input type="password" name="admin_password" class="form-control" value="kader11000pass">
            </div>
            <button type="submit" class="btn btn-success">Save Settings</button>
        </form>
    </div>

    <div class="card p-4 mb-4">
        <h4>Session & API Controls</h4>
        <form method="POST" action="/api-control">
            <button type="submit" name="action" value="read" class="btn btn-warning mb-2">Read API Token</button>
            <button type="submit" name="action" value="copy" class="btn btn-secondary">Copy API Token</button>
        </form>
        <p class="mt-2 text-info">Your session token is automatically stored and integrated with TikTok API.</p>
    </div>

    <div class="card p-4">
        <h4>API Integration</h4>
        <form method="POST" action="/api-integration">
            <div class="mb-3">
                <label class="form-label">API Endpoint</label>
                <input type="url" name="api_endpoint" class="form-control" placeholder="https://api.tiktok.com/...">
            </div>
            <div class="mb-3">
                <label class="form-label">Access Token</label>
                <input type="text" name="access_token" class="form-control" placeholder="Enter your token">
            </div>
            <button type="submit" class="btn btn-success">Connect to API</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    if 'username' in session:
        return render_template_string(HTML_TEMPLATE)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ALLOWED_USER:
            session['username'] = username
            STORED_SESSION[username] = 'session_token_xyz'
            return redirect('/')
        else:
            return 'Unauthorized', 401
    return render_template_string(HTML_TEMPLATE)

@app.route('/settings', methods=['POST'])
def settings():
    global ALLOWED_USER, ADMIN_PASSWORD
    if request.form['admin_password'] == ADMIN_PASSWORD:
        ALLOWED_USER = request.form['allowed_username']
        ADMIN_PASSWORD = request.form['admin_password']
        return redirect('/')
    return 'Invalid admin password', 403

@app.route('/api-control', methods=['POST'])
def api_control():
    action = request.form['action']
    if 'username' not in session:
        return 'Unauthorized', 401
    if action == 'read':
        return f"Your API Token: {STORED_SESSION.get(session['username'], 'None')}"
    elif action == 'copy':
        return f"Copied Token: {STORED_SESSION.get(session['username'], 'None')}"
    return 'Unknown action'

@app.route('/api-integration', methods=['POST'])
def api_integration():
    endpoint = request.form['api_endpoint']
    token = request.form['access_token']
    CONNECTED_API['endpoint'] = endpoint
    CONNECTED_API['token'] = token
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
