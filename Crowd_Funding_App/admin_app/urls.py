from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("category/", views.category, name="category"),
    path("update-category/<int:categoryID>", views.updateCategory, name="updateCategory"),
    path("delete-category/<int:categoryID>", views.deleteCategory, name="deleteCategory"),
  
  
]
