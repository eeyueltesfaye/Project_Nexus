from rest_framework import serializers
from .models import Job, JobApplication, SavedJob, JobCategory

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

class SavedJobSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'job_title', 'saved_at']


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name']
