from django.contrib import admin

from contacts.models import ProjectRole, Person, Contacts

admin.site.register(Contacts)
admin.site.register(Person)
admin.site.register(ProjectRole)
