def describe_situation_prompt(weather: dict) -> str:
    prompt = f'''You are a motorcycle safety instructor and must assess a situation given a rider's POV of the road ahead 
    and the current weather conditions. The image provided shows the rider's POV, and the current weather conditions are: 
    {weather}. You will assess the situation in terms of the following: 
    1. Road traction, considering the surface type and weather conditions, 
    2. Curve shape, considering only the road that is visible ahead, 
    3. Visibility, considering how far ahead is visible and the weather conditions, and 
    4. The possibility of oncoming traffic, considering the lanes in the road. 
    You will return your response in the following Python dictionary format, 
    only selecting one value from the list of values for each key: 
    {{ 
    'road': ['grippy', 'wet', 'icy', 'gravel'], 
    'curve': ['slight left', 'smooth left', 'sharp left', 'slight right', 'smooth right','sharp right', 'straight'], 
    'visibility': ['low', 'medium', 'high'], 
    'oncoming_traffic': ['present', 'absent'] 
    }}'''
    return prompt