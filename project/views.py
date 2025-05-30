import datetime
import locale
import calendar

from os.path import splitext
import logging
from itertools import groupby
from operator import attrgetter

from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from wagtail.models import Locale

from core.settings.base import PREVIEW_EXT

from .models import FileFolder, FileInFolder, Project

logger = logging.getLogger(__name__)


def add_photo(request, pk):
    logger.info(f'Page (add_photo) was accessed by {request.user} ')

    project_folder = FileFolder.objects.get(pk=pk)
    preview_selector = True

    if request.method == 'POST':
        logger.info(f'Action POST (add_photo)  by {request.user} started')
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            _, extension = splitext(image.name)
            if extension.lower() in PREVIEW_EXT:
                preview_selector = True
            else:
                preview_selector = False

            photo = FileInFolder.objects.create(
                page=project_folder,
                name=image.name,
                file=image,
                can_preview=preview_selector,
            )
        project_folder.save()  # TODO change time in  last_published_at

        logger.info(f'Action POST (add_photo)  by {request.user} sucsessful')
        return redirect(project_folder.url)
    #
    # logger.info(project_folder.url + " | " + request.user.username)
    # context = {'filefolder': project_folder, 'project_folder':project_folder.url}
    # return render(request, 'project/addfiles.html', context)

    logger.info(
        f'{datetime.datetime.now()} | add file(s) to {project_folder.name} | {project_folder.url} | {request.user.username}')
    context = {'filefolder': project_folder, 'project_folder': project_folder.url}
    return render(request, 'project/addfiles.html', context)


def get_projects_for_user(request):
    user = request.user
    user_groups = user.groups.all()

    projects = Project.objects.live()
    #  .filter(locale=Locale.get_active())
    # projects_dict = projects.filter(locale=UKR_CODE)
    projects_dict = projects.filter(locale=Locale.get_active())

    if user.is_superuser:
        return projects_dict

    if not user.is_authenticated:
        return projects.filter(is_public=True)

    elif user.is_authenticated:
        return projects.filter(is_public=True) | projects.filter(slug__in=user_groups)

    return projects_dict


def projects_planned(request):
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    context = {}
    language = get_language()

    locale.setlocale(locale.LC_ALL, language)

    projects = get_projects_for_user(request)  # return projects allowed for user
    projects_current_year = projects.filter(date__year=current_year)

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

    # Get month names based on language
    context['grouped_projects'] = grouped_projects
    context['language'] = language
    return render(request, 'project/planned.html', context)
