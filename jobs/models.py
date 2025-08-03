from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Job(models.Model):
    STATUS_CHOICES = [
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed'),
    ]
    JOB_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
        ('FR', 'Freelance'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100, db_index=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES,db_index=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    company_name = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    posted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    expires_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('REVIEWED', 'Reviewed'),
    ('INTERVIEW', 'Interview'),
    ('REJECTED', 'Rejected'),
    ('HIRED', 'Hired'),
]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE,
    related_name='applications'
)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"
    
