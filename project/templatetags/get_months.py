from datetime import datetime
import locale
import calendar

from django import template
from django.utils import translation
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def months_by_num(value, months_number):
    # fake func for example
    today = datetime.today()
    datem = datetime(today.year, months_number, 1)
    return datem


@register.filter
def get_date(value):
    print(value)
    return value.date()
