import os
from . import weather
from . import date_time
from dotenv import load_dotenv
from . import prompts
from google import genai
from google.genai import types

# Get prompt inputs
zip_code = weather.get_zip_code()
current_weather = weather.get_weather_info(zip_code)
current_date_time = date_time.get_date_time()

# Initialize Gemini client
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=api_key)


# Describe riding conditions based on current weather, date, and time
async def describe_conditions() -> dict[str, str]:
    prompt = prompts.describe_conditions_prompt(current_weather, current_date_time)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level='low'),
            response_mime_type='application/json',
            response_json_schema=prompts.ConditionsResponse.model_json_schema(),
        )
    )
    #return parse_llm_response(response.text)
    return prompts.ConditionsResponse.model_validate_json(response.text)


# Describe the situation based on an image of the rider's POV
async def describe_scene(image: bytes) -> dict[str, str]:
    prompt = prompts.describe_scene_prompt
    response = client.models.generate_content(
        model="gemini-robotics-er-1.5-preview",
        contents = [
            types.Part.from_bytes(
                data=image,
                mime_type='image/png',
            ),
            prompt
        ],
        config = types.GenerateContentConfig(
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type='application/json',
            response_json_schema=prompts.SceneResponse.model_json_schema(),
        )
    )
    return prompts.SceneResponse.model_validate_json(response.text)


# Recommend how to approach a curve based on the assessed conditions and situation
def recommend_approach(conditions: dict[str, str], scene: dict[str, str], context: str) -> dict[str, str]:
    prompt = prompts.recommend_approach_prompt(conditions, scene, context)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level='medium'),
            response_mime_type='application/json',
            response_json_schema=prompts.RecommendationResponse.model_json_schema(),
        )
    )
    return prompts.RecommendationResponse.model_validate_json(response.text)