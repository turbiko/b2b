import os
from datetime import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import activate, gettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from wagtail.models import Page, Orderable
from .tools import file_path


# Genres functionality
class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectGenres(Orderable):
    genre = models.ForeignKey(Genre, related_name='+', null=True, on_delete=models.SET_NULL)
    page = ParentalKey('project.Project', related_name='project_genres')
    panels = [
        FieldPanel('genre'),
    ]


class Project(Page):
    template = 'project' + os.sep + 'project.html'
    parent_page_types = ['Projects']
    # subpage_types = ['ProjectNews', 'ProjectFiles']
    date = models.DateField(auto_now_add=False, blank=True, null=True)
    representative_image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
        FieldPanel('representative_image'),
        MultiFieldPanel(
                [InlinePanel("project_genres", label="Genre")],
                heading="Genres",
        ),
    ]

    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super(Project, self).get_context(request)
        # context['files'] = self.get_children().type(ProjectFiles)
        return context

    class Meta:
        ordering = ['-date']

class Projects(Page):
    template = 'project'+os.sep+'projects.html'
    max_count = 1
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = "Projects index page"
