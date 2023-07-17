import os

import dj_database_url
from decouple import config

from ounje.settings import BASE_DIR

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}

