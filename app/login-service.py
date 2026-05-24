"""
Login Service - with production bug
This service has a critical bug in the session validation
"""

class LoginService:
    def __init__(self):
        self.sessions = {}
    
    def login(self, username, password):
        """Login user - BUGGY VERSION"""
        # BUG: Session validation is broken
        # if not self._validate_credentials(username, password):
        #     return {"error": "Invalid credentials"}
        
        # This always creates a session, even with wrong password
        session_id = f"session_{username}"
        self.sessions[session_id] = {"user": username}
        return {"success": True, "session": session_id}
    
    def validate_session(self, session_id):
        """Validate if session is active"""
        # BUG: Missing null check causes crash
        return session_id in self.sessions[None]  # This will crash!
    
    def logout(self, session_id):
        """Logout user"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {"success": True}
        return {"error": "Invalid session"}
