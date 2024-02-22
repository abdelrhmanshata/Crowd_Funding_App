from django.db import models
from django.contrib.auth.models import User
from admin_app.models import *
from django.utils import timezone



class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    details = models.TextField(default="")
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    currentFunds = models.FloatField(default=0)
    tags = models.CharField(blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)
    avgRating = models.FloatField(default=0)
    

    def __str__(self):
        return self.title

class Image(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project_images/")

    def getImageUrl(self):
        return f"/media/{self.image}"

class Comment(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    commentContent = models.CharField(default="")
    commentDate = models.DateField(default=timezone.now)
    numCommentReport = models.IntegerField(default=0)

class ProjectReport(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    reportContent = models.CharField(default="")

class Donation(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    donationAmount = models.FloatField(default=0.0)

class Rating(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    ratingValue = models.IntegerField(default=0)

class Tag(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    tagContent = models.CharField(default="")