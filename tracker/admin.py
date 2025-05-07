from django.contrib import admin
from .models import Project, Issue

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    fields = ('name', 'description')  # Only show these fields in the form

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'description')

