import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class AIChef:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_recipe(self, query: str) -> dict:
        """
        Process a user query about a meal and return structured JSON:
        {
            "meal": "<meal name>",
            "steps": ["Step 1", "Step 2", ...]
        }
        """
        system_prompt = (
            "You are an expert chef assistant called AIChef. "
            "When a user asks about a meal or recipe, identify the name of the meal "
            "and list the steps to make it in a clean JSON format like this:\n\n"
            "{\n"
            '  "meal": "Meal Name",\n'
            '  "steps": ["Step 1", "Step 2", ...]\n'
            "}\n\n"
            "Do not include explanations or extra text — return ONLY valid JSON."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            if response.choices:
                raw_content = response.choices[0].message.content.strip()
            else:
                raw_content = ""

            # Attempt to parse the JSON safely
            recipe = json.loads(raw_content)

            # Validate the expected keys
            if "meal" not in recipe or "steps" not in recipe:
                raise ValueError("Missing 'meal' or 'steps' fields")

            return {"ok": True, "recipe": recipe}

        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "Invalid JSON returned by AI",
                "raw": raw_content,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
