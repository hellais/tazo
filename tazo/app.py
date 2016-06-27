from celery import Celery
from flask import Flask

from .utils import INSTANCE_FOLDER_PATH
from .config import DefaultConfig
from .api import api
from .frontend import frontend

DEFAULT_BLUEPRINTS = [
    api,
    frontend
]

def create_app(config=None, app_name=None, blueprints=None):
    if app_name is None:
        app_name = __name__
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH,
                instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, blueprints)

    return app

def configure_app(app, config):
    app.config.from_object(DefaultConfig)

    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def create_celery():
    app = create_app()
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
