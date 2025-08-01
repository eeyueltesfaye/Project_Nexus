from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileStatusView, ProfileUpdateView, ResumeDownloadView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/status/', ProfileStatusView.as_view(), name='profile-status'),
    path('profile/resume/', ResumeDownloadView.as_view(), name='resume-download'),
]
