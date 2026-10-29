#!/usr/bin/env python3
"""
Database module with SQL injection vulnerabilities
SECURITY ISSUE: Contains multiple SQL injection vulnerabilities and insecure database practices
"""

import sqlite3
import hashlib
import os
from config import Config

class Database:
    """
    Database class with intentional security vulnerabilities
    SECURITY ISSUE: Multiple SQL injection vulnerabilities and insecure practices
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.config = Config()
        # SECURITY ISSUE: Using SQLite for demo, but connection string shows PostgreSQL
        self.db_path = '/tmp/visionone_demo.db'
        self.init_database()
    
    def init_database(self):
        """
        Initialize database with sample data
        SECURITY ISSUE: Creates database with weak sample data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT,
                    api_key TEXT,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # SECURITY ISSUE: Insert sample users with weak passwords
            sample_users = [
                ('admin', 'admin123', 'admin@example.com', 'admin-api-key-12345', 'admin'),
                ('user1', 'password', 'user1@example.com', 'user1-api-key-67890', 'user'),
                ('test', 'test', 'test@example.com', 'test-api-key-abcdef', 'user'),
                ('demo', '123456', 'demo@example.com', 'demo-api-key-ghijkl', 'user'),
                ('guest', '', 'guest@example.com', 'guest-api-key-mnopqr', 'guest')  # SECURITY ISSUE: Empty password
            ]
            
            for username, password, email, api_key, role in sample_users:
                # SECURITY ISSUE: Storing passwords in plain text
                cursor.execute('''
                    INSERT OR REPLACE INTO users (username, password, email, api_key, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password, email, api_key, role))
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # SECURITY ISSUE: Logging database initialization with sensitive info
            print(f"[DATABASE] Initialized database at {self.db_path}")
            print(f"[DATABASE] Sample users created with weak passwords")
            
        except Exception as e:
            print(f"[DATABASE] Error initializing database: {e}")
    
    def execute_query(self, query, params=None):
        """
        Execute SQL query
        SECURITY ISSUE: Allows execution of arbitrary SQL queries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # SECURITY ISSUE: Logging SQL queries with potential sensitive data
            print(f"[DATABASE] Executing query: {query}")
            if params:
                print(f"[DATABASE] Query parameters: {params}")
            
            if params:
                cursor.execute(query, params)
            else:
                # SECURITY ISSUE: Executing raw SQL without parameters
                cursor.execute(query)
            
            # Determine if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
                conn.close()
                return results
            else:
                conn.commit()
                conn.close()
                return cursor.rowcount
                
        except Exception as e:
            print(f"[DATABASE] Query execution error: {e}")
            raise e
    
    def get_user_by_username(self, username):
        """
        Get user by username
        SECURITY ISSUE: Vulnerable to SQL injection
        """
        # SECURITY ISSUE: Direct string interpolation in SQL query
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return self.execute_query(query)
    
    def get_user_by_id(self, user_id):
        """
        Get user by ID
        SECURITY ISSUE: Vulnerable to SQL injection
        """
        # SECURITY ISSUE: Direct string interpolation without validation
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.execute_query(query)
    
    def authenticate_user(self, username, password):
        """
        Authenticate user
        SECURITY ISSUE: Multiple vulnerabilities in authentication
        """
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            result = self.execute_query(query)
            if result:
                user = result[0]
                # SECURITY ISSUE: Logging authentication attempts with credentials
                print(f"[DATABASE] Authentication successful for user: {username}")
                print(f"[DATABASE] User details: {user}")
                return user
            else:
                # SECURITY ISSUE: Logging failed authentication attempts
                print(f"[DATABASE] Authentication failed for user: {username} with password: {password}")
                return None
                
        except Exception as e:
            # SECURITY ISSUE: Exposing database errors
            print(f"[DATABASE] Authentication error: {e}")
            return None
    
    def create_user(self, username, password, email, role='user'):
        """
        Create new user
        SECURITY ISSUE: Insecure user creation
        """
        # SECURITY ISSUE: No password validation or hashing
        api_key = f"{username}-api-key-{hashlib.md5(username.encode()).hexdigest()[:8]}"
        
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"""
            INSERT INTO users (username, password, email, api_key, role)
            VALUES ('{username}', '{password}', '{email}', '{api_key}', '{role}')
        """
        
        try:
            result = self.execute_query(query)
            print(f"[DATABASE] Created user: {username} with password: {password}")
            return result
        except Exception as e:
            print(f"[DATABASE] Error creating user: {e}")
            raise e
    
    def update_user_password(self, user_id, new_password):
        """
        Update user password
        SECURITY ISSUE: No password validation or hashing
        """
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"UPDATE users SET password = '{new_password}' WHERE id = {user_id}"
        
        try:
            result = self.execute_query(query)
            print(f"[DATABASE] Updated password for user ID {user_id} to: {new_password}")
            return result
        except Exception as e:
            print(f"[DATABASE] Error updating password: {e}")
            raise e
    
    def search_users(self, search_term):
        """
        Search users
        SECURITY ISSUE: SQL injection vulnerability in search
        """
        # SECURITY ISSUE: Direct string interpolation in LIKE query
        query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"[DATABASE] Search error: {e}")
            raise e
    
    def log_action(self, user_id, action, details, ip_address):
        """
        Log user action
        SECURITY ISSUE: SQL injection in logging
        """
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"""
            INSERT INTO logs (user_id, action, details, ip_address)
            VALUES ({user_id}, '{action}', '{details}', '{ip_address}')
        """
        
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"[DATABASE] Logging error: {e}")
            raise e
    
    def get_user_logs(self, user_id):
        """
        Get user logs
        SECURITY ISSUE: SQL injection vulnerability
        """
        # SECURITY ISSUE: Direct string interpolation
        query = f"SELECT * FROM logs WHERE user_id = {user_id} ORDER BY timestamp DESC"
        
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"[DATABASE] Error retrieving logs: {e}")
            raise e
    
    def create_session(self, user_id, session_token, ip_address, user_agent):
        """
        Create user session
        SECURITY ISSUE: Insecure session management
        """
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"""
            INSERT INTO sessions (user_id, session_token, ip_address, user_agent)
            VALUES ({user_id}, '{session_token}', '{ip_address}', '{user_agent}')
        """
        
        try:
            result = self.execute_query(query)
            # SECURITY ISSUE: Logging session tokens
            print(f"[DATABASE] Created session for user {user_id}: {session_token}")
            return result
        except Exception as e:
            print(f"[DATABASE] Session creation error: {e}")
            raise e
    
    def get_session(self, session_token):
        """
        Get session by token
        SECURITY ISSUE: SQL injection vulnerability
        """
        # SECURITY ISSUE: Direct string interpolation
        query = f"SELECT * FROM sessions WHERE session_token = '{session_token}'"
        
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"[DATABASE] Session retrieval error: {e}")
            raise e
    
    def execute_raw_sql(self, sql_query):
        """
        Execute raw SQL query
        SECURITY ISSUE: Allows execution of arbitrary SQL
        """
        # SECURITY ISSUE: No validation or sanitization
        print(f"[DATABASE] Executing raw SQL: {sql_query}")
        
        try:
            return self.execute_query(sql_query)
        except Exception as e:
            print(f"[DATABASE] Raw SQL execution error: {e}")
            raise e
    
    def backup_database(self, backup_path):
        """
        Backup database
        SECURITY ISSUE: Insecure backup functionality
        """
        try:
            # SECURITY ISSUE: No path validation - allows path traversal
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            # SECURITY ISSUE: Logging backup location
            print(f"[DATABASE] Database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            print(f"[DATABASE] Backup error: {e}")
            return False
    
    def get_database_info(self):
        """
        Get database information
        SECURITY ISSUE: Exposes sensitive database information
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table information
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Get user count
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # Get database file size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            conn.close()
            
            # SECURITY ISSUE: Exposing database structure and statistics
            info = {
                'database_path': self.db_path,
                'tables': tables,
                'user_count': user_count,
                'database_size': db_size,
                'connection_string': self.config.get_database_url(),
                'config': self.config.DATABASE_CONFIG
            }
            
            print(f"[DATABASE] Database info: {info}")
            return info
            
        except Exception as e:
            print(f"[DATABASE] Error getting database info: {e}")
            raise e

# SECURITY ISSUE: Global database instance
db_instance = Database()
