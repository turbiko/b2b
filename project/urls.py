from django.urls import path
from . import views

urlpatterns = [
	path('uploadprojectfiles/<str:pk>/', views.addPhoto, name='uploads'),
]

