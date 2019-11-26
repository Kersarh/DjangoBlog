# Django Blog

## About

Блог на основе Django framework

### Реализовано

Админ панель
Post модель для блога
Комментарии
Статические страницы
Теги 
ЧПУ (`site/frendly_link/`)
Карта сайта (sitemap.xml)
Отправка email

## Install

1. Создайте базу в PostgreSQL
2. Add the ``pg_trgm module`` to the database  
	`CREATE EXTENSION pg_trgm;`
2. Создайте виртуальное окружение
3. Установите зависимости из ``requirements.txt``  
	`pip install -r requirements.txt`
4. Создайте проект Django и скопируйте в него папку `blog`
7. Отредактируйте  `settyngs.py` 

```python
import os

# Загрузка переменных окружения
from dotenv import load_dotenv
load_dotenv(verbose=True)

INSTALLED_APPS = [
	...
	'django.contrib.sites',
    'django.contrib.sitemaps',
    'martor',
    'crispy_forms',
    'blog',
    'django.contrib.admin', # переместить в конец
]

...

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
    	...
        'DIRS': [TEMPLATE_DIR],
       	...
    },
]

...

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

...

LOGIN_REDIRECT_URL = '/'

# lang
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = False

# time
USE_TZ = True
TIME_ZONE = 'UTC'
DATE_FORMAT = 'd E Y'

# email (yandex.ru)
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "YOUR_LOGIN@yandex.ru"
EMAIL_HOST_PASSWORD = "YOUR_PASSWORD"
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# time
USE_TZ = True
TIME_ZONE = 'UTC'
DATE_FORMAT = 'd E Y'

# static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_prod")

# media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

```

6. Отредактируйте основной url.py  
```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('martor/', include('martor.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

7. Перейдите в папку проекта и выполните следующие команды:

```bash
manage.py migrate
manage.py createsuperuser
manage.py makemigrations blog
manage.py migrate blog
```

8. Запускаем сервер.

```bash
manage.py runserver
```

9. Открываем в браузере [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


