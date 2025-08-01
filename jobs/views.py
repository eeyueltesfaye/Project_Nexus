from rest_framework import generics
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from .permissions import IsAdmin, IsRecruiter, IsJobSeeker
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Admin & Recruiter can create jobs
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin | IsRecruiter]


# Anyone authenticated can view jobs
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')  # recent jobs first
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'category', 'job_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


# Job Seekers can apply for jobs
class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobSeeker]

    def perform_create(self, serializer):
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

