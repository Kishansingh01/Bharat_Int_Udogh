# ML Recommendation System for Brick Sales

## Overview

This project now includes a lightweight machine learning recommendation flow for brick suggestions.

## Components

- ml/recommendation_pipeline.py: training, serialization, and prediction logic
- ml/api.py: FastAPI service exposing /health and /recommend
- app/api/recommend/route.ts: Next.js proxy route to the Python service
- components/RecommendationWidget.tsx: customer-facing recommendation form
- app/recommendation-demo/page.tsx: standalone demo page
- app/shop/page.tsx: the widget is embedded into the shop experience

## Quick start

1. Install Python dependencies:
   - C:/Users/desktop/AppData/Local/Programs/Python/Python312/python.exe -m pip install -r requirements-ml.txt
2. Train the model:
   - C:/Users/desktop/AppData/Local/Programs/Python/Python312/python.exe ml/recommendation_pipeline.py
3. Start the API:
   - C:/Users/desktop/AppData/Local/Programs/Python/Python312/python.exe -m uvicorn ml.api:app --reload --port 8000
4. Start the Next.js app:
   - npm run dev
5. Open http://localhost:3000/shop or http://localhost:3000/recommendation-demo

## Data and retraining

The initial model uses a small starter dataset stored in ml/data/brick_recommendations.csv.
As real interactions are collected, append rows with the same schema and retrain the model by rerunning the training script.

## Suggested schema for real data

- constructionType
- budget
- requiredStrength
- durability
- brickPrice
- brickQuality
- customerPreference
- previousOrders
- recommendedBrick
