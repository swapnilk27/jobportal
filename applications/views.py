from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from jobs.models import Job
from .models import Application

@login_required(login_url='login')
def my_applications(request):
    if request.user.roles != "jobseeker":
        return redirect('recruiter_dashboard')

    applications = Application.objects.filter(applicant=request.user)

    return render(
        request,
        "applications/my_applications.html",
        {"applications": applications}
    )

@login_required(login_url='login')
def job_applications(request, job_id):
    if request.user.roles != "recruiter":
        return redirect('jobseeker_dashboard')
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)
    # messages.success()
    return render(
        request,
        "applications/job_applications.html",
        {
            "job": job,
            "applications": applications
        }
    )


@login_required(login_url='login')
def update_application_status(request, app_id, status):
    if request.user.roles != "recruiter":
        return redirect('jobseeker_dashboard')

    application = get_object_or_404(Application, id=app_id, job__posted_by=request.user)

    if status not in ["accepted", "rejected"]:
        messages.error(request, "Invalid Option")
        return redirect('job_applications',job_id=application.job.id)

    application.status = status
    application.save()

    messages.success(request, f"Application {status.capitalize()}!")
    return redirect('job_applications',job_id=application.job.id)