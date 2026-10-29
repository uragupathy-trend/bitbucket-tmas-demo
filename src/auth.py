#!/usr/bin/env python3
"""
Authentication module with security vulnerabilities
SECURITY ISSUE: Contains weak authentication and authorization mechanisms
"""

import hashlib
import jwt
import base64
import os
import time
from datetime import datetime, timedelta
from config import Config

class AuthManager:
    """
    Authentication manager with intentional security vulnerabilities
    SECURITY ISSUE: Weak authentication and session management
    """
    
    def __init__(self):
        """Initialize authentication manager"""
        self.config = Config()
        # SECURITY ISSUE: Hardcoded JWT secret
        self.jwt_secret = self.config.JWT_CONFIG['secret']
        self.jwt_algorithm = self.config.JWT_CONFIG['algorithm']
        
        # SECURITY ISSUE: Weak session storage (in-memory dictionary)
        self.active_sessions = {}
        
        # SECURITY ISSUE: Hardcoded admin credentials
        self.admin_credentials = {
            'username': 'admin',
            'password': 'admin123',  # SECURITY ISSUE: Weak password
            'api_key': 'admin-master-key-12345'
        }
    
    def hash_password(self, password):
        """
        Hash password
        SECURITY ISSUE: Uses weak MD5 hashing without salt
        """
        # SECURITY ISSUE: MD5 is cryptographically broken
        return hashlib.md5(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed_password):
        """
        Verify password
        SECURITY ISSUE: Weak password verification
        """
        # SECURITY ISSUE: Simple MD5 comparison
        return self.hash_password(password) == hashed_password
    
    def generate_session_token(self, user_id, username):
        """
        Generate session token
        SECURITY ISSUE: Predictable session token generation
        """
        # SECURITY ISSUE: Predictable token based on user info and timestamp
        timestamp = str(int(time.time()))
        token_data = f"{user_id}:{username}:{timestamp}"
        
        # SECURITY ISSUE: Base64 encoding is not encryption
        session_token = base64.b64encode(token_data.encode()).decode()
        
        # SECURITY ISSUE: Logging session tokens
        print(f"[AUTH] Generated session token for {username}: {session_token}")
        
        return session_token
    
    def create_jwt_token(self, user_id, username, role='user'):
        """
        Create JWT token
        SECURITY ISSUE: Weak JWT implementation
        """
        # SECURITY ISSUE: Long expiration time
        expiration = datetime.utcnow() + timedelta(hours=24)
        
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': expiration,
            'iat': datetime.utcnow(),
            # SECURITY ISSUE: Including sensitive information in JWT
            'admin_key': self.admin_credentials['api_key'] if role == 'admin' else None,
            'secret_key': self.config.SECRET_KEY[:10]  # SECURITY ISSUE: Partial secret in token
        }
        
        try:
            # SECURITY ISSUE: Using weak secret for JWT signing
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            
            # SECURITY ISSUE: Logging JWT tokens
            print(f"[AUTH] Created JWT token for {username}: {token}")
            
            return token
            
        except Exception as e:
            print(f"[AUTH] JWT creation error: {e}")
            return None
    
    def verify_jwt_token(self, token):
        """
        Verify JWT token
        SECURITY ISSUE: Weak JWT verification
        """
        try:
            # SECURITY ISSUE: No proper token validation
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # SECURITY ISSUE: Logging token payload
            print(f"[AUTH] JWT token verified: {payload}")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            print("[AUTH] JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"[AUTH] Invalid JWT token: {e}")
            return None
    
    def authenticate_user(self, username, password):
        """
        Authenticate user
        SECURITY ISSUE: Multiple authentication vulnerabilities
        """
        # SECURITY ISSUE: Check hardcoded admin credentials first
        if username == self.admin_credentials['username']:
            if password == self.admin_credentials['password']:
                print(f"[AUTH] Admin authentication successful")
                return {
                    'id': 0,
                    'username': username,
                    'role': 'admin',
                    'api_key': self.admin_credentials['api_key']
                }
        
        # SECURITY ISSUE: Weak password validation
        if len(password) < 3:  # SECURITY ISSUE: Very weak password requirement
            print(f"[AUTH] Password too short for user: {username}")
            return None
        
        # SECURITY ISSUE: Common password check (but allows them)
        common_passwords = ['password', '123456', 'admin', 'test', 'guest', '']
        if password in common_passwords:
            print(f"[AUTH] Warning: User {username} using common password: {password}")
            # SECURITY ISSUE: Still allows authentication with weak passwords
        
        # SECURITY ISSUE: Simulate database lookup with hardcoded users
        fake_users = {
            'user1': {'id': 1, 'password': 'password', 'role': 'user'},
            'test': {'id': 2, 'password': 'test', 'role': 'user'},
            'demo': {'id': 3, 'password': '123456', 'role': 'user'},
            'guest': {'id': 4, 'password': '', 'role': 'guest'}  # SECURITY ISSUE: Empty password
        }
        
        if username in fake_users:
            user = fake_users[username]
            if user['password'] == password:  # SECURITY ISSUE: Plain text comparison
                print(f"[AUTH] User authentication successful: {username}")
                return {
                    'id': user['id'],
                    'username': username,
                    'role': user['role'],
                    'api_key': f"{username}-api-key-{user['id']}"
                }
        
        print(f"[AUTH] Authentication failed for user: {username}")
        return None
    
    def authenticate_api_key(self, api_key):
        """
        Authenticate using API key
        SECURITY ISSUE: Weak API key authentication
        """
        # SECURITY ISSUE: Check hardcoded admin API key
        if api_key == self.admin_credentials['api_key']:
            print(f"[AUTH] Admin API key authentication successful")
            return {
                'id': 0,
                'username': 'admin',
                'role': 'admin',
                'api_key': api_key
            }
        
        # SECURITY ISSUE: Predictable API key format
        if api_key.endswith('-api-key-1') or api_key.endswith('-api-key-2') or api_key.endswith('-api-key-3'):
            username = api_key.split('-api-key-')[0]
            print(f"[AUTH] API key authentication successful for: {username}")
            return {
                'id': 1,
                'username': username,
                'role': 'user',
                'api_key': api_key
            }
        
        print(f"[AUTH] Invalid API key: {api_key}")
        return None
    
    def create_session(self, user_id, username, ip_address, user_agent):
        """
        Create user session
        SECURITY ISSUE: Insecure session management
        """
        session_token = self.generate_session_token(user_id, username)
        
        # SECURITY ISSUE: Storing sessions in memory (lost on restart)
        session_data = {
            'user_id': user_id,
            'username': username,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            # SECURITY ISSUE: No session expiration
            'expires_at': None
        }
        
        self.active_sessions[session_token] = session_data
        
        # SECURITY ISSUE: Logging session creation with sensitive data
        print(f"[AUTH] Session created: {session_token} for user {username}")
        print(f"[AUTH] Session data: {session_data}")
        
        return session_token
    
    def validate_session(self, session_token):
        """
        Validate session token
        SECURITY ISSUE: Weak session validation
        """
        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            
            # SECURITY ISSUE: No session expiration check
            # Update last activity
            session['last_activity'] = datetime.utcnow()
            
            print(f"[AUTH] Session validated for user: {session['username']}")
            return session
        
        print(f"[AUTH] Invalid session token: {session_token}")
        return None
    
    def logout_session(self, session_token):
        """
        Logout session
        SECURITY ISSUE: Basic session cleanup
        """
        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            username = session['username']
            del self.active_sessions[session_token]
            
            print(f"[AUTH] Session logged out for user: {username}")
            return True
        
        return False
    
    def check_permissions(self, user_role, required_role):
        """
        Check user permissions
        SECURITY ISSUE: Weak authorization logic
        """
        # SECURITY ISSUE: Simple string comparison for roles
        role_hierarchy = {
            'guest': 0,
            'user': 1,
            'admin': 2
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 1)
        
        # SECURITY ISSUE: Logging authorization checks
        print(f"[AUTH] Permission check: {user_role} ({user_level}) >= {required_role} ({required_level})")
        
        return user_level >= required_level
    
    def generate_api_key(self, username):
        """
        Generate API key for user
        SECURITY ISSUE: Predictable API key generation
        """
        # SECURITY ISSUE: Predictable API key format
        timestamp = str(int(time.time()))
        api_key = f"{username}-api-key-{timestamp[-6:]}"
        
        print(f"[AUTH] Generated API key for {username}: {api_key}")
        return api_key
    
    def reset_password(self, username, new_password):
        """
        Reset user password
        SECURITY ISSUE: No verification for password reset
        """
        # SECURITY ISSUE: No identity verification
        # SECURITY ISSUE: No password strength validation
        
        print(f"[AUTH] Password reset for user {username} to: {new_password}")
        
        # SECURITY ISSUE: Return new password in response
        return {
            'success': True,
            'username': username,
            'new_password': new_password,
            'message': 'Password reset successful'
        }
    
    def get_user_sessions(self, username):
        """
        Get all sessions for a user
        SECURITY ISSUE: Exposes session information
        """
        user_sessions = []
        
        for token, session in self.active_sessions.items():
            if session['username'] == username:
                # SECURITY ISSUE: Exposing session tokens and details
                user_sessions.append({
                    'token': token,
                    'ip_address': session['ip_address'],
                    'user_agent': session['user_agent'],
                    'created_at': session['created_at'].isoformat(),
                    'last_activity': session['last_activity'].isoformat()
                })
        
        print(f"[AUTH] Retrieved {len(user_sessions)} sessions for user: {username}")
        return user_sessions
    
    def export_auth_config(self):
        """
        Export authentication configuration
        SECURITY ISSUE: Exposes sensitive authentication configuration
        """
        config = {
            'jwt_secret': self.jwt_secret,  # SECURITY ISSUE: Exposing JWT secret
            'jwt_algorithm': self.jwt_algorithm,
            'admin_credentials': self.admin_credentials,  # SECURITY ISSUE: Exposing admin creds
            'active_sessions_count': len(self.active_sessions),
            'session_tokens': list(self.active_sessions.keys()),  # SECURITY ISSUE: Exposing session tokens
            'config': self.config.export_config()  # SECURITY ISSUE: Exposing full config
        }
        
        print(f"[AUTH] Exported authentication configuration")
        return config

# SECURITY ISSUE: Global authentication manager instance
auth_manager = AuthManager()
