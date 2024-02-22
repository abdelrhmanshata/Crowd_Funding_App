
from django.shortcuts import render, redirect

# Create your views here.
from admin_app.models import Category
from projects_app.models import Projects, Image
from django.db.models import Q


def home(request):
    cat_menu = Category.objects.all()
    last_5_projects = Projects.objects.order_by("-id")[:5]
    featured_projects = Projects.objects.filter(featured=True)[:6]

    allLast_5_Data = []
    for project in last_5_projects:
        images = Image.objects.filter(project=project)
        allLast_5_Data.append({"project": project, "images": images})

    Featured_All_Data = []
    for project in featured_projects:
        images = Image.objects.filter(project=project)
        Featured_All_Data.append({"project": project, "images": images})
        
    # projects = Projects.objects.all()
    
    context = {
        "cat_menu": cat_menu,
        "allLast_5_Data": allLast_5_Data,
        "Featured_All_Data": Featured_All_Data,
      
    }
    return render(request, "home/home.html", context)


def get_category_projects(request, category_id):
    projects = Projects.objects.filter(category=category_id).all()
    category = Category.objects.get(id=category_id)
    all_Projects_Data = []
    for project in projects:
        images = Image.objects.filter(project=project)
        all_Projects_Data.append({"project": project, "images": images})
    
    context = {
        "category": category,
        "all_Projects_Data": all_Projects_Data,
    }
    return render(request, "home/category.html", context)



