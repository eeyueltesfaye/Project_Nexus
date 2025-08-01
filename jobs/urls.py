# jobs/urls.py

from django.urls import path
from .views import (
    JobCreateView, JobListView, JobApplicationCreateView,
    JobUpdateView, JobDeleteView,
    JobApplicationUpdateView, JobApplicationDeleteView,
)

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/apply/', JobApplicationCreateView.as_view(), name='job-apply'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('applications/<int:pk>/update/', JobApplicationUpdateView.as_view(), name='application-update'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='application-delete'),
]
