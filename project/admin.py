from django.contrib import admin
from .models import Genre, ProjectGenres, Project, Projects, FileFolder, FileInFolder, NewsArticle

admin.site.register(Genre)
admin.site.register(ProjectGenres)
admin.site.register(Project)
admin.site.register(FileFolder)
admin.site.register(FileInFolder)
admin.site.register(NewsArticle)
