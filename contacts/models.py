import os

from django.db import models
from django.forms import CheckboxSelectMultiple

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable, Locale
from wagtail.users.forms import User


class Contacts(Page):
    template = 'contacts' + os.sep + 'contacts.html'
    parent_page_types = ['home.HomePage']

    short_story = RichTextField(blank=True,
                                help_text='Short description of contacts')
    contacts_story = RichTextField(blank=True,
                                   help_text='Description of contacts')

    content_panels = Page.content_panels + [
        FieldPanel('short_story'),
        FieldPanel('contacts_story'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['user'] = request.user
        contact_list = Person.objects.all().filter(locale=Locale.get_active()).filter(is_contact=True)
        print("contact_list: ", contact_list)
        context['contact_list'] = contact_list

        return context


class Person(Page):
    template = 'contacts' + os.sep + 'person.html'
    parent_page_types = ['Contacts']

    is_contact = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    representative_image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    company_position = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    content_panels = Page.content_panels + [
        FieldPanel('user'),
        FieldPanel('is_contact'),
        FieldPanel('representative_image'),
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('description'),
        FieldPanel('company'),
        FieldPanel('company_position'),
    ]


class ProjectRole(Page):
    template = 'contacts' + os.sep + 'project_role.html'
    parent_page_types = ['project.Project']

    role = models.CharField(max_length=100)
    persons = models.ManyToManyField(Person, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('role'),
        FieldPanel('persons'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['user'] = request.user
        context['person_list'] = self.persons.all()
        print("person_list: ", self.persons.filter(locale=Locale.get_active()).all())
        return context