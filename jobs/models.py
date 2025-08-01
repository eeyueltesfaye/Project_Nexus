from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
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
    category = models.CharField(max_length=100, db_index=True)
    company_name = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"
