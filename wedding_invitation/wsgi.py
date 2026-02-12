"""
WSGI config for wedding invitation project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')

application = get_wsgi_application()
