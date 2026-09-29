import json
import requests
from backend.config import AI_API_URL, AI_API_KEY, AI_MODEL

FOODS = {
    "vegetarian": {
        "breakfast": ["vegetable poha with curd", "oats with fruit and nuts"],
        "lunch": ["dal, rice, mixed vegetables and salad", "roti, chana and vegetables"],
        "snack": ["fruit with yogurt", "roasted chickpeas"],
        "dinner": ["vegetable khichdi with curd", "paneer and mixed vegetables with roti"],
    },
    "vegan": {
        "breakfast": ["oats with banana and seeds", "vegetable poha with fruit"],
        "lunch": ["dal, rice, vegetables and salad", "chickpea roti bowl with vegetables"],
        "snack": ["fruit and roasted chickpeas", "nuts and fruit"],
        "dinner": ["lentil khichdi with vegetables", "tofu and mixed vegetables with roti"],
    },
    "non-vegetarian": {
        "breakfast": ["vegetable omelette with whole-grain toast", "oats with fruit and yogurt"],
        "lunch": ["rice, lentils, vegetables and grilled chicken", "roti, vegetables and egg curry"],
        "snack": ["fruit with yogurt", "roasted chickpeas and fruit"],
        "dinner": ["vegetable soup with chicken and roti", "rice, vegetables and fish"],
    },
}

def _key(pref):
    pref = (pref or "vegetarian").lower()
    if "vegan" in pref:
        return "vegan"
    if "non" in pref or "egg" in pref or "chicken" in pref:
        return "non-vegetarian"
    return "vegetarian"

def local_plan(profile):
    foods = FOODS[_key(profile.get("dietary_preference"))]
    goal = profile.get("goal") or "general balanced eating"
    activity = profile.get("activity_level") or "moderate"
    allergy_note = profile.get("allergies") or "No demo exclusions supplied."

    # This intentionally avoids clinical calorie prescriptions.
    return {
        "breakfast": foods["breakfast"][0],
        "lunch": foods["lunch"][0],
        "snack": foods["snack"][0],
        "dinner": foods["dinner"][0],
        "nutrition_summary": (
            f"General wellness example for the demo goal '{goal}' and activity "
            f"level '{activity}'. Aim for variety across food groups, regular meals, "
            f"and hydration according to personal needs. Demo exclusions: {allergy_note}"
        ),
        "source": "local_rule_based_fallback",
        "disclaimer": "Educational/general wellness example, not medical advice.",
    }

def _call_optional_ai(profile):
    if not (AI_API_URL and AI_API_KEY and AI_MODEL):
        return None

    prompt = {
        "task": "Create a general educational meal-plan example, not medical advice.",
        "profile": {
            "activity_level": profile.get("activity_level"),
            "dietary_preference": profile.get("dietary_preference"),
            "goal": profile.get("goal"),
            "preferences_or_allergies": profile.get("allergies"),
        },
        "required_fields": [
            "breakfast", "lunch", "snack", "dinner", "nutrition_summary"
        ],
    }
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": AI_MODEL, "input": json.dumps(prompt)}
    try:
        response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Accept a simple structured response from a compatible endpoint.
        if all(k in data for k in ["breakfast", "lunch", "snack", "dinner"]):
            data["nutrition_summary"] = data.get("nutrition_summary", "")
            data["source"] = "optional_ai_api"
            data["disclaimer"] = "Educational/general wellness example, not medical advice."
            return data
    except (requests.RequestException, ValueError, TypeError):
        return None
    return None

def generate_plan(profile):
    return _call_optional_ai(profile) or local_plan(profile)
