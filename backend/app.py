"""Main Flask application entry point"""

from flask import Flask
from flask_cors import CORS
from routes.stock_routes import stock_bp
from routes.user_routes import user_bp
from routes.shop_routes import shop_bp
from routes.mommy_routes import mommy_bp
from routes.advice_routes import advice_bp

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(stock_bp)
app.register_blueprint(user_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(mommy_bp)
app.register_blueprint(advice_bp)

if __name__ == "__main__":
    app.run(debug=True)
