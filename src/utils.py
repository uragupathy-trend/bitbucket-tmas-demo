#!/usr/bin/env python3
"""
Utility module with security vulnerabilities
SECURITY ISSUE: Contains various utility functions with security flaws
"""

import os
import subprocess
import pickle
import base64
import hashlib
import random
import string
import tempfile
import shutil
from urllib.parse import urlparse
import requests

class SecurityUtils:
    """
    Security utilities with intentional vulnerabilities
    SECURITY ISSUE: Multiple security flaws in utility functions
    """
    
    def __init__(self):
        """Initialize security utilities"""
        # SECURITY ISSUE: Hardcoded encryption key
        self.encryption_key = "REPLACE_ME_ENCRYPTION_KEY"
        
        # SECURITY ISSUE: Weak random seed
        random.seed(12345)
    
    def sanitize_input(self, user_input):
        """
        Sanitize user input
        SECURITY ISSUE: Inadequate input sanitization
        """
        # SECURITY ISSUE: Only removes obvious SQL injection patterns
        dangerous_patterns = ["'", '"', ';', '--', '/*', '*/', 'DROP', 'DELETE']
        
        sanitized = user_input
        for pattern in dangerous_patterns:
            # SECURITY ISSUE: Case-sensitive replacement only
            sanitized = sanitized.replace(pattern, '')
        
        # SECURITY ISSUE: Logging potentially sensitive input
        print(f"[UTILS] Sanitized input: '{user_input}' -> '{sanitized}'")
        
        return sanitized
    
    def validate_email(self, email):
        """
        Validate email address
        SECURITY ISSUE: Weak email validation
        """
        # SECURITY ISSUE: Very basic email validation
        if '@' in email and '.' in email:
            print(f"[UTILS] Email validation passed: {email}")
            return True
        
        print(f"[UTILS] Email validation failed: {email}")
        return False
    
    def generate_random_string(self, length=10):
        """
        Generate random string
        SECURITY ISSUE: Predictable random generation
        """
        # SECURITY ISSUE: Using weak random with fixed seed
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        
        print(f"[UTILS] Generated random string: {random_string}")
        return random_string
    
    def hash_data(self, data):
        """
        Hash data
        SECURITY ISSUE: Uses weak MD5 hashing
        """
        # SECURITY ISSUE: MD5 is cryptographically broken
        hash_value = hashlib.md5(data.encode()).hexdigest()
        
        print(f"[UTILS] Hashed data: '{data}' -> {hash_value}")
        return hash_value
    
    def encrypt_data(self, data):
        """
        Encrypt data
        SECURITY ISSUE: Fake encryption using base64
        """
        # SECURITY ISSUE: Base64 encoding is not encryption
        encrypted = base64.b64encode(data.encode()).decode()
        
        print(f"[UTILS] Encrypted data: '{data}' -> {encrypted}")
        return encrypted
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt data
        SECURITY ISSUE: Fake decryption using base64
        """
        try:
            # SECURITY ISSUE: Base64 decoding is not decryption
            decrypted = base64.b64decode(encrypted_data).decode()
            
            print(f"[UTILS] Decrypted data: '{encrypted_data}' -> {decrypted}")
            return decrypted
            
        except Exception as e:
            print(f"[UTILS] Decryption error: {e}")
            return None
    
    def serialize_object(self, obj):
        """
        Serialize object
        SECURITY ISSUE: Uses pickle for serialization
        """
        # SECURITY ISSUE: Pickle serialization can be dangerous
        serialized = pickle.dumps(obj)
        encoded = base64.b64encode(serialized).decode()
        
        print(f"[UTILS] Serialized object: {type(obj).__name__}")
        return encoded
    
    def deserialize_object(self, serialized_data):
        """
        Deserialize object
        SECURITY ISSUE: Unsafe pickle deserialization
        """
        try:
            # SECURITY ISSUE: Pickle deserialization of untrusted data
            decoded = base64.b64decode(serialized_data)
            obj = pickle.loads(decoded)
            
            print(f"[UTILS] Deserialized object: {type(obj).__name__}")
            return obj
            
        except Exception as e:
            print(f"[UTILS] Deserialization error: {e}")
            return None
    
    def execute_command(self, command):
        """
        Execute system command
        SECURITY ISSUE: Command injection vulnerability
        """
        try:
            # SECURITY ISSUE: Executing user-provided commands without validation
            print(f"[UTILS] Executing command: {command}")
            
            result = subprocess.run(
                command, 
                shell=True,  # SECURITY ISSUE: Using shell=True
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            output = {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'command': command  # SECURITY ISSUE: Echoing command in output
            }
            
            print(f"[UTILS] Command output: {output}")
            return output
            
        except Exception as e:
            print(f"[UTILS] Command execution error: {e}")
            return {'error': str(e), 'command': command}
    
    def download_file(self, url, filename=None):
        """
        Download file from URL
        SECURITY ISSUE: No URL validation - SSRF vulnerability
        """
        try:
            # SECURITY ISSUE: No URL validation
            print(f"[UTILS] Downloading file from: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                # SECURITY ISSUE: Filename from URL without validation
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path) or 'downloaded_file'
            
            # SECURITY ISSUE: No path validation - path traversal vulnerability
            file_path = f"/tmp/{filename}"
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"[UTILS] File downloaded to: {file_path}")
            
            return {
                'success': True,
                'file_path': file_path,
                'size': len(response.content),
                'url': url  # SECURITY ISSUE: Reflecting URL in response
            }
            
        except Exception as e:
            print(f"[UTILS] Download error: {e}")
            return {'success': False, 'error': str(e), 'url': url}
    
    def save_file(self, content, filename):
        """
        Save content to file
        SECURITY ISSUE: Path traversal vulnerability
        """
        try:
            # SECURITY ISSUE: No path validation
            file_path = f"/tmp/{filename}"
            
            # SECURITY ISSUE: Creating directories without validation
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"[UTILS] Content saved to: {file_path}")
            
            return {
                'success': True,
                'file_path': file_path,
                'size': len(content)
            }
            
        except Exception as e:
            print(f"[UTILS] File save error: {e}")
            return {'success': False, 'error': str(e)}
    
    def read_file(self, filename):
        """
        Read file content
        SECURITY ISSUE: Path traversal vulnerability
        """
        try:
            # SECURITY ISSUE: No path validation - allows reading any file
            file_path = f"/tmp/{filename}"
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            print(f"[UTILS] Read file: {file_path} ({len(content)} bytes)")
            
            return {
                'success': True,
                'content': content,
                'file_path': file_path,
                'size': len(content)
            }
            
        except Exception as e:
            print(f"[UTILS] File read error: {e}")
            return {'success': False, 'error': str(e)}
    
    def backup_file(self, source_path, backup_dir="/tmp/backups"):
        """
        Backup file
        SECURITY ISSUE: Path traversal and insecure backup
        """
        try:
            # SECURITY ISSUE: No path validation
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            filename = os.path.basename(source_path)
            backup_path = os.path.join(backup_dir, f"{filename}.backup")
            
            # SECURITY ISSUE: Using shutil.copy2 without validation
            shutil.copy2(source_path, backup_path)
            
            print(f"[UTILS] File backed up: {source_path} -> {backup_path}")
            
            return {
                'success': True,
                'source_path': source_path,
                'backup_path': backup_path
            }
            
        except Exception as e:
            print(f"[UTILS] Backup error: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_url(self, url):
        """
        Validate URL
        SECURITY ISSUE: Inadequate URL validation
        """
        # SECURITY ISSUE: Very basic URL validation
        if url.startswith('http://') or url.startswith('https://'):
            print(f"[UTILS] URL validation passed: {url}")
            return True
        
        print(f"[UTILS] URL validation failed: {url}")
        return False
    
    def parse_xml(self, xml_data):
        """
        Parse XML data
        SECURITY ISSUE: XML External Entity (XXE) vulnerability
        """
        try:
            import xml.etree.ElementTree as ET
            
            # SECURITY ISSUE: Parsing XML without disabling external entities
            root = ET.fromstring(xml_data)
            
            result = {
                'tag': root.tag,
                'text': root.text,
                'attributes': root.attrib,
                'children': [child.tag for child in root]
            }
            
            print(f"[UTILS] Parsed XML: {result}")
            return result
            
        except Exception as e:
            print(f"[UTILS] XML parsing error: {e}")
            return {'error': str(e)}
    
    def generate_temp_file(self, content, suffix='.tmp'):
        """
        Generate temporary file
        SECURITY ISSUE: Insecure temporary file creation
        """
        try:
            # SECURITY ISSUE: Using predictable temporary file names
            temp_filename = f"temp_{self.generate_random_string(8)}{suffix}"
            temp_path = f"/tmp/{temp_filename}"
            
            with open(temp_path, 'w') as f:
                f.write(content)
            
            # SECURITY ISSUE: Setting permissive file permissions
            os.chmod(temp_path, 0o777)
            
            print(f"[UTILS] Created temporary file: {temp_path}")
            
            return {
                'success': True,
                'file_path': temp_path,
                'filename': temp_filename
            }
            
        except Exception as e:
            print(f"[UTILS] Temp file creation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def log_activity(self, activity, details):
        """
        Log activity
        SECURITY ISSUE: Insecure logging
        """
        # SECURITY ISSUE: Logging to world-readable file
        log_file = "/tmp/activity.log"
        
        try:
            with open(log_file, 'a') as f:
                log_entry = f"[{self.get_timestamp()}] {activity}: {details}\n"
                f.write(log_entry)
            
            # SECURITY ISSUE: Setting permissive log file permissions
            os.chmod(log_file, 0o666)
            
            print(f"[UTILS] Logged activity: {activity}")
            
        except Exception as e:
            print(f"[UTILS] Logging error: {e}")
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_system_info(self):
        """
        Get system information
        SECURITY ISSUE: Exposes sensitive system information
        """
        try:
            info = {
                'os': os.name,
                'platform': os.uname() if hasattr(os, 'uname') else 'unknown',
                'python_version': os.sys.version,
                'environment_variables': dict(os.environ),  # SECURITY ISSUE: Exposing all env vars
                'current_directory': os.getcwd(),
                'temp_directory': tempfile.gettempdir(),
                'user': os.getenv('USER', 'unknown'),
                'home': os.getenv('HOME', 'unknown'),
                'path': os.getenv('PATH', 'unknown')
            }
            
            print(f"[UTILS] Retrieved system information")
            return info
            
        except Exception as e:
            print(f"[UTILS] System info error: {e}")
            return {'error': str(e)}

# SECURITY ISSUE: Global utility instance
security_utils = SecurityUtils()
