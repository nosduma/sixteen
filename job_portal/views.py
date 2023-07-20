from django.shortcuts import render
from .models import Job, Candidate, Application

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_portal/job_list.html', {'jobs': jobs})

def candidate_profile(request):
    candidates = Candidate.objects.all()
    return render(request, 'job_portal/candidate_profile.html', {'candidates': candidates})
