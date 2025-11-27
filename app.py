from flask import Flask, jsonify, Response, stream_with_context
from config.logging import logger
from config.settings import settings
from routes import ask_routes
from flask_cors import CORS
from tickets import RecipeStorage
import time
import json


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])

    # Configure Flask settings

    # routes used for chef meal request #
    app.register_blueprint(ask_routes.bp, url_prefix="/ask")

    # Health check endpoint
    @app.route("/health")
    def health_check():
        """Health check endpoint"""
        from datetime import datetime

        return jsonify(
            {"status": "healthy", "version": "1.0.0", "timestamp": str(datetime.now())}
        ), 200

    @app.route("/")
    def home():
        return "Welcome to the Book Search API!"

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "status": 400}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found", "status": 404}), 404

    @app.errorhandler(413)
    def too_large(error):
        return jsonify({"error": "File too large", "status": 413}), 413

    @app.errorhandler(429)
    def rate_limit(error):
        return jsonify({"error": "Rate limit exceeded", "status": 429}), 429

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error", "status": 500}), 500

    # app.py

    @app.route("/stream-recipes")
    def stream_recipes():
        def event_stream():
            RECIPE_EVENTS = RecipeStorage.events
            while True:
                recipe = RECIPE_EVENTS.get()  # waits for new recipe
                yield f"data: {json.dumps(recipe)}\n\n"

        return Response(
            stream_with_context(event_stream()), mimetype="text/event-stream"
        )

    return app


if __name__ == "__main__":
    # Create Flask app
    app = create_app()

    # Display live indicator

    # Start server
    logger.info(f"Starting AI Chef server on port {settings.port}")
    app.run(
        host="0.0.0.0", port=settings.port, debug=(settings.flask_env == "development")
    )
