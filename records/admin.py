from django.contrib import admin
from .models import StudentRecord

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'course', 'year_level', 'owner')
    list_filter = ('course', 'year_level')
    search_fields = ('full_name',)
