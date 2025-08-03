# jobs/urls.py

from django.urls import path
from .views import (
    JobCreateView, JobListView, JobApplicationCreateView,
    JobUpdateView, JobDeleteView,
    JobApplicationUpdateView, JobApplicationDeleteView,
    JobDetailView,
    RecruiterApplicationListView,
    SavedJobListView, SavedJobCreateView, SavedJobDeleteView,
    JobCategoryCreateView,
    JobCategoryListView,
    JobCategoryUpdateView,
    JobCategoryDeleteView,
)

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/apply/', JobApplicationCreateView.as_view(), name='job-apply'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('applications/<int:pk>/update/', JobApplicationUpdateView.as_view(), name='application-update'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='application-delete'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('applications/recruiter/', RecruiterApplicationListView.as_view(), name='recruiter-applications'),
    path('saved-jobs/', SavedJobListView.as_view(), name='saved-job-list'),
    path('saved-jobs/create/', SavedJobCreateView.as_view(), name='saved-job-create'),
    path('saved-jobs/<int:pk>/delete/', SavedJobDeleteView.as_view(), name='saved-job-delete'),
    path('categories/', JobCategoryListView.as_view(), name='category-list'),
    path('categories/create/', JobCategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', JobCategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', JobCategoryDeleteView.as_view(), name='category-delete'),


]
