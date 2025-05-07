from django import forms
from .models import Project, Issue
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name","description"]

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'priority', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only list active users for assignment
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)

class UpdateIssueStatusForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status']