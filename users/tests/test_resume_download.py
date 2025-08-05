import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_resume_download(user_with_resume):
    user = user_with_resume
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get('/api/users/profile/resume/')
    assert response.status_code == 200
    assert response.get('Content-Disposition', '').startswith('attachment;')
