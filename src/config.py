#!/usr/bin/env python3
"""
Configuration module with hardcoded secrets
SECURITY ISSUE: Contains hardcoded credentials and sensitive configuration
"""

import os

class Config:
    """
    Application configuration class
    SECURITY ISSUE: Hardcoded secrets and credentials
    """
    
    # SECURITY ISSUE: Hardcoded secret key
    SECRET_KEY = "REPLACE_ME_SECRET_KEY"
    
    # SECURITY ISSUE: Hardcoded database configuration
    DATABASE_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'username': 'admin',
        'password': 'REPLACE_ME_DB_PASSWORD',  # SECURITY ISSUE: Hardcoded password
        'database': 'visionone_demo',
        'ssl_mode': 'disable'  # SECURITY ISSUE: SSL disabled
    }
    
    # SECURITY ISSUE: Hardcoded AWS credentials (FAKE - for testing only)
    AWS_CONFIG = {
        'access_key_id': 'REPLACE_ME_AWS_ACCESS_KEY_ID',
        'secret_access_key': 'REPLACE_ME_AWS_SECRET_ACCESS_KEY',
        'region': 'us-west-2',
        'bucket': 'vision-one-demo-bucket'
    }
    
    # SECURITY ISSUE: Hardcoded API keys (FAKE - for testing only)
    API_KEYS = {
        'vision_one': 'REPLACE_ME_VISION_ONE_API_KEY',
        'github': 'REPLACE_ME_GITHUB_TOKEN',
        'slack_webhook': 'https://hooks.slack.com/services/REPLACE_ME',
        'openai': 'REPLACE_ME_OPENAI_API_KEY',
        'stripe': 'REPLACE_ME_STRIPE_API_KEY'
    }
    
    # SECURITY ISSUE: Hardcoded JWT configuration
    JWT_CONFIG = {
        'secret': 'REPLACE_ME_JWT_SECRET',
        'algorithm': 'HS256',
        'expiration_hours': 24
    }
    
    # SECURITY ISSUE: Hardcoded encryption keys
    ENCRYPTION_CONFIG = {
        'key': 'REPLACE_ME_ENCRYPTION_KEY',  # SECURITY ISSUE: Hardcoded encryption key
        'iv': 'REPLACE_ME_IV',      # SECURITY ISSUE: Hardcoded IV
        'salt': 'salt-for-password-hashing-fake'     # SECURITY ISSUE: Hardcoded salt
    }
    
    # SECURITY ISSUE: Insecure application settings
    APP_CONFIG = {
        'debug': True,           # SECURITY ISSUE: Debug mode enabled
        'testing': False,
        'host': '0.0.0.0',      # SECURITY ISSUE: Binding to all interfaces
        'port': 5000,
        'threaded': True,
        'ssl_context': None      # SECURITY ISSUE: No SSL/TLS
    }
    
    # SECURITY ISSUE: Hardcoded third-party service credentials
    THIRD_PARTY_SERVICES = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'password': 'redis_password_123',  # SECURITY ISSUE: Hardcoded Redis password
            'db': 0
        },
        'elasticsearch': {
            'host': 'localhost',
            'port': 9200,
            'username': 'elastic',
            'password': 'elastic_password_456'  # SECURITY ISSUE: Hardcoded Elasticsearch password
        },
        'mongodb': {
            'host': 'localhost',
            'port': 27017,
            'username': 'mongo_user',
            'password': 'mongo_password_789'    # SECURITY ISSUE: Hardcoded MongoDB password
        }
    }
    
    # SECURITY ISSUE: Hardcoded LDAP configuration
    LDAP_CONFIG = {
        'server': 'ldap://localhost:389',
        'bind_dn': 'cn=admin,dc=example,dc=com',
        'bind_password': 'ldap_admin_password',  # SECURITY ISSUE: Hardcoded LDAP password
        'base_dn': 'dc=example,dc=com',
        'use_ssl': False  # SECURITY ISSUE: LDAP without SSL
    }
    
    # SECURITY ISSUE: Hardcoded SMTP configuration
    SMTP_CONFIG = {
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': 'demo@example.com',
        'password': 'smtp_password_fake',  # SECURITY ISSUE: Hardcoded SMTP password
        'use_tls': True
    }
    
    def __init__(self):
        """Initialize configuration"""
        # SECURITY ISSUE: Loading sensitive data in constructor
        self.load_secrets()
    
    def load_secrets(self):
        """
        Load secrets from various sources
        SECURITY ISSUE: Demonstrates multiple ways secrets can be exposed
        """
        # SECURITY ISSUE: Reading secrets from environment without validation
        self.runtime_secrets = {
            'db_password': os.getenv('DB_PASSWORD', self.DATABASE_CONFIG['password']),
            'api_key': os.getenv('API_KEY', self.API_KEYS['vision_one']),
            'aws_key': os.getenv('AWS_ACCESS_KEY_ID', self.AWS_CONFIG['access_key_id'])
        }
        
        # SECURITY ISSUE: Logging sensitive information
        print(f"[CONFIG] Loaded secrets: {self.runtime_secrets}")
    
    def get_database_url(self):
        """
        Get database connection URL
        SECURITY ISSUE: Returns URL with embedded credentials
        """
        config = self.DATABASE_CONFIG
        return f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    
    def get_redis_url(self):
        """
        Get Redis connection URL
        SECURITY ISSUE: Returns URL with embedded credentials
        """
        config = self.THIRD_PARTY_SERVICES['redis']
        return f"redis://:{config['password']}@{config['host']}:{config['port']}/{config['db']}"
    
    def export_config(self):
        """
        Export configuration for debugging
        SECURITY ISSUE: Exports all configuration including secrets
        """
        return {
            'secret_key': self.SECRET_KEY,
            'database': self.DATABASE_CONFIG,
            'aws': self.AWS_CONFIG,
            'api_keys': self.API_KEYS,
            'jwt': self.JWT_CONFIG,
            'encryption': self.ENCRYPTION_CONFIG,
            'app': self.APP_CONFIG,
            'third_party': self.THIRD_PARTY_SERVICES,
            'ldap': self.LDAP_CONFIG,
            'smtp': self.SMTP_CONFIG,
            'runtime_secrets': self.runtime_secrets
        }

# SECURITY ISSUE: Global configuration instance with secrets
config_instance = Config()

# SECURITY ISSUE: Exposing configuration as module-level variables
SECRET_KEY = config_instance.SECRET_KEY
DATABASE_URL = config_instance.get_database_url()
AWS_ACCESS_KEY = config_instance.AWS_CONFIG['access_key_id']
AWS_SECRET_KEY = config_instance.AWS_CONFIG['secret_access_key']
