"""Main Flask application entry point"""

from flask import Flask, session
from flask_cors import CORS
from routes.stock_routes import stock_bp
from routes.user_routes import user_bp
from routes.shop_routes import shop_bp
from routes.mommy_routes import mommy_bp
from routes.advice_routes import advice_bp
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from routes.alert_routes import alert_bp
from routes.analytics_routes import analytics_bp
from routes.leaderboard_routes import leaderboard_bp
import database  # Initialize database connection
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Lax works for same-site requests
app.config['SESSION_COOKIE_SECURE'] = False  # False for localhost HTTP, True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours in seconds
app.config['SESSION_COOKIE_DOMAIN'] = None  # Allow cookies for localhost and 127.0.0.1
app.config['SESSION_COOKIE_PATH'] = '/'  # Ensure cookie is available for all paths

# Initialize MongoDB connection
try:
    db = database.db  # This will establish the connection
    print("MongoDB connection initialized")
except Exception as e:
    print(f"Warning: MongoDB connection failed: {e}")
    print("   The app will continue but database operations may fail.")

# Configure CORS with credentials support for sessions
# Note: When using credentials, you must specify exact origins, not "*"
# Add your frontend URL here if it's different
frontend_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5000",  # In case frontend proxies through backend
    "http://127.0.0.1:5000",
]

CORS(app, resources={
    r"/api/*": {
        "origins": frontend_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,  # Not needed with JWT tokens
        "expose_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(user_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(mommy_bp)
app.register_blueprint(advice_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
