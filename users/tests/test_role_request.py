
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser, RoleRequest
import json

@pytest.mark.django_db
class TestRoleRequestView:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def job_seeker(self):
        return CustomUser.objects.create_user(email='jobseeker@example.com', password='pass1234', role='JOB_SEEKER')

    @pytest.fixture
    def recruiter(self):
        return CustomUser.objects.create_user(email='recruiter@example.com', password='pass1234', role='RECRUITER')

    def test_job_seeker_can_request_role(self, client, job_seeker):
        client.force_authenticate(user=job_seeker)
        url = reverse('request-role')  # replace with your actual path name if different
        data = {'requested_role': 'RECRUITER', 'reason': 'I want to post jobs'}
        response = client.post(url, data, format='json')
        assert response.status_code == 201
        assert RoleRequest.objects.filter(user=job_seeker, requested_role='RECRUITER').exists()

    def test_non_job_seeker_cannot_request_role(self, client, recruiter):
        client.force_authenticate(user=recruiter)
        url = reverse('request-role')
        data = {'requested_role': 'ADMIN', 'reason': 'Because I am cool'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    def test_cannot_request_duplicate_role(self, client, job_seeker):
        RoleRequest.objects.create(user=job_seeker, requested_role='RECRUITER', approved=False)
        client.force_authenticate(user=job_seeker)
        url = reverse('request-role')
        data = {'requested_role': 'RECRUITER', 'reason': 'Trying again'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert RoleRequest.objects.filter(user=job_seeker, requested_role='RECRUITER').count() == 1

    def test_invalid_role_value(self, client, job_seeker):
        client.force_authenticate(user=job_seeker)
        url = reverse('request-role')
        data = {'requested_role': 'INVALID_ROLE', 'reason': 'Testing invalid role'}
        response = client.post(url, data, format='json')
        assert response.status_code == 400
