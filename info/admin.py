from django.contrib import admin
from .models import Contact, Employee, Take_attendence
# Register your models here.

admin.site.register(Contact)
admin.site.register(Employee)
admin.site.register(Take_attendence)