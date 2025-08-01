from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['posted_by', 'posted_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.ReadOnlyField(source='applicant.username')

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'applied_at']
