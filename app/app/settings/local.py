# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's1a40j)l1le!dbk@-iv=24oll(_1j*&b2k+%ev^xe%019&-sa-'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wagtailsite',
        'USER': 'wagtailsite',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}