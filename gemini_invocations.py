from dotenv import load_dotenv
import os
from weather import get_zip_code, get_weather_info
from read_images import read_image_choice
from prompts import describe_situation_prompt
from google import genai
from google.genai import types
from ast import literal_eval


load_dotenv()
api_key = os.getenv('API_KEY')

def describe_situation() -> dict:
    client = genai.Client(api_key=api_key)
    zip_code = get_zip_code()
    weather = get_weather_info(zip_code)
    image = read_image_choice()
    prompt = describe_situation_prompt(weather)

    response = client.models.generate_content(
        model="gemini-robotics-er-1.5-preview",
        contents=[
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

    response_dict = '{' + response.text.split('{', 1)[1].split('}', 1)[0] + '}'
    response_dict = literal_eval(response_dict)
    return response_dict