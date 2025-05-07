from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.redirect_after_login, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/available/', views.available_projects, name='available_projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/issues/create/', views.create_issue, name='create_issue'),
    path('projects/<int:project_id>/pick/', views.pick_project, name='pick_project'),
    path('projects/<int:project_id>/update-status/', views.update_project_status, name='update_project_status'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('qa-reported-projects/', views.qa_reported_projects, name='qa_reported_projects'),
    path('issues/<int:issue_id>/update-status/', views.update_issue_status, name='update_issue_status'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('tracker/qa-dashboard/', views.qa_dashboard, name='qa_dashboard'),
    path('issue/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('qa/projects/', views.qa_available_projects, name='qa_available_projects'),  # All available projects QA can pick
    path('qa/my-projects/', views.qa_projects, name='qa_projects'),  # Projects QA has picked
    path('qa/start_testing/<int:project_id>/', views.start_testing, name='start_testing'),
    path('qa/view_issues/<int:project_id>/', views.view_issues, name='view_issues'),
    path('qa/pick-project/<int:project_id>/', views.qa_pick_project, name='qa_pick_project'),
    path('qa/projects/<int:project_id>/', views.qa_project_detail, name='qa_project_detail'),
    path('qa/projects/<int:project_id>/raise-issue/', views.raise_issue, name='raise_issue'),
    path('developer/issues/', views.developer_issues, name='developer_issues'),

    

]