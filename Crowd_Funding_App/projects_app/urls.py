from django.urls import path

# from home_app import views
from . import views


urlpatterns = [
    path("addProject/", views.addProject, name="addProject"),
    path("showProjects/", views.showProjects, name="showAllProjects"),
    path("projectDetails/<int:id>/", views.projectDetails, name="projectDetails"),
    path("projectDelete/<int:id>/", views.deleteProject, name="deleteProject"),
    
]
