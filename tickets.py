# storage.py
from queue import Queue


class RecipeStorage:
    # Stores all recipes keyed by meal name
    recipes = {}

    # Queue used for streaming new recipes
    events = Queue()

    @classmethod
    def add_recipe(cls, meal, steps):
        """Add or update a recipe and push it to the stream queue."""
        recipe = {
            "meal": meal,
            "steps": steps,
        }

        cls.recipes[meal] = recipe

        # push new recipe to SSE stream
        cls.events.put(recipe)

        return recipe

    @classmethod
    def get_recipe(cls, meal):
        """Retrieve a single recipe by meal name."""
        return cls.recipes.get(meal)

    @classmethod
    def get_all_recipes(cls):
        """Return all stored recipes."""
        return list(cls.recipes.values())

    @classmethod
    def pop_event(cls):
        """Block until a new recipe event is available."""
        return cls.events.get()

