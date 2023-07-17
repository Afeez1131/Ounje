import dj_database_url
from decouple import config

from ounje.settings import BASE_DIR

DEBUG = True
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'), conn_max_age=600),
}

