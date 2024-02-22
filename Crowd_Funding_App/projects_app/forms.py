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

class RatingForm(forms.ModelForm):
    ratingValue = forms.IntegerField(
        required=False,
        label="Enter an integer between 0 and 10",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    class Meta:
        model = Rating
        fields = ["ratingValue"]

class CommentForm(forms.ModelForm):
    commentContent = forms.CharField(
        required=False,label="Enter Your Comment",widget=forms.Textarea(attrs={"rows": 4})
    )

    class Meta:
        model = Comment
        fields = ["commentContent"]

class DonationForm(forms.ModelForm):
    donationAmount = forms.FloatField(label="Enter Donation", required=False)

    class Meta:
        model = Donation
        fields = ["donationAmount"]

