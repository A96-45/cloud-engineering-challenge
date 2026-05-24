"""
Authentication API Endpoints
Demonstrates REST API implementation for authentication
"""

from flask import Flask, request, jsonify
from authentication import AuthenticationManager

app = Flask(__name__)
auth_manager = AuthenticationManager()

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        auth_manager.register_user(username, email, password)
        return jsonify({'message': 'User registered successfully'}), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return session token"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing credentials'}), 400
        
        result = auth_manager.authenticate(username, password)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/validate', methods=['POST'])
def validate():
    """Validate session token"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Missing token'}), 400
        
        is_valid = auth_manager.validate_session(token)
        return jsonify({'valid': is_valid}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user and invalidate token"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Missing token'}), 400
        
        success = auth_manager.logout(token)
        if success:
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'error': 'Invalid token'}), 400
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
