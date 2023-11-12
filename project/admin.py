from django.contrib import admin
from .models import (
    Genre,
    ProjectGenres,
    Project,
    Projects,
    FileFolder,
    FileInFolder,
    NewsArticle
)

admin.site.register(Genre)
admin.site.register(ProjectGenres)
admin.site.register(Projects)
admin.site.register(FileFolder)
admin.site.register(NewsArticle)


@admin.register(Project)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'date', 'slug' )


@admin.register(FileInFolder)
class FileInFolderAdmin(admin.ModelAdmin):
    list_display = ("name", "page")