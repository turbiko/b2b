import os
import pathlib
import locale
from datetime import datetime
import uuid
from operator import attrgetter

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timesince import timesince
from django.utils.translation import activate, gettext_lazy as _, get_language

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.fields import RichTextField
from wagtail.documents.models import Document, AbstractDocument

from wagtail.models import Page, Orderable, Locale
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

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('is_public'),
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
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        # ordering = ['-date']


class Projects(Page):
    template = 'project' + os.sep + 'projects.html'
    max_count_per_parent = 1
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = _("Projects index page")


class Planned(Page):
    template = 'project' + os.sep + 'planned.html'
    # max_count_per_parent = 2
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        current_date = datetime.now()
        current_year = current_date.year
        context = {}

        language = get_language()

        user = request.user
        user_groups = user.groups.all()

        projects = Project.objects.live().filter(locale=Locale.get_active())

        if not user.is_superuser:
            if not user.is_authenticated:
                projects = projects.filter(is_public=True)
            elif user.is_authenticated:
                projects = projects.filter(is_public=True) | projects.filter(slug__in=user_groups)

        projects_dict = projects

        projects_current_year = projects_dict.filter(date__year=current_year)

        # Group projects by month
        grouped_projects = {}
        for project in projects_current_year:
            month = project.date.month  # months number
            if project.date > current_date.date():  # or month >= current_month
                if month not in grouped_projects:
                    grouped_projects[month] = []
                grouped_projects[month].append(project)
            # Sort projects within each month
            for month, projects in grouped_projects.items():
                grouped_projects[month] = sorted(projects, key=attrgetter('date'))

            # Sort months in ascending order
            grouped_projects = dict(sorted(grouped_projects.items()))

            # Next year projects
            next_year = current_year + 1
            projects = Project.objects.live().filter(locale=Locale.get_active())
            projects_next_year = projects.filter(date__year=next_year)

            # Get month names based on language
            context['grouped_projects'] = grouped_projects

            context['next_year'] = next_year
            context['next_year_projects'] = projects_next_year

            context['language'] = language

        return context


class FileFolder(Page):
    template = 'project' + os.sep + 'file-folder.html'
    parent_page_types = ['Project', 'FileFolder']
    subpage_types = ['FileFolder']

    folder_date = models.DateField(auto_now_add=True)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Project folder")
        verbose_name_plural = _("Project folders")

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
        context['parent_project'] = self.get_ancestors().type(
            Project).last()  # get Project for FileFolder because have recursion for FileFolder

        return context


class FileInFolder(Orderable):  # TODO: create page for file if can_preview like /filefolder/file/<pk>
    page = ParentalKey(FileFolder, on_delete=models.CASCADE, related_name='file_in_folder')
    name = models.CharField(max_length=255, blank=True, null=True)
    can_preview = models.BooleanField(default=False)  # TODO: if picture = auto set to True
    file = models.FileField(
        upload_to=tools.file_path)  # TODO: upload_to method need to know project and folder name for create dirs

    panels = [
        FieldPanel('name'),
        FieldPanel('file'),
        # FieldPanel('can_preview'),
    ]

    def __str__(self):
        return self.name

    def get_project(self):
        """
        get first parent type: Project
        :return: top parent project
        """
        return self.get_ancestors().type(Project).last()

    def is_open(self):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

    def have_preview(self):
        file_extension = pathlib.Path(self.file.name).suffix
        if file_extension in settings.PREVIEW_EXT:
            return True
        else:
            return False

    def preview_ico(self):
        file_extension = pathlib.Path(self.file.name).suffix

        if file_extension in settings.PICTURE_EXT:
            return settings.PICTURE_ICON  # self.file.url
        if file_extension in settings.VIDEO_EXT:
            return settings.VIDEO_ICON
        return settings.DEFAULT_DOWNLOAD_ICON

    def preview_link_pic(self):
        file_extension = pathlib.Path(self.file.name).suffix

        if file_extension in settings.PICTURE_EXT:
            return True

        return False

    def preview_link_video(self):
        file_extension = pathlib.Path(self.file.name).suffix

        if file_extension in settings.VIDEO_EXT:
            return True

        return False


class NewsArticle(Page):
    template = 'project' + os.sep + 'news_article.html'
    parent_page_types = ['Project']
    subpage_types = []
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    news_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, default=None)
    article_date = models.DateField(verbose_name=_('Created'), auto_now_add=True, )
    featured_image = models.FileField(upload_to=tools.file_path, blank=True, null=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('news_project'),
        FieldPanel('featured_image'),
        FieldPanel('body'),

    ]

    def is_open(self):
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

    def is_open(self):
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

    def is_open(self):
        parent_project = self.get_ancestors().type(Project).last()
        return parent_project.is_public

class Photo(models.Model):
    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    filegroup = models.ForeignKey(
            FileInFolder, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
