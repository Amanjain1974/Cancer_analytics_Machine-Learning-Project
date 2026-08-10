from django import forms

YES_NO_CHOICES = [
    ("No", "No"),
    ("Yes", "Yes"),
]

GENDER_CHOICES = [
    ("Female", "Female"),
    ("Male", "Male"),
    ("Other", "Other"),
]

SMOKING_CHOICES = [
    ("Never", "Never Smoked"),
    ("Former", "Former Smoker"),
    ("Occasionally", "Occasional Smoker"),
    ("Daily", "Daily Smoker"),
]

SURVIVAL_SMOKING_CHOICES = [
    ("Never", "Never"),
    ("Former", "Former"),
    ("Current", "Current"),
]

ALCOHOL_CHOICES = [
    ("Never", "Never / Rarely"),
    ("Occasionally", "Occasionally (1-2 times/month)"),
    ("Weekly", "Weekly (1-3 drinks/week)"),
    ("Daily", "Daily (Heavy consumption)"),
]

EXERCISE_CHOICES = [
    ("Sedentary", "Sedentary (No regular exercise)"),
    ("1-2 times/week", "1-2 times per week"),
    ("3-4 times/week", "3-4 times per week"),
    ("Daily", "Daily vigorous exercise"),
]

LEVEL_CHOICES = [
    ("Low", "Low Level"),
    ("Moderate", "Moderate Level"),
    ("High", "High Level"),
]

DIET_LEVEL_CHOICES = [
    ("Low", "Low / Poor"),
    ("Moderate", "Moderate / Average"),
    ("High", "High / Optimal"),
]

FREQUENCY_CHOICES = [
    ("Rarely", "Rarely / Never"),
    ("Weekly", "Weekly"),
    ("Daily", "Daily"),
]

CANCER_FAMILY_CHOICES = [
    ("None", "None"),
    ("Breast", "Breast Cancer"),
    ("Colon", "Colon / Colorectal Cancer"),
    ("Lung", "Lung Cancer"),
    ("Prostate", "Prostate Cancer"),
    ("Skin", "Skin Cancer / Melanoma"),
    ("Other", "Other Cancer Type"),
]

CANCER_TYPE_CHOICES = [
    ("Breast", "Breast Cancer"),
    ("Colon", "Colon Cancer"),
    ("Lung", "Lung Cancer"),
    ("Prostate", "Prostate Cancer"),
    ("Leukemia", "Leukemia"),
    ("Skin", "Skin Cancer"),
    ("Other", "Other Cancer"),
]

STAGE_CHOICES = [
    ("Stage I", "Stage I (Early / Localized)"),
    ("Stage II", "Stage II (Localized / Regional Spread)"),
    ("Stage III", "Stage III (Advanced Regional)"),
    ("Stage IV", "Stage IV (Distant Metastatic)"),
]

TREATMENT_TYPE_CHOICES = [
    ("Surgery", "Surgical Resection"),
    ("Chemotherapy", "Chemotherapy Regimen"),
    ("Radiation Therapy", "Radiation Therapy"),
    ("Immunotherapy", "Immunotherapy"),
    ("Targeted Therapy", "Targeted Molecular Therapy"),
    ("Combination Therapy", "Combination Multi-Modality Therapy"),
]

TREATMENT_RESPONSE_CHOICES = [
    ("Excellent", "Excellent / Complete Remission"),
    ("Good", "Good / Significant Reduction"),
    ("Stable", "Stable Disease"),
    ("Partial Response", "Partial Response"),
    ("No Response", "No Response / Resistance"),
    ("Disease Progression", "Disease Progression"),
]

GENETIC_MARKER_CHOICES = [
    ("None", "None / Negative"),
    ("BRCA1", "BRCA1 Mutation"),
    ("BRCA2", "BRCA2 Mutation"),
    ("KRAS", "KRAS Mutation"),
    ("EGFR", "EGFR Mutation"),
    ("TP53", "TP53 Mutation"),
]

REGION_CHOICES = [
    ("North", "North Region Medical Center"),
    ("South", "South Region Medical Center"),
    ("East", "East Region Medical Center"),
    ("West", "West Region Medical Center"),
]


class PredictionForm(forms.Form):
    """
    Module 1: Early Cancer Risk Assessment Form (Pre-Diagnosis Evaluation).
    Collects 40+ epidemiological risk indicators across Personal Info, Lifestyle,
    Diet, Medical Conditions, Symptoms, and Environmental Exposures.
    """

    patient_name = forms.CharField(
        max_length=100,
        initial="Jane Doe",
        label="Patient Full Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g., Jane Doe", "class": "form-control"})
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        initial=40,
        label="Age (Years)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Gender",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    height_cm = forms.FloatField(
        min_value=50.0,
        max_value=250.0,
        initial=170.0,
        label="Height (cm)",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "id_height_cm"})
    )
    weight_kg = forms.FloatField(
        min_value=20.0,
        max_value=300.0,
        initial=70.0,
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "id_weight_kg"})
    )

    family_history = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label="Family History of Cancer",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    family_cancer_type = forms.ChoiceField(
        choices=CANCER_FAMILY_CHOICES,
        required=False,
        initial="None",
        label="Primary Cancer Type in Family",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    family_affected_count = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=0,
        label="Number of Affected Relatives",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    smoking_status = forms.ChoiceField(
        choices=SMOKING_CHOICES,
        label="Smoking Status",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    cigarettes_per_day = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=0,
        label="Cigarettes per Day",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    alcohol_intake = forms.ChoiceField(
        choices=ALCOHOL_CHOICES,
        label="Alcohol Consumption",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    tobacco_chewing = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label="Smokeless Tobacco",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    exercise_frequency = forms.ChoiceField(
        choices=EXERCISE_CHOICES,
        label="Exercise Frequency",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    daily_walking_mins = forms.IntegerField(
        min_value=0,
        max_value=300,
        initial=30,
        label="Daily Walking (Mins)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    sleep_hours = forms.IntegerField(
        min_value=1,
        max_value=16,
        initial=7,
        label="Sleep Hours / Night",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    stress_level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        label="Stress Level",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    water_intake_liters = forms.FloatField(
        min_value=0.5,
        max_value=10.0,
        initial=2.0,
        label="Water Intake (Liters/Day)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    vegetables_intake = forms.ChoiceField(choices=DIET_LEVEL_CHOICES, label="Vegetables Intake", widget=forms.Select(attrs={"class": "form-select"}))
    fruits_intake = forms.ChoiceField(choices=DIET_LEVEL_CHOICES, label="Fresh Fruits Intake", widget=forms.Select(attrs={"class": "form-select"}))
    fast_food_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label="Fast Food Frequency", widget=forms.Select(attrs={"class": "form-select"}))
    processed_meat = forms.ChoiceField(choices=YES_NO_CHOICES, label="Processed Meat", widget=forms.Select(attrs={"class": "form-select"}))
    red_meat = forms.ChoiceField(choices=FREQUENCY_CHOICES, label="Red Meat Frequency", widget=forms.Select(attrs={"class": "form-select"}))
    sugary_drinks = forms.ChoiceField(choices=FREQUENCY_CHOICES, label="Sugary Drinks Frequency", widget=forms.Select(attrs={"class": "form-select"}))
    junk_food_frequency = forms.ChoiceField(choices=DIET_LEVEL_CHOICES, label="Junk Food Overall", widget=forms.Select(attrs={"class": "form-select"}))

    diabetes = forms.ChoiceField(choices=YES_NO_CHOICES, label="Type-2 Diabetes", widget=forms.Select(attrs={"class": "form-select"}))
    hypertension = forms.ChoiceField(choices=YES_NO_CHOICES, label="Hypertension", widget=forms.Select(attrs={"class": "form-select"}))
    obesity = forms.ChoiceField(choices=YES_NO_CHOICES, label="Diagnosed Obesity", widget=forms.Select(attrs={"class": "form-select"}))
    chronic_inflammation = forms.ChoiceField(choices=YES_NO_CHOICES, label="Chronic Inflammation", widget=forms.Select(attrs={"class": "form-select"}))
    previous_tumors = forms.ChoiceField(choices=YES_NO_CHOICES, label="History of Benign Tumors", widget=forms.Select(attrs={"class": "form-select"}))
    genetic_disorders = forms.ChoiceField(choices=YES_NO_CHOICES, label="Genetic Disorders", widget=forms.Select(attrs={"class": "form-select"}))

    symptom_cough = forms.BooleanField(required=False, label="Persistent Cough")
    symptom_blood_stool = forms.BooleanField(required=False, label="Blood in Stool")
    symptom_blood_urine = forms.BooleanField(required=False, label="Blood in Urine")
    symptom_chest_pain = forms.BooleanField(required=False, label="Persistent Chest Pain")
    symptom_swallowing_difficulty = forms.BooleanField(required=False, label="Difficulty Swallowing")
    symptom_fatigue = forms.BooleanField(required=False, label="Severe Fatigue")
    symptom_weight_loss = forms.BooleanField(required=False, label="Sudden Weight Loss")
    symptom_fever = forms.BooleanField(required=False, label="Persistent Fever")
    symptom_night_sweats = forms.BooleanField(required=False, label="Night Sweats")
    symptom_skin_lesions = forms.BooleanField(required=False, label="New Skin Lesions")
    symptom_bleeding = forms.BooleanField(required=False, label="Unusual Bleeding")
    symptom_lump = forms.BooleanField(required=False, label="Lump or Body Thickening")
    symptom_chronic_pain = forms.BooleanField(required=False, label="Chronic Pain")
    symptom_infections = forms.BooleanField(required=False, label="Frequent Infections")

    air_pollution = forms.ChoiceField(choices=LEVEL_CHOICES, label="Air Pollution Exposure", widget=forms.Select(attrs={"class": "form-select"}))
    radiation_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Ionizing Radiation", widget=forms.Select(attrs={"class": "form-select"}))
    chemical_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Industrial Chemical Exposure", widget=forms.Select(attrs={"class": "form-select"}))
    asbestos_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Asbestos Exposure", widget=forms.Select(attrs={"class": "form-select"}))
    occupation_risk = forms.ChoiceField(choices=LEVEL_CHOICES, label="Hazardous Occupation Risk", widget=forms.Select(attrs={"class": "form-select"}))
    uv_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Excessive Sun / UV Exposure", widget=forms.Select(attrs={"class": "form-select"}))


class SurvivalPredictionForm(forms.Form):
    """
    Module 2: Cancer Survival Prediction Form (Post-Diagnosis Clinical Prognosis).
    Collects cancer-specific inputs for patients who ALREADY HAVE CANCER.
    """

    # Patient Demographic Profile
    patient_name = forms.CharField(
        max_length=100,
        initial="John Smith",
        label="Patient Full Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g., John Smith", "class": "form-control"})
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        initial=52,
        label="Age (Years)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Gender",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    height_cm = forms.FloatField(
        min_value=50.0,
        max_value=250.0,
        initial=175.0,
        label="Height (cm)",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "id_surv_height_cm"})
    )
    weight_kg = forms.FloatField(
        min_value=20.0,
        max_value=300.0,
        initial=75.0,
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "id_surv_weight_kg"})
    )
    smoking_status = forms.ChoiceField(
        choices=SURVIVAL_SMOKING_CHOICES,
        label="Smoking History",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    hospital_region = forms.ChoiceField(
        choices=REGION_CHOICES,
        label="Treating Hospital Region",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # Pre-existing Medical Conditions
    has_diabetes = forms.ChoiceField(choices=YES_NO_CHOICES, label="Type-2 Diabetes", widget=forms.Select(attrs={"class": "form-select"}))
    has_hypertension = forms.ChoiceField(choices=YES_NO_CHOICES, label="Hypertension", widget=forms.Select(attrs={"class": "form-select"}))
    has_heart_disease = forms.ChoiceField(choices=YES_NO_CHOICES, label="Heart Disease", widget=forms.Select(attrs={"class": "form-select"}))
    has_kidney_disease = forms.ChoiceField(choices=YES_NO_CHOICES, label="Kidney Disease", widget=forms.Select(attrs={"class": "form-select"}))

    # Cancer Diagnosis Parameters
    cancer_type = forms.ChoiceField(
        choices=CANCER_TYPE_CHOICES,
        label="Diagnosed Cancer Type",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    stage = forms.ChoiceField(
        choices=STAGE_CHOICES,
        label="Cancer Stage at Diagnosis",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    tumor_size_cm = forms.FloatField(
        min_value=0.1,
        max_value=30.0,
        initial=3.5,
        label="Tumor Size (cm)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    diagnosis_months = forms.IntegerField(
        min_value=0,
        max_value=240,
        initial=12,
        label="Time Since Initial Diagnosis (Months)",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    metastasis = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label="Distant Metastasis Detected?",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    lymph_nodes = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label="Lymph Node Involvement?",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    genetic_marker = forms.ChoiceField(
        choices=GENETIC_MARKER_CHOICES,
        label="Identified Genetic Biomarker",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # Treatment Parameters
    treatment_type = forms.ChoiceField(
        choices=TREATMENT_TYPE_CHOICES,
        label="Primary Treatment Type Received",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    treatment_response = forms.ChoiceField(
        choices=TREATMENT_RESPONSE_CHOICES,
        label="Clinical Response to Treatment",
        widget=forms.Select(attrs={"class": "form-select"})
    )


class RiskAssessmentForm(forms.Form):
    patient_name = forms.CharField(max_length=100, label="Full Name")
    age = forms.IntegerField(min_value=1, max_value=120, initial=35, label="Age")
    gender = forms.ChoiceField(choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")], label="Gender")
    height_cm = forms.FloatField(min_value=50, max_value=250, initial=170, label="Height (cm)")
    weight_kg = forms.FloatField(min_value=20, max_value=300, initial=70, label="Weight (kg)")

    smoking_status = forms.ChoiceField(choices=SMOKING_CHOICES, label="Smoking Status")
    alcohol_intake = forms.ChoiceField(choices=ALCOHOL_CHOICES, label="Alcohol Consumption")
    tobacco_use = forms.ChoiceField(choices=YES_NO_CHOICES, label="Smokeless Tobacco Use")
    physical_activity = forms.ChoiceField(choices=EXERCISE_CHOICES, label="Physical Activity Level")
    diet_quality = forms.ChoiceField(choices=DIET_LEVEL_CHOICES, label="Diet Quality")
    sleep_hours = forms.IntegerField(min_value=1, max_value=16, initial=7, label="Nightly Sleep (Hours)")
    stress_level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Perceived Stress Level")

    family_history = forms.ChoiceField(choices=YES_NO_CHOICES, label="Family History of Cancer")
    family_relative = forms.ChoiceField(choices=[("None", "None"), ("Parent", "Parent"), ("Sibling", "Sibling"), ("Child", "Child"), ("Extended", "Extended Relative")], required=False, initial="None", label="Affected Relative")
    family_cancer_type = forms.CharField(max_length=100, required=False, initial="None", label="Cancer Type")

    has_diabetes = forms.ChoiceField(choices=YES_NO_CHOICES, label="Type-2 Diabetes")
    has_hypertension = forms.ChoiceField(choices=YES_NO_CHOICES, label="Hypertension")
    is_obese = forms.ChoiceField(choices=YES_NO_CHOICES, label="Diagnosed Obesity")
    previous_radiation = forms.ChoiceField(choices=YES_NO_CHOICES, label="Prior Radiation Therapy")
    previous_benign_tumors = forms.ChoiceField(choices=YES_NO_CHOICES, label="History of Benign Tumors")

    pollution_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Air Pollution Exposure")
    chemical_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="Industrial Chemical Exposure")
    uv_exposure = forms.ChoiceField(choices=LEVEL_CHOICES, label="UV Radiation Exposure")
    occupation_risk = forms.ChoiceField(choices=LEVEL_CHOICES, label="Hazardous Occupation Risk")