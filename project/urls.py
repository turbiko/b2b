from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
	path('uploadprojectfiles/<str:pk>/', views.addPhoto, name='uploads'),
=======
	path('uploadprojectfiles/<str:pk>/', views.add_photo, name='uploads'),
	path('planned/', views.projects_planned, name='projects_planned'),
>>>>>>> Stashed changes
]

