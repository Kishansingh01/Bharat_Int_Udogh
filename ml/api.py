from fastapi import FastAPI
from pydantic import BaseModel

try:
    from .recommendation_pipeline import predict_recommendation
except ImportError:  # pragma: no cover - allows running the module directly
    from recommendation_pipeline import predict_recommendation

app = FastAPI(title='Brick Recommendation API', version='1.0.0')


class RecommendationRequest(BaseModel):
    constructionType: str
    budget: float
    requiredStrength: str
    durability: str
    brickPrice: float
    brickQuality: str
    customerPreference: str
    previousOrders: int = 0


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/recommend')
def recommend(request: RecommendationRequest):
    payload = request.model_dump()
    return predict_recommendation(payload)
