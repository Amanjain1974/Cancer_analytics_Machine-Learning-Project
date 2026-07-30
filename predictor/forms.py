from django import forms


class PredictionForm(forms.Form):
    patient_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Patient Name"
        })
    )

    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )

    gender = forms.ChoiceField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female")
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    race_ethnicity = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    bmi = forms.FloatField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01"
        })
    )

    smoking_status = forms.ChoiceField(
        choices=[
            ("Never", "Never"),
            ("Former", "Former"),
            ("Current", "Current")
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    family_history = forms.ChoiceField(
        choices=[
            ("Yes", "Yes"),
            ("No", "No")
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    cancer_type = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    stage = forms.ChoiceField(
        choices=[
            ("I", "Stage I"),
            ("II", "Stage II"),
            ("III", "Stage III"),
            ("IV", "Stage IV")
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    tumor_size = forms.FloatField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01"
        })
    )

    treatment_type = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    treatment_response = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    survival_months = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    genetic_marker = forms.CharField(
        required=False,
        initial="Unknown",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    hospital_region = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
