from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('candidates/', views.candidate_profile, name='candidate_profile'),
]
