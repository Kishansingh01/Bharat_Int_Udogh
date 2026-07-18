import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from recommendation_pipeline import build_feature_vector, rank_products


class RecommendationPipelineTests(unittest.TestCase):
    def test_build_feature_vector_uses_expected_fields(self):
        payload = {
            'constructionType': 'Residential',
            'budget': 12000,
            'requiredStrength': 'High',
            'durability': 'High',
            'brickPrice': 9,
            'brickQuality': 'Premium',
            'customerPreference': 'Aesthetic',
            'previousOrders': 3,
        }
        vector = build_feature_vector(payload)
        self.assertEqual(len(vector), 8)
        self.assertEqual(vector[0], 'Residential')
        self.assertEqual(vector[1], 12000)

    def test_rank_products_returns_sorted_recommendations(self):
        products = [
            {'id': '1', 'name': 'First', 'price': 9, 'category': 'Premium'},
            {'id': '2', 'name': 'Second', 'price': 8, 'category': 'Standard'},
        ]
        ranked = rank_products(products, {'budget': 10000})
        self.assertEqual(ranked[0]['id'], '2')


if __name__ == '__main__':
    unittest.main()
