from django.db import models
from django.template import context
from django.utils.translation import activate, gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.fields import RichTextField

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.admin.panels import (
    ObjectList,
    TabbedInterface,
)
from project.models import Project

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 2  # TODO: need for each locale 1 HomePage

    def get_context(self, request):
        # https://learnwagtail.com/tutorials/how-to-paginate-your-wagtail-pages/
        # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)
        user = request.user
        user_groups = user.groups.all()
        projects = Project.objects.live()
        projects_dict = projects
        if user.is_superuser:
            context['projects'] = projects_dict
            return context

        if not user.is_authenticated:
            projects_dict = projects.filter(is_public=True)
        else:
            projects_dict = projects.filter(is_public=True) | projects.filter(slug__in=user_groups)

        context['projects'] = projects_dict

        return context

    class Meta:
        verbose_name = "B2B main page"

