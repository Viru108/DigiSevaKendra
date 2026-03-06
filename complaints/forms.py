from django import forms
from .models import Complaint
from departments.models import Department, Category

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'department', 'category', 'description', 
            'formatted_address', 'landmark', 'pincode',
            'latitude', 'longitude', 'before_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3}),
            'formatted_address': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Auto-filled from search or type manually'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'before_image': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'department': forms.Select(attrs={'class': 'form-select glass-input', 'onchange': 'updateCategories()'}),
            'category': forms.Select(attrs={'class': 'form-select glass-input'}),
        }

class ComplaintResolveForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['after_image']
        widgets = {
            'after_image': forms.FileInput(attrs={'class': 'form-control glass-input', 'required': True}),
        }
        labels = {
            'after_image': 'Upload Completion Photo (Mandatory)'
        }
