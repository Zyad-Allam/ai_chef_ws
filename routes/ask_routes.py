from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from config.logging import logger
from services.ai_chef import AIChef
from tickets import RecipeStorage
import time


bp = Blueprint("asking", __name__)
ai_chef = AIChef()


@bp.route("/", methods=["POST"])
def ask():
    """End point to start conversation with chatbot

    1. Action: ask
    Request:{
        "action": "ask",
        "query": "I'd like to have lasagna for dinner tonight",
        "user_id": "user_001"
    }
    Response:{
        "meal": "lasagna",
        "instructions": [{},{},{}],
        "steps": [{},{},{}]
    }
    """
    try:
        # validate request
        data = request.get_json()
        if not data:
            logger.error("Empty request, JSON data required")
            return jsonify("Empty request, JSON data required", 400)

        action = data.get("action", "ask")
        user = data.get("user_id", None)

        logger.info(f"received request with action {action} from user: {user}")

        start_time = time.time()
        logger.info(f"determining action: {action}")
        if action == "ask":
            response = _handle_ask(data)
        else:
            logger.error(f"Invalid action: {action}")
            return jsonify(
                {"error": f"Invalid action: {action}. Must be one of: ask,....for now"}
            ), 400
        # Add timing information
        duration_ms = int((time.time() - start_time) * 1000)

        # add recipe to storage
        logger.info(f"response: {response}")

        recipes_data = response.get("recipe")

        if isinstance(recipes_data, dict):
            # single recipe
            meal = recipes_data["meal"]
            steps = recipes_data["steps"]
            RecipeStorage.add_recipe(meal, steps)
            logger.info(f"Recipe added to storage: {recipes_data}")

        elif isinstance(recipes_data, list):
            # multiple recipes
            for recipe in recipes_data:
                meal = recipe["meal"]
                steps = recipe["steps"]
                RecipeStorage.add_recipe(meal, steps)
                logger.info(f"Recipe added to storage: {recipe}")

        else:
            logger.error(f"Unexpected recipe format: {type(recipes_data)}")

        logger.info(
            f"User {action} action processed successfully in {duration_ms}ms",
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Asking endpoint error: {e}", {"error": str(e)})
        return jsonify({"ok": False, "error": "Internal server error"}), 500


def _handle_ask(data: dict) -> dict:
    """Handle 'ask' action"""
    required_fields = ["user_id", "query"]
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field for 'ask' action {field}")
            return {"ok": False, "error": f"Missing required field: {field}"}

    query = data["query"]
    result = ai_chef.generate_recipe(query)
    return result
