from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator


from accounts.models import User
from applications.models import Application
from .models import Job
# Create your views here.
@login_required(login_url='login')
def jobseeker_dashboard(request):
    if request.user.roles != "jobseeker":
        return redirect('login')

    applications = Application.objects.filter(applicant=request.user)

    total_applications = applications.count()
    pending_applications = applications.filter(status="pending").count()
    accepted_applications = applications.filter(status="accepted").count()
    rejected_applications = applications.filter(status="rejected").count()

    recent_applications = applications.order_by("-applied_date")[:5]

    last_application = applications.order_by("-applied_date").first()

    context = {
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "accepted_applications": accepted_applications,
        "rejected_applications": rejected_applications,
        "recent_applications": recent_applications,
        "last_application": last_application,
    }

    return render(request, "jobs/jobseeker_dashboard.html", context)


@login_required(login_url='login')
def recruiter_dashboard(request):
    if request.user.roles != "recruiter":
        return redirect('login')

    jobs = Job.objects.filter(posted_by=request.user)

    total_job_posted = jobs.count()
    total_applications_received = Application.objects.filter(
        job__posted_by=request.user
    ).exclude(status="withdrawn").count()

    pending_applications = Application.objects.filter(
        status="pending", job__posted_by=request.user
    ).count()
    accepted_applications = Application.objects.filter(
        status="accepted", job__posted_by=request.user
    ).count()

    # Jobs with no applicants
    jobs_with_no_applicants = jobs.filter(application__isnull=True).count()

    latest_jobs = jobs.order_by("-created_date")[:5]

    context = {
        "total_job_posted": total_job_posted,
        "total_applications_received": total_applications_received,
        "pending_applications": pending_applications,
        "accepted_applications": accepted_applications,
        "jobs_with_no_applicants": jobs_with_no_applicants,
        "latest_jobs": latest_jobs,
    }

    return render(request, "jobs/recruiter_dashboard.html", context)



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

def jobseeker_job_list(request):
    query = request.GET.get("q", "").strip()

    jobs = Job.objects.filter(status="open")

    if query:
        jobs = jobs.filter(
            Q(job_title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )

    paginator = Paginator(jobs, 8)  # 8 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "jobseeker_job_list_page_obj": page_obj,
        "query": query,
    }

    return render(request, "jobs/jobseeker_job_list.html", context)

@login_required(login_url='login')
def apply_job(request, job_id):
    if request.user.roles != "jobseeker":
        return redirect('recruiter_dashboard')

    job = Job.objects.get(id=job_id)

    if job.status == "closed":
        messages.error(request, "This job is closed and not accepting applications.")
        return redirect("job_detail", job_id=job.id)
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

@login_required(login_url="login")
def toggle_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.posted_by:
        return redirect("login")

    if job.status == "open":
        job.status = "closed"
        messages.success(request, "Job closed successfully.")
    else:
        job.status = "open"
        messages.success(request, "Job reopened successfully.")

    job.save()
    return redirect("recruiter_dashboard")