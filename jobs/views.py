from rest_framework import generics
from .models import Job, JobApplication, SavedJob, JobCategory
from .serializers import JobSerializer, JobApplicationSerializer, SavedJobSerializer, JobCategorySerializer
from .permissions import IsAdmin, IsRecruiter, IsJobSeeker
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import JobPagination
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers

# Admin & Recruiter can create jobs
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsRecruiter]


# Anyone authenticated can view jobs
class JobListView(generics.ListAPIView):
    pagination_class = JobPagination
    queryset = Job.objects.all().order_by('-posted_at')  # recent jobs first
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'category', 'job_type']  # for dropdowns/facets
    search_fields = ['title', 'description','industry', 'company_name'] #for full-text search
    ordering_fields = ['-posted_at', 'title']

    def get_queryset(self):
        return Job.objects.select_related('category', 'posted_by').all().order_by('-posted_at')

# Job Seekers can apply for jobs
class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobSeeker]

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        if JobApplication.objects.filter(job=job, applicant=self.request.user).exists():
            raise serializers.ValidationError("You have already applied to this job.")
        serializer.save(applicant=self.request.user)


class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        # Restrict to jobs created by the current recruiter
        return Job.objects.filter(posted_by=self.request.user)

class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin | IsRecruiter]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class JobApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

class JobApplicationDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)


class SavedJobListView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)

class SavedJobCreateView(generics.CreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def perform_create(self, serializer):
        job = serializer.validated_data.get('job')
        user = self.request.user

        # Prevent duplicate saves
        if SavedJob.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError("You have already saved this job.")

        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response({'detail': str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SavedJobDeleteView(generics.DestroyAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_object(self):
        job_id = self.kwargs.get('pk')
        saved_job = get_object_or_404(SavedJob, user=self.request.user, pk=job_id)
        return saved_job

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail': 'Saved job deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({'detail': 'Failed to delete saved job.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)


class RecruiterApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsRecruiter]

    def get_queryset(self):
            user = self.request.user
            if user.role == 'ADMIN':  # assuming is_staff means admin
                return JobApplication.objects.all()  # Admin sees all applications
            return JobApplication.objects.filter(job__posted_by=user)  # Recruiter sees only their own


# Admins can create categories
class JobCategoryCreateView(generics.CreateAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

# Anyone can list categories
class JobCategoryListView(generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated]

# Admins can update categories
class JobCategoryUpdateView(generics.UpdateAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

# Admins can delete categories
class JobCategoryDeleteView(generics.DestroyAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]