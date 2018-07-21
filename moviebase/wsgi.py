import os


configuration = os.getenv('ENVIRONMENT', 'development').title()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviebase.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
