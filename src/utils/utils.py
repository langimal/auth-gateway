# utils.py

import hashlib
import hmac
import base64
import json
import os
import secrets
import string
from cryptography.fernet import Fernet
from flask import current_app
from auth_gateway.config import Config

def generate_salt(length=32):
    """Generate a cryptographically secure random string of a specified length."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

def generate_fernet_key():
    """Generate a Fernet key for encryption."""
    return Fernet.generate_key()

def encrypt_data(data):
    """Encrypt data using the Fernet key stored in the config."""
    fernet_key = current_app.config['FERNET_KEY']
    cipher_suite = Fernet(fernet_key)
    return cipher_suite.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data):
    """Decrypt data using the Fernet key stored in the config."""
    fernet_key = current_app.config['FERNET_KEY']
    cipher_suite = Fernet(fernet_key)
    return cipher_suite.decrypt(encrypted_data).decode('utf-8')

def verify_token(token, secret_key):
    """Verify a token using HMAC and SHA256."""
    expected_token = hmac.new(secret_key.encode('utf-8'), token.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac.compare_digest(token, expected_token)

def generate_verification_token(secret_key, user_id):
    """Generate a verification token for a user."""
    payload = {'user_id': user_id}
    return base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')

def get_config_value(key):
    """Get a config value from the .env file."""
    return os.getenv(key, None)

def load_config():
    """Load the config from the .env file."""
    return Config.from_envvar('AUTH_GATEWAY_CONFIG_FILE')