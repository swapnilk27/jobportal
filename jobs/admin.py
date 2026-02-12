from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company_name", "location", "status", "created_date")
    list_filter = ("status", "location", "created_date")
    search_fields = ("job_title", "company_name", "location")
