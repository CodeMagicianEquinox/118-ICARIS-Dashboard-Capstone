from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Risk Management
    path('risks/', views.risk_register, name='risk_register'),
    path('risks/create/', views.risk_create, name='risk_create'),
    path('risks/<int:pk>/edit/', views.risk_update, name='risk_update'),
    path('risks/<int:pk>/delete/', views.risk_delete, name='risk_delete'),
    path('api/risk-heatmap/', views.risk_heatmap_data, name='risk_heatmap_data'),

    # User Guide
    path('user-guide/', views.user_guide, name='user_guide'),
    
    # Compliance
    path('compliance/', views.compliance_tracking, name='compliance_tracking'),
    
    # Audit Management
    path('audits/', views.audit_management, name='audit_management'),
    
    # Issue/PO&AM Tracking
    path('issues/', views.issue_tracking, name='issue_tracking'),
    path('issues/create/', views.issue_create, name='issue_create'),
    path('issues/<int:pk>/edit/', views.issue_update, name='issue_update'),
    path('issues/<int:pk>/delete/', views.issue_delete, name='issue_delete'),
    
    # Artifacts
    path('artifacts/', views.artifacts, name='artifacts'),
    path('artifacts/upload/', views.artifact_create, name='artifact_create'),
    path('artifacts/<int:pk>/delete/', views.artifact_delete, name='artifact_delete'),

    # Add these URL patterns to grc_dashboard/urls.py
# Add them to your existing urlpatterns list

    # Vulnerability Management
    path('vulnerabilities/', views.vulnerability_management, name='vulnerability_management'),
    path('vulnerabilities/<int:pk>/', views.vulnerability_detail, name='vulnerability_detail'),
    path('vulnerabilities/upload/', views.vulnerability_upload_scan, name='vulnerability_upload_scan'),
    path('vulnerabilities/<int:pk>/update-status/', views.vulnerability_update_status, name='vulnerability_update_status'),
    path('vulnerabilities/<int:pk>/add-note/', views.vulnerability_add_note, name='vulnerability_add_note'),
    path('vulnerabilities/scans/<int:pk>/delete/', views.vulnerability_scan_delete, name='vulnerability_scan_delete'),
    path('vulnerabilities/export/', views.vulnerability_export, name='vulnerability_export'),
]