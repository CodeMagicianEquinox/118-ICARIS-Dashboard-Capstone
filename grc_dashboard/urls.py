# grc_dashboard/urls.py
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
    
    # Compliance
    path('compliance/', views.compliance_tracking, name='compliance_tracking'),
    
    # Audit Management
    path('audits/', views.audit_management, name='audit_management'),
    
    # Issue Tracking
    path('issues/', views.issue_tracking, name='issue_tracking'),
]