from django.test import TestCase
from predictor.models import PredictionHistory

class PredictionHistoryModelTest(TestCase):
    def test_model_exists(self):
        self.assertTrue(PredictionHistory)
