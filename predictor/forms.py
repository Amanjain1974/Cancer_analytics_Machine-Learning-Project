from django import forms

RACE_CHOICES = [
    ("Asian", "Asian"),
    ("Caucasian", "Caucasian"),
    ("Hispanic", "Hispanic"),
    ("African American", "African American"),
    ("Other", "Other"),
]

CANCER_CHOICES = [
    ("Breast", "Breast"),
    ("Colon", "Colon"),
    ("Lung", "Lung"),
    ("Prostate", "Prostate"),
    ("Leukemia", "Leukemia"),
    ("Skin", "Skin"),
]

STAGE_CHOICES = [
    ("Stage I", "Stage I"),
    ("Stage II", "Stage II"),
    ("Stage III", "Stage III"),
    ("Stage IV", "Stage IV"),
]

SMOKING_CHOICES = [
    ("Never", "Never"),
    ("Former", "Former"),
    ("Current", "Current"),
]

YES_NO = [
    ("Yes", "Yes"),
    ("No", "No"),
]

TREATMENT_CHOICES = [
    ("Chemotherapy", "Chemotherapy"),
    ("Radiation", "Radiation"),
    ("Surgery", "Surgery"),
    ("Combination Therapy", "Combination Therapy"),
]

RESPONSE_CHOICES = [
    ("Complete Remission", "Complete Remission"),
    ("Partial Remission", "Partial Remission"),
    ("No Response", "No Response"),
]

GENETIC_CHOICES = [
    ("BRCA1", "BRCA1"),
    ("KRAS", "KRAS"),
    ("EGFR", "EGFR"),
]

REGION_CHOICES = [
    ("North", "North"),
    ("South", "South"),
    ("East", "East"),
    ("West", "West"),
]


class PredictionForm(forms.Form):

    patient_name = forms.CharField(max_length=100)

    age = forms.IntegerField(min_value=1, max_value=120)

    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female")]
    )

    race_ethnicity = forms.ChoiceField(choices=RACE_CHOICES)

    bmi = forms.FloatField(min_value=10, max_value=60)

    smoking_status = forms.ChoiceField(choices=SMOKING_CHOICES)

    family_history = forms.ChoiceField(choices=YES_NO)

    cancer_type = forms.ChoiceField(choices=CANCER_CHOICES)

    stage = forms.ChoiceField(choices=STAGE_CHOICES)

    tumor_size = forms.FloatField(min_value=0)

    treatment_type = forms.ChoiceField(choices=TREATMENT_CHOICES)

    treatment_response = forms.ChoiceField(choices=RESPONSE_CHOICES)

    survival_months = forms.IntegerField(min_value=0, max_value=300)

    genetic_marker = forms.ChoiceField(choices=GENETIC_CHOICES)

    hospital_region = forms.ChoiceField(choices=REGION_CHOICES)