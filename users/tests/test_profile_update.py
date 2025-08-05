import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_profile_update(user_with_profile):
    user, profile = user_with_profile
    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "phone_number": "1234567890",
        "gender": "M",
        "country": "US"
    }
    response = client.put('/api/users/profile/update/', data)
    assert response.status_code == 200
    assert response.data['profile_completed'] is True
