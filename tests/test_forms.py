from django.test import TestCase
from predictor.forms import PredictionForm

class FormTest(TestCase):
    def test_form_creation(self):
        form=PredictionForm()
        self.assertTrue(form.fields)
