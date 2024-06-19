from django import forms
from django.template.defaulttags import now

from .models import Category
from django.utils import timezone



class AddTransactionForm(forms.Form):
    description = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
