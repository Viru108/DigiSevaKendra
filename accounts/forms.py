from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from departments.models import City, Department


class CitizenRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Phone Number'}))
    city = forms.ModelChoiceField(queryset=City.objects.filter(is_active=True), widget=forms.Select(attrs={'class': 'form-select glass-input'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('full_name', 'email', 'phone', 'city', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CITIZEN'
        if commit:
            user.save()
        return user


class AddOfficerForm(forms.Form):
    """Used by Municipal Head to add an Officer to a department."""
    full_name  = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Full Name'}))
    email      = forms.EmailField(                 widget=forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Email'}))
    phone      = forms.CharField(max_length=15,    widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Phone Number'}))
    password   = forms.CharField(                  widget=forms.PasswordInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Temporary Password'}))
    department = forms.ModelChoiceField(queryset=Department.objects.none(),
                                        widget=forms.Select(attrs={'class': 'form-select glass-input'}))

    def __init__(self, city=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if city:
            self.fields['department'].queryset = Department.objects.filter(city=city, is_active=True)


class AddTechnicianForm(forms.Form):
    """Used by Department Officer to add a Technician."""
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Full Name'}))
    email     = forms.EmailField(               widget=forms.EmailInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Email'}))
    phone     = forms.CharField(max_length=15,  widget=forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Phone Number'}))
    password  = forms.CharField(               widget=forms.PasswordInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Temporary Password'}))

