import pytest
from users.models import CustomUser
from jobs.models import Job, JobCategory
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return CustomUser.objects.create_user(email='admin@example.com', password='admin123', role='admin', is_staff=True, is_superuser=True)

@pytest.fixture
def recruiter_user(db):
    return CustomUser.objects.create_user(email='recruiter@example.com', password='recruiter123', role='recruiter')

@pytest.fixture
def job_seeker_user(db):
    return CustomUser.objects.create_user(email='seeker@example.com', password='seek123', role='job_seeker')

@pytest.fixture
def auth_client(api_client, recruiter_user):
    api_client.force_authenticate(user=recruiter_user)
    return api_client

@pytest.fixture
def job_category():
    return JobCategory.objects.create(name="Engineering")

@pytest.fixture
def job(recruiter_user, job_category):
    return Job.objects.create(
        title="Backend Developer",
        description="Django experience required",
        location="Remote",
        job_type="Full-time",
        posted_by=recruiter_user,
        category=job_category
    )
