from fastapi import FastAPI
from pydantic import BaseModel
from services import get_context, get_recommendation, save_recommendation

app = FastAPI(title='Motorcycle Cornering Decision Support Agent')

class RecommendationRequest(BaseModel):
    weather: dict
    date_time: str
    image_path: str

class SaveRecommendationRequest(BaseModel):
    conditions: dict
    scene: dict
    recommendation: dict

@app.get('/context')
def context():
    '''Get the current weather information, date and time, and available rider POV images'''
    return get_context()

@app.post('/recommendation')
async def recommendation(request: RecommendationRequest):
    '''Analyze the weather conditions, rider's POV, and relevant documentation, then recommend how to approach a curve'''
    return await get_recommendation(request.weather, request.date_time, request.image_path)

@app.post('/save_recommendation')
def save(request: SaveRecommendationRequest):
    '''Save the analysis of conditions and scene and the final recommendation to a CSV file'''
    save_recommendation(request.conditions, request.scene, request.recommendation)
    return {'status': 'success', 'message': 'Recommendation history saved successfully'}