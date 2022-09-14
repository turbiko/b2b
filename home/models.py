from django.db import models
from django.template import context
from django.utils.translation import activate, gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    ObjectList,
    TabbedInterface,
)


class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1

    def get_context(self, request):
        # https://learnwagtail.com/tutorials/how-to-paginate-your-wagtail-pages/
        # https://stackoverflow.com/questions/32626815/wagtail-views-extra-context
        context = super().get_context(request)
        return context

    class Meta:
        verbose_name = "B2B main page"


