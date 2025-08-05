import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser

@pytest.mark.django_db
def test_logout(user_factory):
    user = user_factory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.force_authenticate(user=user)
    
    response = client.post('/api/users/logout/', {"refresh": str(refresh)})
    assert response.status_code == 205
