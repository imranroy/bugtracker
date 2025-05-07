from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    picked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='picked_projects')
    has_issues = models.BooleanField(default=False)
    team = models.ManyToManyField(User, related_name='projects', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    qa_assigned = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='qa_projects')


    def __str__(self):
        return self.name


class Issue(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed")
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"


class Bug(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('reported', 'Reported'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved')
        ],
        default='reported'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bug in {self.project.name} reported by {self.reported_by.username}"
