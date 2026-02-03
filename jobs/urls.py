from django.urls import path, include

from applications.views import job_applications
from .views import *
urlpatterns = [
    path('jobseeker/', jobseeker_dashboard, name="jobseeker_dashboard"),
    path('recruiter/', recruiter_dashboard, name="recruiter_dashboard"),
    path('post-job/', post_job, name="post_job"),
    path('recruiter-job-list/', recruiter_job_list, name="recruiter_job_list"),
    path('jobseeker-job-list/', jobseeker_job_list, name="jobseeker_job_list"),
    path('job/<int:job_id>/', job_detail_page, name="job_detail"),
    path('job/<int:job_id>/apply/', apply_job, name="apply_job"),
    path('job/<int:job_id>/applications/', job_applications, name='job_applications'),
]