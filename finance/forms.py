from django import forms

from .models import Category, Profile, Tag


class AddTransactionForm(forms.Form):
    description = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
