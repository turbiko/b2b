from os.path import splitext
import logging

from django.shortcuts import render, redirect
# from .models import FilesToFolder, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.settings.base import PREVIEW_EXT
from .models import FileFolder, FileInFolder

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
    logger.info(project_folder.url + " | " + request.user.username)
    context = {'filefolder': project_folder, 'project_folder':project_folder.url}
    return render(request, 'project/addfiles.html', context)
