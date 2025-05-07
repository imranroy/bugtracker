from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Project, Issue
from .forms import ProjectForm, IssueForm, UpdateIssueStatusForm
from django.db.models import Count, Q

# Home view (optional general entry)
def home(request):
    return redirect('redirect_after_login')

# View to show available projects (for Developers)
@login_required
@user_passes_test(lambda user: user.groups.filter(name='Developers').exists())
def available_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'tracker/available_projects.html', {'projects': projects})

# Project list view for Managers and general use
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project_list.html', {'projects': projects})

# View to create a project (Manager only)
@login_required
def create_project(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.created_by = request.user
            proj.save()
            return redirect('project_detail', pk=proj.pk)
    else:
        form = ProjectForm()

    return render(request, 'tracker/create_project.html', {'form': form})

# Edit project (creator or Manager)
@login_required
def edit_project(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if not (request.user == proj.created_by or request.user.groups.filter(name='Manager').exists()):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=proj)

    return render(request, 'tracker/edit_project.html', {'form': form})

# Delete project (creator or Manager)
@login_required
def delete_project(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if not (request.user == proj.created_by or request.user.groups.filter(name='Manager').exists()):
        raise PermissionDenied
    proj.delete()
    return redirect('project_list')

# Project detail with related issues
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    issues = Issue.objects.filter(project=project)
    can_edit = request.user == project.created_by or request.user.groups.filter(name="Manager").exists()
    
    return render(request, 'tracker/project_detail.html', {
        'project': project,
        'issues': issues,
        'can_edit': can_edit,
    })

# Create issue (only QA or Manager)
@login_required
def create_issue(request, project_id):
    if not (request.user.groups.filter(name='QA').exists() or request.user.groups.filter(name='Manager').exists()):
        messages.error(request, "Only QA or Manager can create issues.")
        return redirect('project_detail', pk=project_id)

    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = project
            issue.created_by = request.user
            issue.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = IssueForm()
        if request.user.groups.filter(name='QA').exists():
            dev_group = Group.objects.get(name='Developers')
            form.fields['assigned_to'].queryset = dev_group.user_set.all()

    return render(request, 'tracker/create_issue.html', {'form': form, 'project': project})

# View for QA-reported projects assigned to developer
@login_required
@user_passes_test(lambda user: user.groups.filter(name='Developers').exists())
def qa_reported_projects(request):
    projects_with_issues = Project.objects.filter(
        issues__assigned_to=request.user,
        issues__status='Reported'
    ).distinct()
    return render(request, 'tracker/developer_qa_issues.html', {'projects': projects_with_issues})

# Pick a project (Developer)
@login_required
def pick_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.picked_by is None and request.user.groups.filter(name="Developers").exists():
        project.picked_by = request.user
        project.save()
        messages.success(request, "You have picked this project.")
    else:
        messages.error(request, "This project has already been picked.")

    return redirect('my_projects')

# Developer's own projects
@login_required
def my_projects(request):
    user = request.user
    projects = Project.objects.filter(picked_by=user).annotate(
        open_issues_count=Count('issues', filter=Q(issues__status='open'))
    )
    return render(request, 'tracker/my_projects.html', {'projects': projects})

# Update issue status (Developer only)
@login_required
def update_issue_status(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, assigned_to=request.user)
    if request.method == 'POST':
        form = UpdateIssueStatusForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=issue.project.id)
    else:
        form = UpdateIssueStatusForm(instance=issue)

    return render(request, 'tracker/update_issue_status.html', {'form': form, 'issue': issue})

# Role-based redirection after login
@login_required
def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        return redirect('project_list')
    elif user.groups.filter(name='Developers').exists():
        return redirect('available_projects')
    elif user.groups.filter(name='QA').exists():
        return redirect('qa_dashboard')  # only if defined
    else:
        return redirect('project_list')

@login_required
def update_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure the user has picked the project
    if project.picked_by != request.user:
        messages.error(request, "You cannot update the status of a project you haven't picked.")
        return redirect('available_projects')

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Project.STATUS_CHOICES).keys():
            project.status = status
            project.save()
            messages.success(request, "Project status updated successfully!")
            return redirect('available_projects')  # Or redirect to any other page as needed
        else:
            messages.error(request, "Invalid status selection.")
            return redirect('available_projects')
    return redirect('available_projects')

@login_required
def update_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user == project.picked_by and request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Project.STATUS_CHOICES):
            project.status = new_status
            project.save()
    return redirect('available_projects')

@login_required
def qa_dashboard(request):
    issues = Issue.objects.all().order_by('-created_at')  # Remove group filter temporarily
    return render(request, 'tracker/qa_dashboard.html', {'issues': issues})

@login_required
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    return render(request, 'tracker/issue_detail.html', {'issue': issue})

@login_required
def qa_available_projects(request):
    # Fetch all available projects that are not in progress or completed
    projects = Project.objects.filter(status__in=['open', 'in_progress'])

    # Only show projects that are not already assigned to a QA (if applicable)
    return render(request, 'tracker/qa_available_projects.html', {'projects': projects})

@login_required
def start_testing(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure the user is a QA and can start testing
    if request.user.role != 'QA':
        messages.error(request, "You do not have permission to start testing this project.")
        return redirect('qa_available_projects')
    
    # Change the project status to 'in_progress'
    project.status = 'in_progress'
    project.save()

    messages.success(request, "You have started testing the project.")
    return redirect('qa_available_projects')

@login_required
def view_issues(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Fetch issues related to the project
    issues = Issue.objects.filter(project=project)

    return render(request, 'tracker/view_issues.html', {'project': project, 'issues': issues})

@login_required
def qa_projects(request):
    projects = Project.objects.filter(qa_assigned=request.user).order_by('-created_at')
    return render(request, 'tracker/qa_projects.html', {'projects': projects})

@login_required
def qa_pick_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.groups.filter(name='QA').exists():
        if project.qa_assigned is None:
            project.qa_assigned = request.user
            project.status = 'in_progress'
            project.save()
            messages.success(request, "Project assigned to you and marked as In Progress.")
        else:
            messages.error(request, "This project is already assigned to a QA.")
    else:
        messages.error(request, "Only QA members can pick projects.")

    return redirect('qa_available_projects')

@login_required
def qa_project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, qa_assigned=request.user)
    issues = Issue.objects.filter(project=project).order_by('-created_at')
    return render(request, 'tracker/qa_project_detail.html', {
        'project': project,
        'issues': issues,
    })

@login_required
def raise_issue(request, project_id):
    project = get_object_or_404(Project, id=project_id, qa_assigned=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Issue.objects.create(
                title=title,
                description=description,
                project=project,
                reported_by=request.user,
                created_by=request.user 
            )
            messages.success(request, 'Issue raised successfully.')
            return redirect('qa_project_detail', project_id=project.id)
        else:
            messages.error(request, 'Title and description are required.')

    return render(request, 'tracker/raise_issue.html', {'project': project})

@login_required
def developer_issues(request):
    projects = Project.objects.filter(picked_by=request.user)
    issues = Issue.objects.filter(project__in=projects).order_by('-created_at')
    return render(request, 'tracker/developer_issues.html', {'issues': issues})
