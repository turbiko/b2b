import os

from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from core import tools

class Contacts(Page):
    template = 'contacts' + os.sep + 'contacts.html'
    parent_page_types = ['home.HomePage']
    short_story = RichTextField(blank=True)
    contacts_story = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_story'),
        FieldPanel('contacts_story'),
    ]

class Person(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

