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


ALCOHOL_CHOICES = [
    ("None", "None / Rarely"),
    ("Moderate", "Moderate (1-2 drinks/week)"),
    ("Heavy", "Heavy (>= 3 drinks/week)"),
]

ACTIVITY_CHOICES = [
    ("Low", "Low / Sedentary"),
    ("Moderate", "Moderate (150 mins/week)"),
    ("High", "High / Vigorous"),
]

DIET_CHOICES = [
    ("Poor", "Poor / Processed Foods Focus"),
    ("Average", "Average / Balanced"),
    ("Good", "Good / High Fiber & Veggies"),
    ("Excellent", "Excellent / Whole Food Plant Focus"),
]

STRESS_CHOICES = [
    ("Low", "Low"),
    ("Moderate", "Moderate"),
    ("High", "High Chronic Stress"),
]

RELATIVE_CHOICES = [
    ("None", "None"),
    ("Parent", "Parent (Mother/Father)"),
    ("Sibling", "Sibling (Brother/Sister)"),
    ("Child", "Child"),
    ("Extended", "Extended Relative (Aunt/Uncle/Grandparent)"),
]

EXPOSURE_CHOICES = [
    ("Low", "Low Exposure"),
    ("Moderate", "Moderate Exposure"),
    ("High", "High Exposure"),
]


class RiskAssessmentForm(forms.Form):
    # Personal Metrics
    patient_name = forms.CharField(max_length=100, label="Full Name")
    age = forms.IntegerField(min_value=1, max_value=120, initial=35, label="Age")
    gender = forms.ChoiceField(
        choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")],
        label="Gender"
    )
    height_cm = forms.FloatField(min_value=50, max_value=250, initial=170, label="Height (cm)")
    weight_kg = forms.FloatField(min_value=20, max_value=300, initial=70, label="Weight (kg)")

    # Lifestyle Factors
    smoking_status = forms.ChoiceField(choices=SMOKING_CHOICES, label="Smoking Status")
    alcohol_intake = forms.ChoiceField(choices=ALCOHOL_CHOICES, label="Alcohol Consumption")
    tobacco_use = forms.ChoiceField(choices=YES_NO, label="Smokeless Tobacco Use")
    physical_activity = forms.ChoiceField(choices=ACTIVITY_CHOICES, label="Physical Activity Level")
    diet_quality = forms.ChoiceField(choices=DIET_CHOICES, label="Diet Quality")
    sleep_hours = forms.IntegerField(min_value=1, max_value=16, initial=7, label="Nightly Sleep (Hours)")
    stress_level = forms.ChoiceField(choices=STRESS_CHOICES, label="Perceived Stress Level")

    # Family History
    family_history = forms.ChoiceField(choices=YES_NO, label="Family History of Cancer")
    family_relative = forms.ChoiceField(choices=RELATIVE_CHOICES, required=False, initial="None", label="Affected Relative")
    family_cancer_type = forms.CharField(max_length=100, required=False, initial="None", label="Cancer Type (Optional)")

    # Medical History
    has_diabetes = forms.ChoiceField(choices=YES_NO, label="Type-2 Diabetes")
    has_hypertension = forms.ChoiceField(choices=YES_NO, label="Hypertension (High BP)")
    is_obese = forms.ChoiceField(choices=YES_NO, label="Diagnosed Obesity")
    previous_radiation = forms.ChoiceField(choices=YES_NO, label="Prior Radiation Therapy")
    previous_benign_tumors = forms.ChoiceField(choices=YES_NO, label="History of Benign Tumors/Polyps")

    # Environmental & Occupational
    pollution_exposure = forms.ChoiceField(choices=EXPOSURE_CHOICES, label="Air Pollution Exposure")
    chemical_exposure = forms.ChoiceField(choices=EXPOSURE_CHOICES, label="Industrial Chemical Exposure")
    uv_exposure = forms.ChoiceField(choices=EXPOSURE_CHOICES, label="Sun / UV Radiation Exposure")
    occupation_risk = forms.ChoiceField(choices=EXPOSURE_CHOICES, label="Hazardous Occupation Risk")