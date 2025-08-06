from rest_framework import serializers
from .models import Job, JobApplication, SavedJob, JobCategory
import re

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.ReadOnlyField(source='posted_by.username')
    category_name = serializers.CharField(write_only=True, required=True)
    category = serializers.SerializerMethodField(read_only=True)
    salary = serializers.CharField(required=True, allow_blank=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    industry = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    job_type = serializers.ChoiceField(choices=Job.JOB_TYPE_CHOICES, required=True)
    company_name = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=Job.STATUS_CHOICES, required=False)
    

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['posted_by', 'posted_at', 'view_count']

    def get_category(self, obj):
        return obj.category.category_name if obj.category else None

    def validate_category_name(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        try:
            return JobCategory.objects.get(category_name__iexact=value)
        except JobCategory.DoesNotExist:
            raise serializers.ValidationError("Category not found.")
        
    def validate_salary(self, value):
        if not re.match(r'^[\w\s\-\.,]+$', value):
            raise serializers.ValidationError("Salary must contain only letters, numbers, spaces, or basic punctuation.")
        return value

    def create(self, validated_data):
        category = validated_data.pop('category_name')
        validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'category_name' in validated_data:
            category = validated_data.pop('category_name')
            validated_data['category'] = category
        return super().update(instance, validated_data)


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
        fields = ['id', 'category_name']
