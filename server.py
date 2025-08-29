import sys
import os

# Path to your Django project
sys.path.insert(0, os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'milki.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
