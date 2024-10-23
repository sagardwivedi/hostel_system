from django.contrib import admin

from .models import Application, Rector, Student

# Register your models here.
admin.site.register(Student)
admin.site.register(Rector)
admin.site.register(Application)
