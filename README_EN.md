# Django-Blog

### About

Blog on the Django framework. 
The main functions are implemented. 
Available extensions and edits.

### Basic Features

Admin panel.
Posts model
Static Pages.
Tags
Friendly URL.
Sitemap
Send mail

### Install

1. Set dependencies from ``requirements.txt``
2. Copy the ``"blog"`` folder to your project.
3. Create a PostgreSQL database
4. Add the ``pg_trgm module`` to the database  
`CREATE EXTENSION pg_trgm;`

5. Edit settyngs.py

```python
SITE_ID = 1

INSTALLED_APPS = [
	...
	'django.contrib.sites',
    'django.contrib.sitemaps',
    'martor',
    'crispy_forms',
    'blog',
    'django.contrib.admin', # переместить в конец
]

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
    	...
        'DIRS': [TEMPLATE_DIR],
       	...
    },
]

DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.postgresql_psycopg2',
 'NAME': 'BASE_NAME',
 'USER': 'BASE_USER',
 'PASSWORD': 'BASE_PASSWORD',
 'HOST': 'localhost',
 'PORT': '',
 }
}

# email (yandex.ru)
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "yourLogin@yandex.ru"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_REDIRECT_URL = '/'

# lang
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = False

# time
USE_TZ = True
TIME_ZONE = 'UTC'
DATE_FORMAT = 'd E Y'

# static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_prod")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

```

6. Edit url.py  
```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
```

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('blog.urls')),
    path('martor/', include('martor.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

7. Execute commands:

```bash
manage.py migrate
manage.py createsuperuser
manage.py makemigrations blog
manage.py migrate blog
```

8. Start the server.

```bash
manage.py runserver
```
