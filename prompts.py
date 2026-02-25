from pydantic import BaseModel
from typing import Literal

# Describe riding conditions based on current weather, date, and time
def describe_conditions_prompt(weather: dict, date_time: str) -> str:
    prompt = f'''You are a motorcycle safety instructor and must assess the riding conditions given the current weather conditions. 
    The weather conditions are: {weather}, and it is {date_time}. You will assess the situation in terms of the following: 
    1. Road traction, considering temperature and precipitation; 
    2. Visibility, considering precipitation, the date, and the time of day; and 
    3. Likelihood of traffic, considering the date and time of day.'''
    return prompt


# Describe the situation based on an image of the rider's POV
describe_scene_prompt = f'''You are a motorcycle safety instructor and must assess a situation given a rider's POV of the road ahead. 
The image provided shows the rider's POV. You will assess the situation in terms of the following: 
1. Curve sharpness, considering the direction of the farthest visible part of the road; 
2. Visible curve length, considering how much of the curve is visible ahead; and 
3. The possibility of oncoming traffic, considering any adjacent lanes and their dividing lines.'''

# JSON structure for each response
class ConditionsResponse(BaseModel):
    traction: Literal['grippy', 'wet', 'icy']
    visibility: Literal['low', 'medium', 'high']
    traffic: Literal['light', 'moderate', 'heavy']

class SceneResponse(BaseModel):
    curve_sharpness: Literal['slight left', 'smooth left', 'sharp left', 'slight right', 'smooth right','sharp right', 'straight']
    visible_curve_length: Literal['fully visible', 'end obstructed', 'mostly obstructed']
    oncoming_traffic: Literal['present', 'possible', 'only same direction', 'single lane']