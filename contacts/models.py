from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from core import tools

class Contacts(Page):
    template = 'contacts/contacts.html'

    short_story = RichTextField(blank=True)
    contacts_story = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_story'),
        FieldPanel('contacts_story'),
    ]
class Company(Page):
    template = 'contacts/company.html'
    name = models.CharField(max_length=100)
    content_panels = Page.content_panels + [
        FieldPanel('name'),
    ]
    def __str__(self):
        return self.name

class CompanyStuff(Page):
    template = 'contacts/company_stuff.html'
    name = models.CharField(max_length=100)
    content_panels = Page.content_panels + [
        FieldPanel('name'),
    ]
    def __str__(self):
        return self.name

class Contact(Page):
    template = 'contacts/contact.html'
    featured_image = models.FileField(upload_to=tools.file_path, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    company_name = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    staff_name = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    email = models.EmailField()

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('first_name'),
        FieldPanel('company_name'),
        FieldPanel('staff_name'),
        FieldPanel('email'),
    ]
