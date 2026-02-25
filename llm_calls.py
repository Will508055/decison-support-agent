import os
import weather
import date_time
from dotenv import load_dotenv
import prompts
from google import genai
from google.genai import types
from ast import literal_eval

# Get prompt inputs
zip_code = weather.get_zip_code()
current_weather = weather.get_weather_info(zip_code)
current_date_time = date_time.get_date_time()

# Initialize Gemini client
load_dotenv()
api_key = os.getenv('API_KEY')
client = genai.Client(api_key=api_key)

# Parse JSON-like response from LLM
def parse_llm_response(response: str) -> dict[str, str]:
    try:
        response_dict = '{' + response.split('{', 1)[1].split('}', 1)[0] + '}'
        response_dict = literal_eval(response_dict)
        for key, value in response_dict.items():
            if isinstance(value, list):
                response_dict[key] = value[0]
        return response_dict
    except Exception as e:
        print(f'Error parsing LLM response: {e}')
        return {}

# Describe current riding conditions
async def describe_conditions() -> dict[str, str]:
    prompt = prompts.describe_conditions_prompt(current_weather, current_date_time)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level='low')
        )
    )
    return parse_llm_response(response.text)


# Describe situation from image
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
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    return parse_llm_response(response.text)
