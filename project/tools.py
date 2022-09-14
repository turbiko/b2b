import os
import uuid
from datetime import datetime

from wagtail.models import Page


def file_path(instance, filename):
    print('file_path Instance= ', instance)
    basefilename, file_extension= os.path.splitext(filename)
    filename= datetime.now().strftime('%Y/%m/%d/')+'file-'+uuid.uuid4().hex
    return 'projects/{project_filename}{ext}'.format( project_filename= filename, ext= file_extension)




