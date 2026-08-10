from django import forms
from .models import Class, Subject, AttendanceSession


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'department', 'year', 'section', 'subject', 'students']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS301-A'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A/B/C'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = __import__('accounts.models', fromlist=['CustomUser']).CustomUser.objects.filter(role='student')


class AttendanceSessionForm(forms.ModelForm):
    duration = forms.IntegerField(
        min_value=5, max_value=120, initial=15,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'})
    )

    class Meta:
        model = AttendanceSession
        fields = ['location']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room/Location (optional)'}),
        }
