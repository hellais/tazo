import os
from utils import INSTANCE_FOLDER_PATH

from .testlists import load_category_codes, load_country_codes

# XXX changeme
TEST_LISTS_REPO = os.path.join(INSTANCE_FOLDER_PATH, 'test-lists')
category_codes = load_category_codes(TEST_LISTS_REPO)
country_codes = load_country_codes(TEST_LISTS_REPO)

class BaseConfig(object):
    APP_NAME = 'tazo'
    APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'super sekrit'
    CELERY_BROKER_URL = "redis://localhost:6379/"
    CELERY_BACKEND = "redis://localhost:6379/"
    TEST_LISTS_LOCK = "/tmp/test-list.lock"
    GITHUB_USERNAME = None
    GITHUB_PASSWORD = None
    TARGET_REPO = "hellais/test-lists"

class DefaultConfig(BaseConfig):
    DEBUG = True
    TEST_LISTS_REPO = TEST_LISTS_REPO
