from django import forms
from .models import *
from django.core.exceptions import ValidationError


# category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
