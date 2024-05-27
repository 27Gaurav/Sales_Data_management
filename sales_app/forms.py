from django import forms
from .models import SalesRecord

class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = ['date', 'product', 'sales_amount', 'region', 'receipt_photo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Make it a date picker
        }