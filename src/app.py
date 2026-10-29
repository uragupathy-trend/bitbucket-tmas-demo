#!/usr/bin/env python3
"""
Vision One Code Security Demo - Flask Application
This application contains intentional security vulnerabilities for TMAS testing.

⚠️ WARNING: This code contains security vulnerabilities and should NEVER be used in production!
All secrets and credentials are FAKE and for demonstration purposes only.
"""

import os
import sqlite3
import hashlib
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import subprocess
import pickle
import base64

# Import our vulnerable modules
from config import Config
from database import Database
from auth import AuthManager
from utils import SecurityUtils

# Initialize Flask app with debug mode (SECURITY ISSUE: Debug mode in production)
app = Flask(__name__)
app.debug = True  # SECURITY ISSUE: Debug mode should never be enabled in production

# Load configuration with hardcoded secrets
config = Config()
app.secret_key = config.SECRET_KEY  # SECURITY ISSUE: Hardcoded secret key

# Initialize components
db = Database()
auth_manager = AuthManager()
security_utils = SecurityUtils()

# SECURITY ISSUE: Hardcoded AWS credentials (FAKE - for testing only)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-west-2"

# SECURITY ISSUE: Hardcoded database credentials
DB_PASSWORD = "super_secret_password_123"
DB_CONNECTION_STRING = f"postgresql://admin:{DB_PASSWORD}@localhost:5432/visionone_demo"

# SECURITY ISSUE: Hardcoded API keys (FAKE - for testing only)
VISION_ONE_API_KEY = "fake-vision-one-api-key-12345-abcdef"
GITHUB_TOKEN = "ghp_fake_github_token_for_testing_only_123456789"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

# SECURITY ISSUE: JWT secret hardcoded
JWT_SECRET = "jwt-super-secret-key-never-change-this"

@app.route('/')
def index():
    """Home page with basic information"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vision One Code Security Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .warning { background: #ffebee; border: 1px solid #f44336; padding: 20px; margin: 20px 0; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }
        </style>
    </head>
    <body>
        <h1>🛡️ Vision One Code Security Demo</h1>
        
        <div class="warning">
            <h3>⚠️ Security Warning</h3>
            <p>This application contains intentional security vulnerabilities for TMAS testing purposes.</p>
            <p><strong>DO NOT USE IN PRODUCTION!</strong></p>
        </div>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <strong>POST /api/login</strong><br>
            Login with username/password (vulnerable to SQL injection)
        </div>
        
        <div class="endpoint">
            <strong>GET /api/user/{id}</strong><br>
            Get user information (vulnerable to SQL injection)
        </div>
        
        <div class="endpoint">
            <strong>POST /api/search</strong><br>
            Search functionality (vulnerable to command injection)
        </div>
        
        <div class="endpoint">
            <strong>POST /api/upload</strong><br>
            File upload (vulnerable to path traversal)
        </div>
        
        <div class="endpoint">
            <strong>GET /api/config</strong><br>
            Application configuration (exposes secrets)
        </div>
        
        <div class="endpoint">
            <strong>POST /api/deserialize</strong><br>
            Data processing (vulnerable to deserialization attacks)
        </div>
        
        <h2>Security Issues Included</h2>
        <ul>
            <li>Hardcoded AWS credentials and API keys</li>
            <li>SQL injection vulnerabilities</li>
            <li>Command injection vulnerabilities</li>
            <li>Insecure deserialization</li>
            <li>Path traversal vulnerabilities</li>
            <li>Debug mode enabled</li>
            <li>Weak session management</li>
            <li>Information disclosure</li>
        </ul>
        
        <p><em>All credentials are FAKE and for testing purposes only.</em></p>
    </body>
    </html>
    """)

@app.route('/api/login', methods=['POST'])
def login():
    """
    User login endpoint
    SECURITY ISSUE: Vulnerable to SQL injection
    """
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    
    # SECURITY ISSUE: SQL injection vulnerability - user input directly in query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        result = db.execute_query(query)
        if result:
            # SECURITY ISSUE: Weak JWT implementation
            token = jwt.encode({
                'user_id': result[0]['id'],
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, JWT_SECRET, algorithm='HS256')
            
            return jsonify({
                'success': True,
                'token': token,
                'message': 'Login successful'
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        # SECURITY ISSUE: Information disclosure through error messages
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}',
            'query': query  # SECURITY ISSUE: Exposing SQL query in error
        }), 500

@app.route('/api/user/<user_id>')
def get_user(user_id):
    """
    Get user information
    SECURITY ISSUE: SQL injection through URL parameter
    """
    # SECURITY ISSUE: No input validation, direct SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    try:
        result = db.execute_query(query)
        if result:
            user = result[0]
            # SECURITY ISSUE: Exposing sensitive information
            return jsonify({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'password_hash': user['password'],  # SECURITY ISSUE: Exposing password hash
                'api_key': user.get('api_key', ''),  # SECURITY ISSUE: Exposing API key
                'aws_access_key': AWS_ACCESS_KEY_ID,  # SECURITY ISSUE: Exposing AWS credentials
                'database_url': DB_CONNECTION_STRING  # SECURITY ISSUE: Exposing DB connection
            })
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({
            'error': f'Database error: {str(e)}',
            'query': query
        }), 500

@app.route('/api/search', methods=['POST'])
def search():
    """
    Search functionality
    SECURITY ISSUE: Command injection vulnerability
    """
    search_term = request.json.get('query', '')
    search_type = request.json.get('type', 'file')
    
    # SECURITY ISSUE: Command injection - user input directly in shell command
    if search_type == 'file':
        command = f"find /tmp -name '*{search_term}*'"
    elif search_type == 'content':
        command = f"grep -r '{search_term}' /tmp/"
    else:
        command = f"ls -la | grep {search_term}"
    
    try:
        # SECURITY ISSUE: Executing user-controlled shell commands
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return jsonify({
            'command': command,  # SECURITY ISSUE: Exposing executed command
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Command execution failed: {str(e)}',
            'command': command
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    File upload endpoint
    SECURITY ISSUE: Path traversal vulnerability
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = request.form.get('filename', file.filename)
    
    # SECURITY ISSUE: No path validation - allows directory traversal
    upload_path = f"/tmp/uploads/{filename}"
    
    try:
        # SECURITY ISSUE: Saving file without validation
        file.save(upload_path)
        
        # SECURITY ISSUE: Exposing file system information
        file_info = os.stat(upload_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': upload_path,  # SECURITY ISSUE: Exposing file path
            'size': file_info.st_size,
            'upload_dir': '/tmp/uploads',  # SECURITY ISSUE: Exposing directory structure
            'aws_bucket': 'vision-one-demo-bucket',  # SECURITY ISSUE: Exposing AWS bucket name
            'aws_key': AWS_ACCESS_KEY_ID  # SECURITY ISSUE: Exposing AWS credentials
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Upload failed: {str(e)}',
            'path': upload_path
        }), 500

@app.route('/api/config')
def get_config():
    """
    Application configuration endpoint
    SECURITY ISSUE: Exposing sensitive configuration and secrets
    """
    return jsonify({
        'app_name': 'Vision One Code Security Demo',
        'version': '1.0.0',
        'debug': app.debug,
        'secret_key': app.secret_key,  # SECURITY ISSUE: Exposing secret key
        'database': {
            'host': 'localhost',
            'port': 5432,
            'username': 'admin',
            'password': DB_PASSWORD,  # SECURITY ISSUE: Exposing DB password
            'connection_string': DB_CONNECTION_STRING  # SECURITY ISSUE: Full connection string
        },
        'aws': {
            'access_key_id': AWS_ACCESS_KEY_ID,  # SECURITY ISSUE: Exposing AWS credentials
            'secret_access_key': AWS_SECRET_ACCESS_KEY,  # SECURITY ISSUE: Exposing AWS secret
            'region': AWS_REGION,
            'bucket': 'vision-one-demo-bucket'
        },
        'api_keys': {
            'vision_one': VISION_ONE_API_KEY,  # SECURITY ISSUE: Exposing API key
            'github': GITHUB_TOKEN,  # SECURITY ISSUE: Exposing GitHub token
            'slack_webhook': SLACK_WEBHOOK_URL  # SECURITY ISSUE: Exposing webhook URL
        },
        'jwt': {
            'secret': JWT_SECRET,  # SECURITY ISSUE: Exposing JWT secret
            'algorithm': 'HS256'
        },
        'environment': os.environ.copy()  # SECURITY ISSUE: Exposing all environment variables
    })

@app.route('/api/deserialize', methods=['POST'])
def deserialize_data():
    """
    Data deserialization endpoint
    SECURITY ISSUE: Insecure deserialization vulnerability
    """
    data = request.json.get('data', '')
    
    try:
        # SECURITY ISSUE: Deserializing untrusted data with pickle
        decoded_data = base64.b64decode(data)
        result = pickle.loads(decoded_data)  # SECURITY ISSUE: Pickle deserialization
        
        return jsonify({
            'success': True,
            'result': str(result),
            'type': type(result).__name__
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Deserialization failed: {str(e)}',
            'data': data
        }), 500

@app.route('/api/proxy', methods=['POST'])
def proxy_request():
    """
    HTTP proxy endpoint
    SECURITY ISSUE: Server-Side Request Forgery (SSRF)
    """
    url = request.json.get('url', '')
    headers = request.json.get('headers', {})
    
    # SECURITY ISSUE: No URL validation - allows SSRF attacks
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text[:1000],  # Limit content for demo
            'url': url  # SECURITY ISSUE: Reflecting user input
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Request failed: {str(e)}',
            'url': url
        }), 500

@app.route('/api/eval', methods=['POST'])
def eval_code():
    """
    Code evaluation endpoint
    SECURITY ISSUE: Code injection vulnerability
    """
    code = request.json.get('code', '')
    
    # SECURITY ISSUE: Executing arbitrary user code
    try:
        result = eval(code)  # SECURITY ISSUE: eval() with user input
        
        return jsonify({
            'success': True,
            'result': str(result),
            'code': code
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Evaluation failed: {str(e)}',
            'code': code
        }), 500

@app.errorhandler(404)
def not_found(error):
    """
    404 error handler
    SECURITY ISSUE: Information disclosure in error messages
    """
    return jsonify({
        'error': 'Not found',
        'path': request.path,
        'method': request.method,
        'headers': dict(request.headers),  # SECURITY ISSUE: Exposing request headers
        'args': dict(request.args),
        'form': dict(request.form),
        'files': list(request.files.keys()),
        'remote_addr': request.remote_addr,
        'user_agent': request.user_agent.string
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    500 error handler
    SECURITY ISSUE: Information disclosure in error messages
    """
    return jsonify({
        'error': 'Internal server error',
        'debug_info': {
            'error': str(error),
            'path': request.path,
            'method': request.method,
            'config': {
                'debug': app.debug,
                'secret_key': app.secret_key[:10] + '...',  # SECURITY ISSUE: Partial secret exposure
                'database_host': 'localhost'
            }
        }
    }), 500

if __name__ == '__main__':
    # SECURITY ISSUE: Running with debug mode and on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
