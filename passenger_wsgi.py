import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'server.py')
application = wsgi.application
# application = get_asgi_application()  # Uncomment this line if using ASGI
