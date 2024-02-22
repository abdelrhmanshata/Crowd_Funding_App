from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


def showProjects(request):
    projects = Projects.objects.all()
    allData = []
    for project in projects:
        images = Image.objects.filter(project=project)
        allData.append({"project": project, "images": images})

    context = {"allData": allData}
    return render(request, "projects_app/project.html", context)


# Create your views here.
@login_required
def addProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            images = request.FILES.getlist("images")
            for image in images:
                Image.objects.create(project=project, image=image)

            tags = request.POST.get("tags")
            for tag in tags.split("#"):
                if len(tag) != 0:
                    Tag.objects.create(project=project, tagContent=tag)

        return redirect("home")
    else:
        form = ProjectForm()
        return render(request, "projects_app/addproject.html", {"form": form})


def deleteProject(request, id):
    project = Projects.objects.get(user=request.user, id=id)
    checkTarget = int(project.total_target) * 0.25
    if project.currentFunds > checkTarget:
        messages.info(
            request,
            "This project has funds more than 25% of the total target, you can not delete it! ",
        )
    else:
        project.delete()

    projects = Projects.objects.filter(user=request.user)
    allData = []
    for project in projects:
        images = Image.objects.filter(project=project)
        allData.append({"project": project, "images": images})

    context = {"allData": allData}
    return render(request, "registration/projectProfile.html", context)



def projectDetails(request, id):
    project = Projects.objects.get(id=id)
    basedProjects = getBasedProject(project)
    photos = Image.objects.filter(project=project)
    tags = Tag.objects.filter(project=project)
    comments = Comment.objects.filter(project=project)
        
    donationForm = DonationForm()
    ratingForm = RatingForm()
    commentForm = CommentForm()

    if request.method == "POST":
        donationForm = DonationForm(request.POST)
        ratingForm = RatingForm(request.POST)
        commentForm = CommentForm(request.POST)

        if donationForm.is_valid():
            donation = donationForm.save(commit=False)
            if donation.donationAmount != None and donation.donationAmount != 0:
                addDonation(donation, request.user, project)

        if ratingForm.is_valid():
            rating = ratingForm.save(commit=False)
            if rating.ratingValue != None:
                addRating(rating, request.user, project)
                project.avgRating = calculateRatings(project)
                project.save()

        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            if comment.commentContent != "":
                addComment(comment, request.user, project)
                comments = Comment.objects.filter(project=project)
    
    
    allComments = []
    for comment in comments:
        commentReportsNum = CommentReport.objects.filter(comment=comment).count()
        allComments.append({"comment": comment, "commentReportsNum": commentReportsNum})
    
    isProjectActive = timezone.now() <= project.end_time
        
    context = {
        "project": project,
        "basedProjects": basedProjects,
        "photos": photos,
        "tags": tags,
        "allComments": allComments,
        "rating": calculateRatings(project),
        "donationForm": donationForm,
        "ratingForm": ratingForm,
        "commentForm": commentForm,
        "isProjectActive":isProjectActive
    }
    return render(request, "projects_app/detail.html", context)



def reportComments(request, idComment):
    if Comment.objects.filter(id=idComment).exists():
        comment = Comment.objects.get(id=idComment)
        if request.method == "POST":
            if not CommentReport.objects.filter(
                user=request.user, comment=comment
            ).exists():
                CommentReport.objects.create(
                    comment=comment,
                    user=request.user,
                    reportContent=request.POST["userComment"],
                )
            return redirect("home")
        context = {"comment": comment}
        return render(request, "projects_app/reportComment.html", context)
    return redirect("showAllProjects")

def reportProject(request, idProject):
    project = Projects.objects.get(id=idProject)
    ProjectReport.objects.create(project=project, user=request.user)
    return redirect("home")

def addDonation(donation, user, project):
    if Donation.objects.filter(project=project, user=user).exists():
        donationObj = Donation.objects.get(project=project, user=user)
        donationObj.donationAmount += donation.donationAmount
        donationObj.save()
    else:
        donation.project = project
        donation.user = user
        donation.save()
    project.currentFunds += donation.donationAmount
    project.save()

def addRating(rating, user, project):
    if Rating.objects.filter(project=project, user=user).exists():
        Rating.objects.filter(project=project, user=user).delete()
    rating.project = project
    rating.user = user
    rating.save()



def addComment(comment, user, project):
    if Comment.objects.filter(project=project, user=user).exists():
        commentObj = Comment.objects.get(project=project, user=user)
        commentObj.commentContent = comment.commentContent
        commentObj.save()
    else:
        comment.project = project
        comment.user = user
        comment.save()

# get 4 BaseProject
def getBasedProject(project):
    tags = Tag.objects.filter(project=project)
    basedProjects = []
    for tag in tags:
        projectTags = Tag.objects.filter(tagContent=tag.tagContent)
        for projectTag in projectTags:
            if projectTag.project != project:
                try:
                    basedProjects.index(projectTag.project)
                except:
                    basedProjects.append(projectTag.project)        
    return basedProjects[:4]



# Start Ratings Block
def calculateRatings(project):
    ratings = Rating.objects.all().filter(project=project)
    if ratings:
        totalRating = 0
        for rating in ratings:
            totalRating += rating.ratingValue
        return totalRating / len(ratings)
    return 0

def projectFeatured(request, id):
    project = Projects.objects.get(id=id)
    project.featured = not project.featured
    project.save()
    return redirect("showAllProjects")
