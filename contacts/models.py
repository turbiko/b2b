import os

from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.users.forms import User



class Contacts(Page):
    template = 'contacts' + os.sep + 'contacts.html'
    parent_page_types = ['home.HomePage']

    short_story = RichTextField(blank=True)
    contacts_story = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('short_story'),
        FieldPanel('contacts_story'),
    ]


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
        FieldPanel('representative_image'),
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('description'),
        FieldPanel('company'),
        FieldPanel('company_position'),
    ]
