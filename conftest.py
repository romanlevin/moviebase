import configurations
import os


def pytest_configure():
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviebase.settings')
    configurations.setup()
