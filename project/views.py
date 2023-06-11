import datetime
from os.path import splitext
import logging

from django.utils.translation import get_language
from django.shortcuts import render, redirect
# from .models import FilesToFolder, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.settings.base import PREVIEW_EXT
from .models import FileFolder, FileInFolder, Projects

logger = logging.getLogger(__name__)

def addPhoto(request, pk):

    project_folder = FileFolder.objects.get(pk=pk)
    previev_selector = True

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            _, extension = splitext(image.name)
            if extension.lower() in PREVIEW_EXT:
                previev_selector = True
            else:
                previev_selector = False

            photo = FileInFolder.objects.create(
                page=project_folder,
                name=image.name,
                file=image,
                can_preview=previev_selector,
            )
        project_folder.save()  # TODO change time in  last_published_at
        return redirect(project_folder.url)

    logger.info(f'{datetime.datetime.now()} | add file(s) to {project_folder.name} | {project_folder.url} | {request.user.username}')
    context = {'filefolder': project_folder, 'project_folder':project_folder.url}
    return render(request, 'project/addfiles.html', context)


def get_projects_for_user(request):
    current_year = datetime.now().year
    user = request.user
    user_groups = user.groups.all()
    is_admin = user.is_superuser
    is_authenticated = user.is_authenticated
    projects = Projects.objects.live().filter(date__year=current_year).order_by('date')
    if not user.is_authenticated:
        projects_dict = projects.filter(is_public=True)
    elif is_admin:
        projects_dict = projects
    elif is_authenticated:
        projects_dict = projects.filter(slug__in=user_groups)
    return projects_dict



def projects_planned(request):

    context = {}
    language = get_language()
    projects = get_projects_for_user(request)
    context['projects'] = projects
    context['language'] = language

    for project in projects:
        context['project'] = project


    return render(request, 'project/planned.html')