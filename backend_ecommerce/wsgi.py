import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_ecommerce.settings")
application = get_wsgi_application()
# Vercel tìm biến "app"
app = application
