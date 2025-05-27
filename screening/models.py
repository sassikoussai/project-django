import datetime
from datetime import timezone
from email.policy import default
<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator, EmailValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError

def validate_latitude(value):
    if not (-90 <= value <= 90):
        raise ValidationError("Latitude must be between -90 and 90 degrees.")

def validate_longitude(value):
    if not (-180 <= value <= 180):
        raise ValidationError("Longitude must be between -180 and 180 degrees.")

class EdgeNode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])
    status = models.CharField(max_length=20, choices=[("healthy", "Healthy"), ("unhealthy", "Unhealthy")], default="healthy")
    api_key = models.CharField(max_length=40, unique=True)  # For secure comms
    registered_at = models.DateTimeField(auto_now_add=True)
    last_health_check = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class APIRequestLog(models.Model):
    edge_node = models.ForeignKey(EdgeNode, related_name='api_logs', on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.FloatField()
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])
    status_code = models.IntegerField()
    client_ip = models.GenericIPAddressField()
    extra_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.edge_node.name} @ {self.request_time}"
=======

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator, EmailValidator, MinValueValidator
>>>>>>> d30f84b59699fed65edce0472ade1c9665d8cb10


class TimeStampedModel(models.Model):
    """Abstract base class that provides self-updating created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Applicant(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile',null=True)
    full_name = models.CharField(max_length=190)
    email = models.EmailField(validators=[EmailValidator()])
    birthdate = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, validators=[
        RegexValidator(r'^\+?[0-9]{8,15}$', 'Enter a valid phone number.')
    ])
    skills = models.TextField()
    linkedin_profile = models.URLField(blank=True)

    class Meta:
        ordering = ['full_name']
        db_table = 'applicant'
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['email'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_applicant_email')
        ]

    def __str__(self):
        return self.full_name


class Recruiter(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile',null=True)
    company_name = models.CharField(max_length=190)
    position = models.CharField(max_length=190)
    contact_email = models.EmailField(validators=[EmailValidator()])

    class Meta:
        ordering = ['company_name']
        db_table = 'recruiter'
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['contact_email'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['contact_email'], name='unique_recruiter_email')
        ]

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class Job(TimeStampedModel):
    recruiter = models.CharField(max_length=190)
    applicants = models.ManyToManyField(Applicant, related_name='applied_jobs', blank=True)
    title = models.CharField(max_length=190)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=190)
    salary_range = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']
        db_table = 'job'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location'])
        ]

    def __str__(self):
        return self.title


class Resume(TimeStampedModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx'])
    ])
    parsed_text = models.TextField(blank=True)
    extracted_skills = models.TextField(blank=True)
    ai_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ['-id']
        db_table = 'resume'
        indexes = [
            models.Index(fields=['applicant']),
            models.Index(fields=['ai_score'])
        ]

    def __str__(self):
        return f"Resume of {self.applicant.full_name}"


class Interview(TimeStampedModel):
    INTERVIEW_MODE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
    ]

    INTERVIEW_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='interviews')
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=20, choices=INTERVIEW_MODE_CHOICES)
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'time']
        db_table = 'interview'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['job', 'applicant'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['job', 'applicant', 'date', 'time'], name='unique_interview_schedule')
        ]

    def __str__(self):
        return f"Interview for {self.applicant.full_name} on {self.date} at {self.time}"


class ScreeningQuestion(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='screening_questions')
    question_text = models.TextField()
    answer_text = models.TextField(blank=True)

    class Meta:
        ordering = ['job', 'question_text']
        db_table = 'screening_question'
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['question_text'])
        ]

    def __str__(self):
        return f"Question for {self.job.title}: {self.question_text}"


class ScreeningAnswer(TimeStampedModel):
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE, related_name='answers')
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='screening_answers')
    answer_text = models.TextField()

    class Meta:
        ordering = ['question', 'applicant']
        db_table = 'screening_answer'
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['applicant'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['question', 'applicant'], name='unique_screening_answer')
        ]

    def __str__(self):
        return f"Answer by {self.applicant.full_name} for question: {self.question.question_text}"


class Feedback(TimeStampedModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks',null=True)
    comments = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['-id']
        db_table = 'feedback'
        indexes = [
            models.Index(fields=['interview']),
            models.Index(fields=['reviewer'])
        ]

    def __str__(self):
        return f"Feedback for {self.interview.applicant.full_name} by {self.reviewer.username}"


class Notification(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        db_table = 'notification'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_read'])
        ]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class JobApplication(TimeStampedModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected')
    ], default='applied')

    class Meta:
        ordering = ['-created_at']
        db_table = 'job_application'
        indexes = [
            models.Index(fields=['applicant']),
            models.Index(fields=['job'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'job'], name='unique_job_application')
        ]

    def __str__(self):
        return f"Application by {self.applicant.full_name} for {self.job.title}"