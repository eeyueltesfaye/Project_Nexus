import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser

@pytest.mark.django_db
def test_user_login(user_factory):  # Assuming you have a user factory
    user = user_factory(email='user@example.com', password='testpass123')
    client = APIClient()
    payload = {"email": "user@example.com", "password": "testpass123"}

    response = client.post(reverse('login'), data=payload)
    assert response.status_code == 200
    assert 'token' in response.data
    assert 'redirect' in response.data
