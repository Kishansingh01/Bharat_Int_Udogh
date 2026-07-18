from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / 'data' / 'brick_recommendations.csv'
MODEL_PATH = ROOT / 'models' / 'brick_recommender.joblib'

FEATURE_COLUMNS = [
    'constructionType',
    'budget',
    'requiredStrength',
    'durability',
    'brickPrice',
    'brickQuality',
    'customerPreference',
    'previousOrders',
]

TARGET_COLUMN = 'recommendedBrick'


def ensure_dataset() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DATA_PATH.exists():
        return

    sample_rows = [
        {'constructionType': 'Residential', 'budget': 12000, 'requiredStrength': 'High', 'durability': 'High', 'brickPrice': 9, 'brickQuality': 'Premium', 'customerPreference': 'Aesthetic', 'previousOrders': 3, 'recommendedBrick': 'प्रथम श्रेणी सामान्य ईंट'},
        {'constructionType': 'Residential', 'budget': 14000, 'requiredStrength': 'High', 'durability': 'High', 'brickPrice': 10, 'brickQuality': 'Premium', 'customerPreference': 'Durability', 'previousOrders': 4, 'recommendedBrick': 'प्रथम श्रेणी सामान्य ईंट (उच्च गुणवत्ता)'},
        {'constructionType': 'Residential', 'budget': 10000, 'requiredStrength': 'Medium', 'durability': 'Medium', 'brickPrice': 8, 'brickQuality': 'Standard', 'customerPreference': 'Budget', 'previousOrders': 2, 'recommendedBrick': 'द्वितीय श्रेणी ईंट'},
        {'constructionType': 'Residential', 'budget': 8000, 'requiredStrength': 'Low', 'durability': 'Low', 'brickPrice': 7, 'brickQuality': 'Basic', 'customerPreference': 'Cost', 'previousOrders': 1, 'recommendedBrick': 'तृतीय श्रेणी ईंट'},
        {'constructionType': 'Commercial', 'budget': 11000, 'requiredStrength': 'High', 'durability': 'High', 'brickPrice': 9, 'brickQuality': 'Premium', 'customerPreference': 'Durability', 'previousOrders': 2, 'recommendedBrick': 'प्रथम श्रेणी सामान्य ईंट'},
        {'constructionType': 'Commercial', 'budget': 9000, 'requiredStrength': 'Medium', 'durability': 'Medium', 'brickPrice': 8, 'brickQuality': 'Standard', 'customerPreference': 'Budget', 'previousOrders': 1, 'recommendedBrick': 'द्वितीय श्रेणी ईंट'},
        {'constructionType': 'Commercial', 'budget': 7000, 'requiredStrength': 'Low', 'durability': 'Low', 'brickPrice': 6, 'brickQuality': 'Basic', 'customerPreference': 'Cost', 'previousOrders': 2, 'recommendedBrick': 'चतुर्थ श्रेणी ईंट'},
        {'constructionType': 'Commercial', 'budget': 8500, 'requiredStrength': 'Medium', 'durability': 'Medium', 'brickPrice': 7, 'brickQuality': 'Basic', 'customerPreference': 'Budget', 'previousOrders': 2, 'recommendedBrick': 'तृतीय श्रेणी ईंट'},
        {'constructionType': 'Industrial', 'budget': 13000, 'requiredStrength': 'High', 'durability': 'High', 'brickPrice': 10, 'brickQuality': 'Premium', 'customerPreference': 'Durability', 'previousOrders': 5, 'recommendedBrick': 'प्रथम श्रेणी सामान्य ईंट'},
        {'constructionType': 'Industrial', 'budget': 10000, 'requiredStrength': 'Medium', 'durability': 'Medium', 'brickPrice': 8, 'brickQuality': 'Standard', 'customerPreference': 'Budget', 'previousOrders': 3, 'recommendedBrick': 'द्वितीय श्रेणी ईंट'},
        {'constructionType': 'Industrial', 'budget': 6000, 'requiredStrength': 'Low', 'durability': 'Low', 'brickPrice': 5, 'brickQuality': 'Basic', 'customerPreference': 'Cost', 'previousOrders': 2, 'recommendedBrick': 'चतुर्थ श्रेणी ईंट'},
        {'constructionType': 'Industrial', 'budget': 7500, 'requiredStrength': 'Low', 'durability': 'Low', 'brickPrice': 6, 'brickQuality': 'Basic', 'customerPreference': 'Budget', 'previousOrders': 2, 'recommendedBrick': 'तृतीय श्रेणी ईंट'},
    ]
    pd.DataFrame(sample_rows).to_csv(DATA_PATH, index=False)


def load_dataset() -> pd.DataFrame:
    ensure_dataset()
    return pd.read_csv(DATA_PATH)


def build_feature_vector(input_payload: Dict[str, Any]) -> List[Any]:
    return [
        input_payload.get('constructionType'),
        input_payload.get('budget'),
        input_payload.get('requiredStrength'),
        input_payload.get('durability'),
        input_payload.get('brickPrice'),
        input_payload.get('brickQuality'),
        input_payload.get('customerPreference'),
        input_payload.get('previousOrders', 0),
    ]


def prepare_training_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y


def train_model(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    if df is None:
        df = load_dataset()

    X, y = prepare_training_data(df)

    numeric_features = ['budget', 'brickPrice', 'previousOrders']
    categorical_features = [
        'constructionType',
        'requiredStrength',
        'durability',
        'brickQuality',
        'customerPreference',
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='median'), numeric_features),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
            ]), categorical_features),
        ]
    )

    clf = Pipeline(
        steps=[
            ('preprocess', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)

    return {
        'model_path': str(MODEL_PATH),
        'accuracy': float((predictions == y_test).mean()),
        'classification_report': report,
        'confusion_matrix': cm.tolist(),
        'classes': list(clf.classes_),
    }


def load_model(path: Optional[str] = None) -> Any:
    model_path = Path(path or MODEL_PATH)
    if not model_path.exists():
        train_model()
    return joblib.load(model_path)


def predict_recommendation(payload: Dict[str, Any], model: Optional[Any] = None) -> Dict[str, Any]:
    if model is None:
        model = load_model()

    features = pd.DataFrame([build_feature_vector(payload)], columns=FEATURE_COLUMNS)
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_

    ranking = sorted(
        zip(classes, probabilities),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        'recommendedBrick': prediction,
        'confidence': float(max(probabilities)),
        'rankedOptions': [
            {'brick': brick, 'confidence': float(conf)} for brick, conf in ranking[:5]
        ],
    }


def rank_products(products: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    scored = []
    budget = preferences.get('budget', 10000)
    for product in products:
        price = product.get('price', 0)
        score = 0
        if price <= budget:
            score += 3
        if product.get('category') in {'प्रथम श्रेणी ईंट', 'प्रथम श्रेणी ईंट (उच्च गुणवत्ता)'}:
            score += 2
        if preferences.get('requiredStrength') == 'High' and product.get('category') in {'प्रथम श्रेणी ईंट', 'प्रथम श्रेणी ईंट (उच्च गुणवत्ता)'}:
            score += 2
        if price <= budget - 1000:
            score += 1
        scored.append({**product, 'score': score})
    return sorted(scored, key=lambda item: (-item['score'], item['price']))


if __name__ == '__main__':
    result = train_model()
    print(json.dumps(result, indent=2))
