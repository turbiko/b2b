from django.shortcuts import render, redirect
# from .models import FilesToFolder, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import FileFolder, FileInFolder


def addPhoto(request, pk):
    project_folder = FileFolder.objects.get(pk=pk)
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            print(image)
            photo = FileInFolder.objects.create(
                page=project_folder,
                name=project_folder.title+' - '+data['description'] + ' - ' + image.name,
                file=image,
                can_preview=True,
            )

        return redirect(project_folder.url)

    context = {'filefolder': project_folder, 'project_folder':project_folder.url}
    return render(request, 'project/addfiles.html', context)