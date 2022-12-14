import os
import pathlib
from datetime import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timesince import timesince
from django.utils.translation import activate, gettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.documents.models import Document, AbstractDocument

from wagtail.models import Page, Orderable
from . import blocks
from core import tools

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
# Genres functionality end

class Project(Page):
    template = 'project' + os.sep + 'project.html'
    parent_page_types = ['Projects']

    date = models.DateField(verbose_name=_('Started'), auto_now_add=False, blank=True, null=True, )
    representative_image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
    )
    body = RichTextField(blank=True)
    is_public = models.BooleanField(default=False)
    # order_number = models.IntegerField(default=100)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('is_public'),
            # FieldPanel('order_number'),
            FieldPanel('body'),
            FieldPanel('representative_image'),
        ],
                heading=_("Project Options"),
        ),
        MultiFieldPanel(
                [InlinePanel("project_genres", label=_("Genre"))],
                heading=_("Additional data"),
        ),
    ]

    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super(Project, self).get_context(request)
        context['folders'] = self.get_children().type(FileFolder)
        context['news'] = self.get_children().type(NewsArticle)
        return context

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        # ordering = ['-date']

class Projects(Page):
    template = 'project'+os.sep+'projects.html'
    max_count_per_parent = 1
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = _("Projects index page")


class FileFolder(Page):
    template = 'project' + os.sep + 'file-folder.html'
    parent_page_types = ['Project', 'FileFolder']
    subpage_types = ['FileFolder']

    folder_date = models.DateField(auto_now_add=True)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "Project folder"
        verbose_name_plural = "Project folders"

    def get_project(self):
        """
        get first parent type: Project
        :return: top parent project
        """
        return self.get_ancestors().type(Project).last()

    def is_open(selfself):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('file_in_folder', heading=_("File header"), label=_("File label")),
    ]
    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)
        context['parent_project'] = self.get_ancestors().type(Project).last()  # get Project for FileFolder because have recursion for FileFolder

        return context


class FileInFolder(Orderable):  # TODO: create page for file if can_preview like /filefolder/file/<pk>
    # title = models.CharField(max_length=255, blank=True, null=True)
    page = ParentalKey(FileFolder, on_delete=models.CASCADE, related_name='file_in_folder')
    name = models.CharField(max_length=255, blank=True, null=True)
    can_preview = models.BooleanField(default=False)  # TODO: if picture = auto set to True
    file = models.FileField(upload_to=tools.file_path)  # TODO: upload_to method need to know project and folder name for create dirs

    panels = [
        FieldPanel('name'),
        FieldPanel('file'),
        FieldPanel('can_preview'),
    ]

    def __str__(self):
        return self.name

    def get_project(self):
        """
        get first parent type: Project
        :return: top parent project
        """
        return self.get_ancestors().type(Project).last()

    def is_open(selfself):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

    def have_preview(self):
        file_extension = pathlib.Path(self.file.name).suffix
        if file_extension in settings.PREVIEW_EXT:
            return True
        else:
            return False

    def previev_ico(self):
        file_extension = pathlib.Path(self.file.name).suffix

        if file_extension in settings.PICTURE_EXT:
            return self.file.url  # settings.PICTURE_ICON
        if file_extension in settings.VIDEO_EXT:
            return settings.VIDEO_ICON
        return settings.DEFAULT_DOWNLOAD_ICON


class NewsArticle(Page):
    template = 'project' + os.sep + 'news_article.html'
    parent_page_types = ['Project']
    subpage_types = []
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    news_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, default=None)
    article_date = models.DateField(verbose_name=_('Created'), auto_now_add=True,)
    featured_image = models.FileField(upload_to=tools.file_path, blank=True, null=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('news_project'),
        FieldPanel('featured_image'),
        FieldPanel('body'),

    ]

    def is_open(selfself):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

    def __str__(self):
        return self.title

    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)

        return context

    def get_project(self):
        """
        get first parent type: Project
        :return: top parent project
        """
        return self.get_ancestors().type(Project).last()

    def is_open(selfself):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public



class FilesToFolder(models.Model):
    user = models.ForeignKey(
        FileFolder, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_project(self):
        """
        get first parent type: Project
        :return: top parent project
        """
        return self.get_ancestors().type(Project).last()

    def is_open(selfself):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    filegroup = models.ForeignKey(
            FileInFolder, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description


