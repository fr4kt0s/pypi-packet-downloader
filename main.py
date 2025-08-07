from flask import Flask
from scripts.webserver import bp as web_bp

# Create the Flask application instance
app = Flask(__name__)

# Secret key for securely signing the session cookie
# (In production, use a strong, random value and keep it secret)
app.secret_key = "your_secret_key_here"

# Register the blueprint defined in webserver.py
app.register_blueprint(web_bp)


if __name__ == "__main__":
    # Start the Flask development server
    # Accessible from all interfaces (0.0.0.0), port 5000
    app.run(host="0.0.0.0", port=5000)

    # NOTE: This is not suitable for production environments.
    # For production, use a WSGI server like Gunicorn or uWSGI.