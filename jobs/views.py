from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import User
from applications.models import Application
from .models import Job
# Create your views here.
@login_required(login_url='login')
def jobseeker_dashboard(request):
    if request.user.roles != "jobseeker":
        return redirect('login')
    return render(request, "jobs/jobseeker_dashboard.html")

@login_required(login_url='login')
def recruiter_dashboard(request):
    if request.user.roles != "recruiter":
        return redirect('login')
    return render(request, "jobs/recruiter_dashboard.html")


@login_required(login_url='login')
def post_job(request):
    if request.user.roles != "recruiter":
        return redirect('login')

    if request.method == "POST":
        data = request.POST
        job_title = data.get("job_title")
        company_name = data.get("company_name")
        location = data.get("location")

        Job.objects.create(job_title=job_title, company_name=company_name,location=location,posted_by=request.user)
        messages.success(request, 'Job created and submitted successfully!')
        return redirect('recruiter_job_list')

    return render(request, 'jobs/post_job.html')

@login_required(login_url='login')
def recruiter_job_list(request):
    if request.user.roles != "recruiter":
        return redirect('jobseeker_dashboard')

    queryset = Job.objects.filter(posted_by=request.user)

    return render(request, "jobs/recruiter_job_list.html", context={'recruiter_job_list':queryset})

@login_required(login_url='login')
def jobseeker_job_list(request):
    if request.user.roles != "jobseeker":
        return redirect('recruiter_dashboard')

    job_id = Job.objects.all()

    return render(request, "jobs/jobseeker_job_list.html", context={'jobseeker_job_list':job_id})


@login_required(login_url='login')
def apply_job(request, job_id):
    if request.user.roles != "jobseeker":
        return redirect('recruiter_dashboard')

    job = Job.objects.get(id=job_id)

    # Prevent duplicate application
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, "You already applied for this job")
        return redirect('job_detail', job_id=job_id)

    if request.method == "POST":
        resume = request.FILES.get("resume")

        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume
        )

        messages.success(request, "Job applied successfully!")
        return redirect('jobseeker_dashboard')

@login_required(login_url='login')
def job_detail_page(request, job_id):
    if request.user.roles != "jobseeker":
        return redirect('recruiter_dashboard')
    job = Job.objects.get(id=job_id)
    return render(request, "jobs/job.html", context={'job':job})

