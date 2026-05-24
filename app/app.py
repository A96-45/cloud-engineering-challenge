"""
Cloud Cost Optimization Dashboard
Main application entry point
"""

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-not-for-production')

@app.route('/')
def index():
    """Dashboard home page"""
    return jsonify({
        'status': 'operational',
        'service': 'Cloud Cost Optimizer',
        'version': '1.0.0'
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }), 200

@app.route('/api/costs')
def get_costs():
    """Get cost data"""
    return jsonify({
        'total_monthly_cost': 5234.50,
        'services': {
            'compute': 2100.00,
            'storage': 1500.00,
            'network': 634.50
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=port)
