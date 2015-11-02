# This Python file uses the following encoding: utf-8
from celery import Celery
from flask import Flask

from corji.api import CorgiResource
from corji.logging import Logger
import corji.settings as settings
from corji.views.marketing import marketing_blueprint
from corji.views.stripe import stripe_blueprint
from corji.views.twilio import twilio_blueprint
from corji.views.admin import admin_blueprint

app = Flask(__name__)

app.config.from_object('corji.settings.Config')
app.register_blueprint(marketing_blueprint)
app.register_blueprint(stripe_blueprint)
app.register_blueprint(twilio_blueprint)
app.register_blueprint(admin_blueprint)

api = CorgiResource()
celery = Celery(app.name, broker=settings.Config.CELERY_BROKER_URL)
celery.conf.update(app.config)
logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)
