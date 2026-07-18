from fastapi.testclient import TestClient
from api import app

client = TestClient(app)
response = client.post('/recommend', json={
    'constructionType': 'Residential',
    'budget': 12000,
    'requiredStrength': 'High',
    'durability': 'High',
    'brickPrice': 9,
    'brickQuality': 'Premium',
    'customerPreference': 'Durability',
    'previousOrders': 2,
})
print(response.status_code)
print(response.text)
