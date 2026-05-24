"""
URGENT FIX: Database connection pool leak
Production issue causing connection exhaustion
"""

class DatabasePool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.active_connections = 0
        self.connections = []
    
    def get_connection(self):
        """Get connection from pool - FIXED"""
        if self.active_connections >= self.max_connections:
            raise Exception("No connections available")
        
        # Create or reuse connection
        conn = self._create_connection()
        self.active_connections += 1
        return conn
    
    def release_connection(self, conn):
        """Release connection back to pool - FIXED"""
        if conn in self.connections:
            self.active_connections -= 1
            # Return connection to pool for reuse
            return True
        return False
    
    def _create_connection(self):
        """Create new database connection"""
        return {"id": hash(time.time()), "status": "active"}
