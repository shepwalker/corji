# This Python file uses the following encoding: utf-8
from flask import Flask


from corji.logging import Logger
import corji.settings as settings
from corji.views.marketing import marketing_blueprint
from corji.views.stripe import stripe_blueprint
from corji.views.twilio import twilio_blueprint

# Why yes, this *is* janky as hell.  Needed to avoid circular imports.
app = Flask(__name__)

app.config.from_object('corji.settings.Config')
app.register_blueprint(marketing_blueprint)
app.register_blueprint(stripe_blueprint)
app.register_blueprint(twilio_blueprint)


logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)
