import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    payload = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!"
    }

    response = client.post(reverse('register'), data=payload)
    assert response.status_code == 201
    assert CustomUser.objects.filter(email="test@example.com").exists()
