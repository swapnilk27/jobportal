from django.db import models

from jobs.models import Job
from accounts.models import User


# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ("withdrawn", "Withdrawn"),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/')
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10)
    applied_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     # verbose_name = "Job Application"
    #     verbose_name_plural = "Job Application"

    def __str__(self):
        return self.job.job_title
