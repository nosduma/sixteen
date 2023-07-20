from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Add more fields as needed

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    # Add more fields as needed

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # Add more fields as needed
