from pydantic import BaseModel
from typing import Literal


# JSON structure for each response
class ConditionsResponse(BaseModel):
    traction: Literal['grippy', 'wet', 'icy']
    visibility: Literal['low', 'medium', 'high']
    traffic: Literal['light', 'moderate', 'heavy']

class SceneResponse(BaseModel):
    curve_sharpness: Literal['slight left', 'smooth left', 'sharp left', 'slight right', 'smooth right','sharp right', 'straight']
    visible_curve_length: Literal['fully visible', 'obstructed near the end', 'mostly obstructed']
    oncoming_traffic: Literal['present', 'possible', 'only same direction', 'single lane']

class RecommendationResponse(BaseModel):
    entry_speed: Literal['well under speed limit', 'just under speed limit', 'at speed limit']
    braking: Literal['light, increasing if needed', 'even throughout', 'hard, releasing gradually']
    lean_angle: Literal['slight', 'medium', 'sharp']
    lane_position: Literal['inside', 'middle', 'outside']


# Describe riding conditions based on current weather, date, and time
def describe_conditions_prompt(weather: dict, date_time: str) -> str:
    prompt = f'''You are a motorcycle safety instructor and must assess the riding conditions given the current weather conditions. 
    The weather conditions are: 
    {weather}, 
    and it is {date_time}. 
    You will assess the situation in terms of the following: 
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


# Get relevant documentation from vector database based on current weather and scene conditions
def db_query(conditions: ConditionsResponse, scene: SceneResponse) -> str:
    query = f'''What techniques should a rider use to approach a curve with {conditions.traction} traction and {conditions.visibility} visibility, 
    when the curve is a {scene.curve_sharpness} curve and is {scene.visible_curve_length}?'''
    return query

# Recommend how to approach a curve based on the assessed conditions and situation
def recommend_approach_prompt(conditions: dict, scene: dict, context: str) -> str:
    prompt = f'''You are a motorcycle safety instructor and must recommend how to approach a curve based on the riding conditions and the situation. 
    You will be given documents relevant to the conditions and situation, and you must use that information to make your recommendations.
    The riding conditions are: 
    {conditions}, 
    and the situation is: 
    {scene}. 
    You will provide recommendations in terms of the following: 
    1. Entry speed, considering all factors but especially road traction; 
    2. Braking, considering all factors but especially curve sharpness, visible curve length, and entry speed; 
    3. Lean angle, considering all factors but especially curve sharpness and entry speed; and 
    4. Lane position, considering all factors but especially visibility and likelihood of oncoming traffic. 
    Use the following context to inform your recommendations: 
    {context}'''
    return prompt