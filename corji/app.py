# This Python file uses the following encoding: utf-8
from flask import Flask


from corji.logging import Logger
import corji.settings as settings
from corji.views.marketing import marketing_blueprint
from corji.views.stripe import stripe_blueprint
from corji.views.twilio import twilio_blueprint

# Why yes, this *is* janky as hell.  Needed to avoid circular imports.
app = Flask(__name__)

<<<<<<< HEAD
import corji.customer_data as customer_data
from corji.data_sources import (
    google_spreadsheets,
    s3
)
from corji.exceptions import CorgiNotFoundException
from corji.logging import Logger, logged_view
import corji.settings as settings
from corji.utils.emoji import (
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric,
    text_contains_emoji
)

=======
>>>>>>> 0b1b96082c68209ab3c93762f7a0d0ee95a817ba
app.config.from_object('corji.settings.Config')
app.register_blueprint(marketing_blueprint)
app.register_blueprint(stripe_blueprint)
app.register_blueprint(twilio_blueprint)


logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)
