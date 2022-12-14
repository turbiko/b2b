from django.contrib import admin
from .models import Genre, ProjectGenres, Project, Projects, FileFolder, FileInFolder, NewsArticle, FilesToFolder, Photo

admin.site.register(Genre)
admin.site.register(ProjectGenres)
admin.site.register(Project)
admin.site.register(FileFolder)
# admin.site.register(FileInFolder)
admin.site.register(NewsArticle)
admin.site.register(FilesToFolder)
admin.site.register(Photo)

@admin.register(FileInFolder)
class FileInFolderAdmin(admin.ModelAdmin):
    list_display = ("name", "page")