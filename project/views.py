from os.path import splitext
from django.shortcuts import render, redirect
# from .models import FilesToFolder, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.settings.base import PREVIEW_EXT
from .models import FileFolder, FileInFolder


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

        return redirect(project_folder.url)

    context = {'filefolder': project_folder, 'project_folder':project_folder.url}
    return render(request, 'project/addfiles.html', context)
