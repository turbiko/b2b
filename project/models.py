import calendar
import os
import pathlib
import logging

from datetime import datetime
from operator import attrgetter

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# from django.utils.timesince import timesince
from django.utils.translation import activate, gettext_lazy as _, get_language
# from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.fields import RichTextField
from wagtail.documents.models import Document, AbstractDocument
from wagtail.api import APIField

from wagtail.models import Page, Orderable, Locale

from contacts.models import ProjectRole

from core import tools

logger = logging.getLogger('project')

# Constants
ALL_YEARS = True  # if no years filtered
ALL_MONTHS = True  # if no months filtered


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
    api_fields = [
        APIField('genre'),
    ]


# Genres functionality end

class Project(Page):
    template = 'project' + os.sep + 'project.html'
    parent_page_types = ['Projects']

    date = models.DateField(verbose_name=_('Початок'), auto_now_add=False, blank=True, null=True, )
    representative_image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+',
            help_text=_('малюнок заголовку проекту')
    )
    youtube_video_id = models.CharField(_('Youtube video ID'), max_length=50, blank=True, null=True, )
    body = RichTextField(blank=True)
    status = models.CharField(_('Статус'), max_length=50, blank=True, null=True, )
    project_type = models.CharField(_('Тип проекту'), max_length=50, blank=True, null=True, )
    production = models.CharField(_('Виробництво'), max_length=150, blank=True, null=True, )
    running_time_minutes = models.IntegerField(_('Тривалість'), blank=True, null=True, )
    project_site_link = models.URLField(_('Посилання на сторінку проекту'), blank=True, null=True, )
    is_public = models.BooleanField(default=False,
                                    help_text=_('якщо увімкнуто - бачать усі відвідувачі'))
    top_priority = models.IntegerField(default=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('is_public'),
            FieldPanel('top_priority'),
            FieldPanel('body'),
            FieldPanel('status'),
            FieldPanel('production'),
            FieldPanel('project_type'),
            FieldPanel('running_time_minutes'),
            FieldPanel('project_site_link'),
            FieldPanel('youtube_video_id'),
            FieldPanel('representative_image'),
        ],
                heading=_("Project Options"),
        ),
        MultiFieldPanel(
                [InlinePanel("project_genres", label=_("Жанр"))],
                heading=_("Додаткова інформація"),
        ),
    ]
    api_fields = [
        APIField('date'),
        APIField('is_public'),
        APIField('top_priority'),
        APIField('body'),
        APIField('status'),
        APIField('production'),
        APIField('project_type'),
        APIField('running_time_minutes'),
        APIField('project_site_link'),
        APIField('youtube_video_id'),
        APIField('representative_image'),
        APIField('project_genres'),
]

    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super(Project, self).get_context(request)
        # get child pages
        positions = self.get_children().live().type(ProjectRole)
        context['folders'] = self.get_children().type(FileFolder)
        context['news'] = self.get_children().type(NewsArticle)
        context['positions'] = positions
        print('positions', positions)
        for position in positions:
            print('position', position)
            print('position.persons.all()', position.specific.persons.all())
        return context

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекти")
        ordering = ['top_priority', '-date']


class Projects(Page):
    template = 'project' + os.sep + 'projects.html'
    max_count_per_parent = 1
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = _("Projects index page")

    @classmethod
    def accessible(cls, request):  # Projects
        active_projects = Project.objects.live().filter(locale=Locale.get_active()).order_by('-date')  # .order_by('top_priority')
        # active_projects = Project.objects.live().filter(locale=Locale.get_active())

        user = request.user

        user_groups = []
        for group in user.groups.all():
            user_groups.append(group.name)
        if user.is_authenticated:
            print(f"{user=}, {user_groups=} ")

        if user.is_superuser:
            return active_projects

        if not user.is_authenticated:
            return active_projects.filter(is_public=True)
        if user.is_authenticated:
            return active_projects.filter(is_public=True) | active_projects.filter(slug__in=user_groups)

        logger.info(f'Projects (accessible) for {request.user} {active_projects.count()=}')
        return active_projects

    def get_context(self, request):  # Projects
        # Get projects accessible for user
        all_projects = self.accessible(request=request)
        logger.info(f'Projects (get_context) for {request.user} {all_projects.count()=}')

        months_filtering = False
        years_filtering = False

        current_date = datetime.now()
        current_year = current_date.year

        # set filtering options
        this_year_months = {project.date.month for project in all_projects if
                            project.date and project.date.year == current_year}
        all_years = {project.date.year for project in all_projects if project.date}

        # this_year_months = set()
        # all_years = set()
        #
        # if all_projects:
        #     try:
        #         for project in all_projects:
        #             all_years.add(project.date.year)
        #             if project.date.year == current_year:
        #                 this_year_months.add(project.date.month)
        #     except AttributeError as e:
        #         # Handle the 'NoneType' attribute error here
        #         logger.error(f"Error: {e} 'NoneType' object has no attribute 'year'")
        logger.info(f'all_years { all_years}, \nthis_year_months {this_year_months}')

        # get filtering options
        filter_for_months = request.GET.getlist('months')
        filter_for_months = [eval(i) for i in filter_for_months]  # months as integer
        filter_for_years = request.GET.getlist('years')
        filter_for_years = [eval(i) for i in filter_for_years]  # years as integer

        # set filtering switches
        if filter_for_months:
            months_filtering = True

        if filter_for_years:
            years_filtering = True

        print('filter_for_months', filter_for_months)

        this_year_projects = all_projects.none()
        other_years_projects = all_projects.none()


        print(f'this_year_projects {filter_for_months}:', this_year_projects)
        if months_filtering:
            this_year_projects = all_projects.filter(date__year=current_year)
            this_year_projects = this_year_projects.filter(date__month__in=filter_for_months)

        if years_filtering:
            other_years_projects = all_projects.filter(date__year__in=filter_for_years)

        if years_filtering and not months_filtering:
            other_years_projects = all_projects.filter(date__year__in=filter_for_years).order_by('-date')

        if not years_filtering and not months_filtering:
            other_years_projects = all_projects.order_by('top_priority', '-date')

        # =====================finish===============================
        # context for rendering
        projects = this_year_projects | other_years_projects
        # projects = sorted(projects, key=attrgetter('date'))
        # projects = sorted(projects, key=lambda x: (x.top_priority,x.date))
        projects = sorted(projects, key=lambda x: (x.top_priority))
        months = sorted(this_year_months)
        years = sorted(all_years)
        context = {
            'projects': projects,
            'months':   months,
            'years':    years,
        }

        return context


class FilterForm(forms.Form):
    months = forms.MultipleChoiceField(
            choices=[(i, month_name) for i, month_name in enumerate(calendar.month_name)][1:],
            widget=forms.CheckboxSelectMultiple,
            required=False
    )
    years = forms.MultipleChoiceField(
            choices=[(year, year) for year in range(datetime.now().year, datetime.now().year + 2)],
            widget=forms.CheckboxSelectMultiple,
            required=False
    )


class Planned(Page):
    template = 'project' + os.sep + 'planned.html'
    # max_count_per_parent = 2
    parent_page_types = ['home.HomePage']

    filter_form = FilterForm()

    content_panels = Page.content_panels + []

    @staticmethod
    def get_releases(request):  # Planned
        """
        get list of projects, that not released.
        from today to the future
        visible depend of user groups
        """
        current_date = datetime.today()

        user = request.user
        user_groups = []
        for group in user.groups.all():
            user_groups.append(group.name)
        # all releases from today to the future
        projects = Project.objects.live().filter(locale=Locale.get_active(), date__gte=current_date)
        # filter releases by user access groups
        if not user.is_superuser:
            if not user.is_authenticated:
                return projects.filter(is_public=True)
            elif user.is_authenticated:
                projects1 = projects.filter(is_public=True)
                projects2 = projects.filter(slug__in=user_groups)
                return projects1 | projects2
        return projects

    def get_context(self, request, *args, **kwargs):  # Planned
        """
        Releases page
        this year projects grouped by month
        next year releases grouped by year
        if selected query for month filter current year releases other as usual
        if selected only year - ignore all except selected year
        """
        months_filtering = False
        years_filtering = False

        current_date = datetime.today()
        context = super().get_context(request, *args, **kwargs)
        context['releases'] = self.get_releases(request)
        # Group projects by month in current year
        projects_dict = self.get_releases(request)

        print('projects_dict: ', projects_dict)

        # get filtering options
        filter_for_months = request.GET.getlist('months')
        if filter_for_months:
            months_filtering = True
        filter_for_years = request.GET.getlist('years')
        if filter_for_years:
            years_filtering = True

        # this year projects
        this_year_months = []
        grouped_projects = {}

        if (years_filtering and months_filtering) or \
                (years_filtering and (str(current_date.year) in filter_for_years)) or \
                not years_filtering:
            this_year_projects = projects_dict.filter(date__year=current_date.year)
            for project in this_year_projects:
                month = project.date.month  # months number
                if project.date > current_date.date():  # or month >= current_month
                    if int(month) not in this_year_months:
                        this_year_months.append(int(month))
                    if months_filtering:
                        if str(month) in filter_for_months:
                            if month not in grouped_projects:
                                grouped_projects[month] = []
                            grouped_projects[month].append(project)
                    else:
                        if month not in grouped_projects:
                            grouped_projects[month] = []
                        grouped_projects[month].append(project)
                # Sort projects within each month
                for month, projects in grouped_projects.items():
                    grouped_projects[month] = sorted(projects, key=attrgetter('date'))
            # Sort months in ascending order
            grouped_projects = dict(sorted(grouped_projects.items()))

        # next years projects
        next_years_projects = projects_dict.filter(date__year__gt=current_date.year)
        next_years = [str(current_date.year)]
        next_years_grouped_projects = {}
        for project in next_years_projects:
            year = str(project.date.year)  # months number
            if year not in next_years:
                next_years.append(year)
            if years_filtering and (year not in filter_for_years):
                continue
            if year not in next_years_grouped_projects:
                next_years_grouped_projects[year] = []
            next_years_grouped_projects[year].append(project)
            # Sort projects within each month
            for year, projects in next_years_grouped_projects.items():
                next_years_grouped_projects[year] = sorted(projects, key=attrgetter('date'))

        # context for rendering
        context['grouped_projects'] = grouped_projects
        context['months'] = this_year_months
        context['years'] = next_years
        context['next_years_grouped_projects'] = next_years_grouped_projects
        return context


class FileFolder(Page):
    template = 'project' + os.sep + 'file-folder.html'
    parent_page_types = ['Project', 'FileFolder']
    subpage_types = ['FileFolder']

    folder_date = models.DateField(auto_now_add=True)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Папка проекту")
        verbose_name_plural = _("Папки проекту")

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
    parent_page_types = ['Project', 'Projects']
    subpage_types = []
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    news_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, default=None)
    article_date = models.DateField(verbose_name=_('Створено'), auto_now_add=True, )
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


class NewsPage(Page):
    template = 'project' + os.sep + 'news_page.html'
    max_count_per_parent = 1
    subpage_types = []
    parent_page_types = ['home.HomePage']
    page_description = _("Новини")

    def __str__(self):
        return self.title

    def get_context(self, request):  # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)
        context['news'] = NewsArticle.objects.all().live()
        return context


# 2023-08-29
# class FilesToFolder(models.Model):
#     user = models.ForeignKey(
#             FileFolder, on_delete=models.SET_NULL, null=True, blank=True)
#     name = models.CharField(max_length=100, null=False, blank=False)
#
#     def __str__(self):
#         return self.name
#
#     def get_project(self):
#         """
#         get first parent type: Project
#         :return: top parent project
#         """
#         return self.get_ancestors().type(Project).last()
#
#     def is_open(self):
#         parent_project = self.get_ancestors().type(Project).last()
#         return parent_project.is_public
#

# 2023-09-26
# class Photo(models.Model):
#     class Meta:
#         verbose_name = _('Фото')
#         verbose_name_plural = _('Фотографії')
#
#     filegroup = models.ForeignKey(
#             FileInFolder, on_delete=models.SET_NULL, null=True, blank=True)
#     image = models.ImageField(null=False, blank=False)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.description
