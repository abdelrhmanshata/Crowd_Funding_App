from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, "Add Category Successfully.")
        return redirect("category")
    else:
        form = CategoryForm()
        context = {"form": form, "categories": Category.getAllCategory()}
        return render(request, "admin_app/showCategory.html", context)


@login_required
def updateCategory(request, categoryID):
    category = Category.getCategory(categoryID)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, "Update Category Successfully.")
        return redirect("category")
    else:
        form = CategoryForm(instance=category)
        context = {"form": form, "categories": Category.getAllCategory()}
        return render(request, "admin_app/showCategory.html", context)


@login_required
def deleteCategory(request, categoryID):
    if request.method == "GET":
        Category.deleteCategory(categoryID)
        messages.success(request, "Delete Category Successfully.")
        return redirect("category")
