"""
Authentication Module - Enhanced for Exercise 4
Demonstrates code review improvements and collaborative development
"""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

class User:
    """User authentication and management"""
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.password_hash = None
        self.created_at = datetime.now()
        self.last_login = None
    
    def set_password(self, password: str) -> bool:
        """Hash and store password securely"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        return True
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        if not self.password_hash:
            return False
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
    
    def record_login(self) -> None:
        """Record successful login timestamp"""
        self.last_login = datetime.now()
    
    def get_account_age(self) -> timedelta:
        """Return how long account has existed"""
        return datetime.now() - self.created_at


class AuthenticationManager:
    """Manages user authentication and session handling"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def register_user(self, username: str, email: str, password: str) -> bool:
        """Register a new user"""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        
        user = User(username, email)
        user.set_password(password)
        self.users[username] = user
        return True
    
    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user and create session"""
        if username not in self.users:
            raise ValueError(f"User {username} not found")
        
        user = self.users[username]
        if not user.verify_password(password):
            raise ValueError("Invalid password")
        
        user.record_login()
        session_token = hashlib.sha256(
            f"{username}{datetime.now()}".encode()
        ).hexdigest()
        
        self.sessions[session_token] = {
            'username': username,
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        return {
            'token': session_token,
            'username': username,
            'email': user.email
        }
    
    def validate_session(self, token: str) -> bool:
        """Validate if session token is active"""
        if token not in self.sessions:
            return False
        
        session = self.sessions[token]
        # Session expires after 24 hours
        if datetime.now() - session['created_at'] > timedelta(hours=24):
            del self.sessions[token]
            return False
        
        session['last_activity'] = datetime.now()
        return True
    
    def logout(self, token: str) -> bool:
        """Invalidate session token"""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False


# Code review improvements implemented:
# 1. Added type hints for better clarity
# 2. Implemented proper password hashing (SHA256 for demo)
# 3. Added session management with expiration
# 4. Better error messages
# 5. Docstrings for all methods
