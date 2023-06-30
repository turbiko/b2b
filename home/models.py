from django.db import models
from django.template import context
from django.utils.translation import activate, gettext_lazy as _, get_language
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.fields import RichTextField

from wagtail.models import Page, Orderable, Locale
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.admin.panels import (
    ObjectList,
    TabbedInterface,
)
from project.models import Project, Projects

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 2  # TODO: need for each locale 1 HomePage

    def get_context(self, request):
        # https://learnwagtail.com/tutorials/how-to-paginate-your-wagtail-pages/
        # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)
        user = request.user
        user_groups = user.groups.all()
        language = get_language()

        projects = Project.objects.live().filter(locale=Locale.get_active())

        if not user.is_superuser:
            if not user.is_authenticated:
                projects = projects.filter(is_public=True)
            elif user.is_authenticated:
                projects = projects.filter(is_public=True) | projects.filter(slug__in=user_groups)

        context['projects'] = projects

        print(f'{user=} {user_groups=}' )
        print(f'{projects=} {projects.count()}' )
        return context

    class Meta:
        verbose_name = "B2B main page"

