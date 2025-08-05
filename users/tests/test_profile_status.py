import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_profile_status(user_with_profile):
    user, _ = user_with_profile
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get('/api/users/profile/status/')
    assert response.status_code == 200
    assert 'profile_completed' in response.data
