import os
import uuid
from datetime import datetime

from wagtail.models import Page


def file_path(instance, filename):
    print('file_path Instance= ', instance)
    basefilename, file_extension= os.path.splitext(filename)
    filename= datetime.now().strftime('%Y/%m/%d/')+'file-'+uuid.uuid4().hex
    return 'projects/{project_filename}{ext}'.format( project_filename= filename, ext= file_extension)


class Projects(Page):
    template = 'projectsinfo'+os.sep+'projects.html'
    max_count = 1
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = "Projects index page"


class Project(Page):
	template = 'projectsinfo' + os.sep + 'project.html'
