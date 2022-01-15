from django.contrib import admin
from web_app.models import student

# Register your models here.
class studentadmin(admin.ModelAdmin):
    list_display = ['name','email']
admin.site.register(student, studentadmin)
