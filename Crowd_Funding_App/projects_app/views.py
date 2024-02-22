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
    photos = Image.objects.filter(project=project)
    tags = Tag.objects.filter(project=project)
    context = {
        "project": project,
        
        "photos": photos,
        "tags": tags,
        
    }
    return render(request, "projects_app/detail.html", context)
