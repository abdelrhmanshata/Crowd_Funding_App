from django.urls import path

# from home_app import views
from . import views


urlpatterns = [
    path("addProject/", views.addProject, name="addProject"),
    path("showProjects/", views.showProjects, name="showAllProjects"),
    path("projectDetails/<int:id>/", views.projectDetails, name="projectDetails"),
    path("projectDelete/<int:id>/", views.deleteProject, name="deleteProject"),
    path("reportComments/<int:idComment>/", views.reportComments, name="reportComments"),
    path("reportProject/<int:idProject>/", views.reportProject, name="reportProject"),
     path("projectFeatured/<int:id>/", views.projectFeatured, name="projectFeatured"),
    
]

