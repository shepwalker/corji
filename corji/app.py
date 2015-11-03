# This Python file uses the following encoding: utf-8
from celery import Celery
from flask import Flask

from corji.logging import Logger
import corji.settings as settings
from corji.views.marketing import marketing_blueprint
from corji.views.stripe import stripe_blueprint
from corji.views.twilio import twilio_blueprint
from corji.views.admin import admin_blueprint

blueprints = [
    admin_blueprint,
    marketing_blueprint,
    stripe_blueprint,
    twilio_blueprint
]

# Boot up the app.
app = Flask(__name__)
app.config.from_object('corji.settings.Config')
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Boot up the celery worker.
celery = Celery(app.name, broker=settings.Config.CELERY_BROKER_URL)
celery.conf.update(app.config)

# Boot up the logger.
logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)
