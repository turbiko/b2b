import logging
from datetime import datetime

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

logger = logging.getLogger('project')

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 2  # TODO: need for each locale 1 HomePage

    def get_context(self, request):
        # https://learnwagtail.com/tutorials/how-to-paginate-your-wagtail-pages/
        # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        logger.info(f'Homepage (get_context) was accessed by {request.user} ')
        context = super().get_context(request)
        user = request.user
        user_groups = []

        for group in user.groups.all():
            user_groups.append(group.name)

        projects = Projects.accessible(request=request)

        context['projects'] = projects

        logger.info(f'Homepage (get_context): {user} {projects.count()=}')

        return context

    class Meta:
        verbose_name = "B2B main page"
