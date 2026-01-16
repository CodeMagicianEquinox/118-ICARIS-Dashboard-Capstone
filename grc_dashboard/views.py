# grc_dashboard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Risk, ComplianceControl, Audit, Issue, Department
from .forms import RiskForm, ComplianceControlForm, AuditForm, IssueForm

@login_required
def dashboard(request):
    """Main GRC dashboard with key metrics and visualizations"""
    
    # Risk metrics
    total_risks = Risk.objects.count()
    critical_risks = Risk.objects.filter(severity='critical', status__in=['open', 'in_progress']).count()
    open_risks = Risk.objects.filter(status='open').count()
    
    # Compliance metrics
    total_controls = ComplianceControl.objects.count()
    compliant_controls = ComplianceControl.objects.filter(status='compliant').count()
    non_compliant_controls = ComplianceControl.objects.filter(status='non_compliant').count()
    compliance_rate = (compliant_controls / total_controls * 100) if total_controls > 0 else 0
    
    # Audit metrics
    total_audits = Audit.objects.count()
    upcoming_audits = Audit.objects.filter(
        status='planned',
        start_date__lte=timezone.now().date() + timedelta(days=30)
    ).count()
    in_progress_audits = Audit.objects.filter(status='in_progress').count()
    
    # Issue metrics
    total_issues = Issue.objects.count()
    open_issues = Issue.objects.filter(status__in=['open', 'in_progress']).count()
    overdue_issues = Issue.objects.filter(
        status__in=['open', 'in_progress'],
        due_date__lt=timezone.now().date()
    ).count()
    
    # Risk by severity
    risks_by_severity = Risk.objects.values('severity').annotate(count=Count('id'))
    
    # Compliance by status
    compliance_by_status = ComplianceControl.objects.values('status').annotate(count=Count('id'))
    
    # Recent activities
    recent_risks = Risk.objects.select_related('department', 'owner').order_by('-created_at')[:5]
    recent_audits = Audit.objects.select_related('department', 'auditor').order_by('-created_at')[:5]
    recent_issues = Issue.objects.select_related('department', 'assigned_to').order_by('-created_at')[:5]
    
    context = {
        'total_risks': total_risks,
        'critical_risks': critical_risks,
        'open_risks': open_risks,
        'total_controls': total_controls,
        'compliance_rate': round(compliance_rate, 1),
        'non_compliant_controls': non_compliant_controls,
        'total_audits': total_audits,
        'upcoming_audits': upcoming_audits,
        'in_progress_audits': in_progress_audits,
        'total_issues': total_issues,
        'open_issues': open_issues,
        'overdue_issues': overdue_issues,
        'risks_by_severity': risks_by_severity,
        'compliance_by_status': compliance_by_status,
        'recent_risks': recent_risks,
        'recent_audits': recent_audits,
        'recent_issues': recent_issues,
    }
    
    return render(request, 'grc_dashboard/dashboard.html', context)


@login_required
def risk_register(request):
    """Risk register view with filtering"""
    risks = Risk.objects.select_related('department', 'owner').all()
    
    # Apply filters
    severity_filter = request.GET.get('severity')
    status_filter = request.GET.get('status')
    department_filter = request.GET.get('department')
    
    if severity_filter:
        risks = risks.filter(severity=severity_filter)
    if status_filter:
        risks = risks.filter(status=status_filter)
    if department_filter:
        risks = risks.filter(department_id=department_filter)
    
    departments = Department.objects.all()
    
    context = {
        'risks': risks,
        'departments': departments,
        'severity_filter': severity_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
    }
    
    return render(request, 'grc_dashboard/risk_register.html', context)


@login_required
def risk_heatmap_data(request):
    """API endpoint for risk heatmap data"""
    risks = Risk.objects.all()
    
    data = []
    for risk in risks:
        data.append({
            'id': risk.id,
            'title': risk.title,
            'likelihood': risk.likelihood,
            'impact': risk.impact,
            'severity': risk.severity,
            'department': risk.department.name,
        })
    
    return JsonResponse({'risks': data})


@login_required
def compliance_tracking(request):
    """Compliance tracking view"""
    controls = ComplianceControl.objects.select_related('framework', 'department', 'owner').all()
    
    # Apply filters
    framework_filter = request.GET.get('framework')
    status_filter = request.GET.get('status')
    
    if framework_filter:
        controls = controls.filter(framework_id=framework_filter)
    if status_filter:
        controls = controls.filter(status=status_filter)
    
    from .models import ComplianceFramework
    frameworks = ComplianceFramework.objects.all()
    
    context = {
        'controls': controls,
        'frameworks': frameworks,
        'framework_filter': framework_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'grc_dashboard/compliance_tracking.html', context)


@login_required
def audit_management(request):
    """Audit management view"""
    audits = Audit.objects.select_related('department', 'auditor').all()
    
    # Apply filters
    type_filter = request.GET.get('type')
    status_filter = request.GET.get('status')
    
    if type_filter:
        audits = audits.filter(audit_type=type_filter)
    if status_filter:
        audits = audits.filter(status=status_filter)
    
    context = {
        'audits': audits,
        'type_filter': type_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'grc_dashboard/audit_management.html', context)


@login_required
def issue_tracking(request):
    """Issue tracking view"""
    issues = Issue.objects.select_related('department', 'assigned_to').all()
    
    # Apply filters
    priority_filter = request.GET.get('priority')
    status_filter = request.GET.get('status')
    
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    context = {
        'issues': issues,
        'priority_filter': priority_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'grc_dashboard/issue_tracking.html', context)


# Create Risk (if you want to re-enable adding later)
@login_required
def risk_create(request):
    """Create a new ConMon requirement"""
    if request.method == 'POST':
        form = RiskForm(request.POST, request.FILES)
        if form.is_valid():
            risk = form.save(commit=False)
            
            # If evidence file is uploaded, mark as uploaded
            if 'evidence_file' in request.FILES:
                risk.evidence_uploaded = True
                from django.utils import timezone
                risk.last_evidence_update = timezone.now()
            
            risk.save()
            messages.success(request, 'ConMon requirement created successfully!')
            return redirect('risk_register')
    else:
        form = RiskForm()
    
    return render(request, 'grc_dashboard/risk_form.html', {
        'form': form,
        'action': 'Create'
    })





@login_required
def risk_update(request, pk):
    """Update/Edit a ConMon requirement"""
    risk = get_object_or_404(Risk, pk=pk)
    
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            return redirect('risk_register')
    else:
        form = RiskForm(instance=risk)
    
    return render(request, 'grc_dashboard/risk_form.html', {'form': form, 'action': 'Update'})


@login_required
def risk_delete(request, pk):
    """Delete a ConMon requirement"""
    risk = get_object_or_404(Risk, pk=pk)
    
    if request.method == 'POST':
        risk.delete()
        return redirect('risk_register')
    
    return render(request, 'grc_dashboard/risk_confirm_delete.html', {'risk': risk})

@login_required
def artifacts(request):
    """Artifacts document management view"""
    context = {
        'artifacts': [],
    }
    return render(request, 'grc_dashboard/artifacts.html', context)

# CRUD Views for Issues/PO&AMs
@login_required
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if not issue.assigned_to:
                issue.assigned_to = request.user
            issue.save()
            return redirect('issue_tracking')
    else:
        form = IssueForm()
    
    return render(request, 'grc_dashboard/issue_form.html', {'form': form, 'action': 'Create'})


@login_required
def issue_update(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issue_tracking')
    else:
        form = IssueForm(instance=issue)
    
    return render(request, 'grc_dashboard/issue_form.html', {'form': form, 'action': 'Update', 'issue': issue})


@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        issue.delete()
        return redirect('issue_tracking')
    
    return render(request, 'grc_dashboard/issue_confirm_delete.html', {'issue': issue})

# CRUD Views for Artifacts
@login_required
def artifact_create(request):
    from .models import Artifact
    from .forms import ArtifactForm
    
    if request.method == 'POST':
        form = ArtifactForm(request.POST, request.FILES)
        if form.is_valid():
            artifact = form.save(commit=False)
            artifact.uploaded_by = request.user
            artifact.save()
            return redirect('artifacts')
    else:
        form = ArtifactForm()
    
    return render(request, 'grc_dashboard/artifact_form.html', {'form': form, 'action': 'Upload'})


@login_required
def artifact_delete(request, pk):
    from .models import Artifact
    
    artifact = get_object_or_404(Artifact, pk=pk)
    
    if request.method == 'POST':
        # Delete the file from storage
        artifact.file.delete()
        artifact.delete()
        return redirect('artifacts')
    
    return render(request, 'grc_dashboard/artifact_confirm_delete.html', {'artifact': artifact})