import os
import sys


sys.path.insert(0, "home/pelitaba/siskerma/siskerma/app")

os.environ['DJANGO_SETTINGS_MODULE'] ='siskerma.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
