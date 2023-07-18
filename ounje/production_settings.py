import os

import dj_database_url
from decouple import config


DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}

