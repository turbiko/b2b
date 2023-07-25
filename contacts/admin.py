from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from contacts.models import ProjectRole, Person, Contacts


class ManyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Contacts)
admin.site.register(Person)
admin.site.register(ProjectRole, ManyModelAdmin)
