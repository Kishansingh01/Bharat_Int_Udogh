# Recommendation System

This folder contains the machine learning recommendation workflow for the storefront.

## Overview

The recommendation system uses a simple supervised pipeline to suggest product recommendations based on product and customer-related input features.

## Files

- `recommendation_pipeline.py` - Builds and trains the recommendation model
- `api.py` - FastAPI service that exposes recommendation predictions
- `verify_api.py` - Helper script to verify the API locally
- `data/brick_recommendations.csv` - Sample training data
- `models/brick_recommender.joblib` - Serialized trained model

## Setup

Install the Python dependencies:

```bash
pip install -r ../requirements-ml.txt
```

## Train the Model

Run:

```bash
python recommendation_pipeline.py
```

This will train the model and save it to the `models/` folder.

## Run the API

Start the recommendation API with:

```bash
python api.py
```

The service will be available at:

- http://127.0.0.1:8000/docs

## Verify the API

You can test the endpoint locally with:

```bash
python verify_api.py
```

## Notes

The current implementation is a starter recommendation pipeline and can be expanded with richer product data, better feature engineering, and a more advanced model over time.
