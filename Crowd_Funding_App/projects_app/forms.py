from django import forms
from .models import *
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
            "title",
            "details",
            "category",
            "total_target",
            "tags",
            "start_time",
            "end_time",
        ]
        # fields = "__all__"

class TagForm(forms.Form):
    tagContent = forms.CharField(label="Would you like to add a tag?")
