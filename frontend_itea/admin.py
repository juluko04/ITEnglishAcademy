from django.utils.html import format_html
from .models import Courses, Dates
from django.contrib import admin

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'unitys')
    search_fields = ('name', 'description')

@admin.register(Dates)
class DatesAdmin(admin.ModelAdmin):
    list_display = ('date_name', 'courses', 'start_date', 'end_date')
    search_fields = ('date_name', 'courses__name')
    list_filter = ('start_date', 'end_date')
