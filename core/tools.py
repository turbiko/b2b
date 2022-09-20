import os
import uuid
from datetime import datetime


def file_path(instance, filename) -> str:   # TODO: upload_to need to know project and folder name for create dirs
    print('file_path Instance= ', instance)
    _, file_extension= os.path.splitext(filename)
    filename = datetime.now().strftime('%Y/%m/')+'f-'+uuid.uuid4().hex
    return 'projects/{project_filename}{ext}'.format(project_filename=filename, ext=file_extension)




