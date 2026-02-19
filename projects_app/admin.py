from django.contrib import admin
from .models import Project, Certificate

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    list_filter = ['created_date']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issued_date']
    list_filter = ['issuer', 'issued_date']
    search_fields = ['title', 'issuer']