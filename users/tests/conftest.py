import pytest
from users.models import CustomUser, Profile
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'JOB_SEEKER',
        }
        data.update(kwargs)
        user = CustomUser.objects.create_user(**data)
        return user
    return create_user

@pytest.fixture
def user_with_profile(user_factory):
    user = user_factory()
    profile = user.profile
    return user, profile

@pytest.fixture
def user_with_resume(user_factory):
    user = user_factory()
    profile = user.profile
    profile.resume = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
    profile.save()
    return user
