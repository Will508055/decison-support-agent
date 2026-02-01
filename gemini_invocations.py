from dotenv import load_dotenv
import os
from weather import get_zip_code, get_weather_info
from date_time import get_date_time
from read_images import read_image_choice
from prompts import describe_conditions_prompt, describe_scene_prompt
from google import genai
from google.genai import types
from ast import literal_eval

# Get prompt inputs
zip_code = get_zip_code()
current_weather = get_weather_info(zip_code)
current_date_time = get_date_time()

# Initialize Gemini client
load_dotenv()
api_key = os.getenv('API_KEY')
client = genai.Client(api_key=api_key)

# Describe current riding conditions
def describe_conditions() -> dict:
    prompt = describe_conditions_prompt(current_weather, current_date_time)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level='low')
        )
    )
    try:
        response_dict = '{' + response.text.split('{', 1)[1].split('}', 1)[0] + '}'
        response_dict = literal_eval(response_dict)
        return response_dict
    except Exception as e:
        print(f'Error parsing LLM environmental assessment: {e}')
        return {}


# Describe situation from image
def describe_scene(image: bytes) -> dict:
    prompt = describe_scene_prompt
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
    try:
        response_dict = '{' + response.text.split('{', 1)[1].split('}', 1)[0] + '}'
        response_dict = literal_eval(response_dict)
        return response_dict
    except Exception as e:
        print(f'Error parsing LLM environmental assessment: {e}')
        return {}
