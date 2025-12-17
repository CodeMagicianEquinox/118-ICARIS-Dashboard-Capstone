# grc_dashboard/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Risk(models.Model):
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('mitigated', 'Mitigated'),
        ('accepted', 'Accepted'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='risks')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    likelihood = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Likelihood score (1-5)"
    )
    impact = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Impact score (1-5)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_risks')
    mitigation_plan = models.TextField(blank=True)
    identified_date = models.DateField(default=timezone.now)
    target_closure_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def risk_score(self):
        return self.likelihood * self.impact

    def __str__(self):
        return f"{self.title} ({self.severity})"

    class Meta:
        ordering = ['-created_at']


class ComplianceFramework(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    version = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ComplianceControl(models.Model):
    STATUS_CHOICES = [
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('in_progress', 'In Progress'),
        ('not_assessed', 'Not Assessed'),
    ]

    framework = models.ForeignKey(ComplianceFramework, on_delete=models.CASCADE, related_name='controls')
    control_id = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='compliance_controls')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_assessed')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_controls')
    evidence = models.TextField(blank=True, help_text="Evidence of compliance")
    last_assessment_date = models.DateField(null=True, blank=True)
    next_assessment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.control_id}: {self.title}"

    class Meta:
        ordering = ['framework', 'control_id']
        unique_together = ['framework', 'control_id']


class Audit(models.Model):
    TYPE_CHOICES = [
        ('internal', 'Internal Audit'),
        ('external', 'External Audit'),
        ('compliance', 'Compliance Review'),
        ('security', 'Security Audit'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    audit_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='audits')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audits_conducted')
    scope = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        ordering = ['-start_date']


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues')
    related_risk = models.ForeignKey(Risk, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    related_audit = models.ForeignKey(Audit, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    due_date = models.DateField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.priority})"

    class Meta:
        ordering = ['-created_at']