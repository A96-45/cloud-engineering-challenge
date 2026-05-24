"""
Login Service - FIXED VERSION
Critical security bug fixed in session validation
"""

class LoginService:
    def __init__(self):
        self.sessions = {}
    
    def _validate_credentials(self, username, password):
        """Validate username and password"""
        # In production, this would check against database
        return len(username) > 0 and len(password) >= 8
    
    def login(self, username, password):
        """Login user - FIXED"""
        if not self._validate_credentials(username, password):
            return {"error": "Invalid credentials", "success": False}
        
        session_id = f"session_{username}_{hash(password)}"
        self.sessions[session_id] = {"user": username, "authenticated": True}
        return {"success": True, "session": session_id}
    
    def validate_session(self, session_id):
        """Validate if session is active - FIXED"""
        # Fixed: Properly check if session exists
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        return session.get("authenticated", False)
    
    def logout(self, session_id):
        """Logout user"""
        if session_id in self.sessions:
            self.sessions[session_id]["authenticated"] = False
            del self.sessions[session_id]
            return {"success": True}
        return {"error": "Invalid session", "success": False}
