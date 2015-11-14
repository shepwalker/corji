import os


class Config(object):
    # General variables.
    DEBUG = os.getenv('DEBUG', False)
    PORT = int(os.getenv('PORT', 8000))
    SITE_URL = os.getenv('SITE_URL', '127.0.0.1:8000')

    DO_NOT_DISTURB = True if (os.getenv('DO_NOT_DISTURB') == "TRUE") else False
    DASHBOARD_ENABLED = True if (os.getenv('DASHBOARD_ENABLED') == "TRUE") else False

    # Storage variables.
    FALLBACK_IMAGE = os.getenv('FALLBACK_IMAGE', 'https://s-media-cache-ak0.pinimg.com/736x/49/2a/7f/492a7ff287bdc50d34a4989ab83d9830.jpg')
    SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')
    PILES_URL = os.getenv('PILES_URL', '')
    REMOTE_CACHE_RETRIEVE = True if (os.getenv('REMOTE_CACHE_RETRIEVE') == "TRUE") else False
    REMOTE_CACHE_POPULATE = True if (os.getenv('REMOTE_CACHE_POPULATE') == "TRUE") else False
    IMAGE_RESIZE = True if (os.getenv('IMAGE_RESIZE') == "TRUE") else False
    IMAGE_RESIZE_PIXELS = os.getenv('IMAGE_RESIZE_PIXELS', 300)
    PREGENERATE_S3_URLS = os.getenv('PREGENERATE_S3_URLS', False)
    MAXIMUM_S3_FILESIZE = os.getenv('MAXIMUM_S3_FILESIZE', 400000)

    # Operational variables.
    LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
    LOG_PATH = os.getenv('LOG_PATH', './.logs')
    LOGGER_NAME = "FLASK_APP_LOGGER"

    # Celery.
    CELERY_BROKER_URL = "sqs://"

    # Frontend variables.
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')

    # Twilio variables.
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

    # AWS variables.
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'SUPER_NOT_VALID_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'SUPER_NOT_VALID_SECRET')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-west-1')
    AWS_S3_CACHE_BUCKET_NAME = os.getenv('AWS_S3_CACHE_BUCKET_NAME', 'corji')
    AWS_PRELOAD_EXPIRATION_TIME = os.getenv('AWS_PRELOAD_EXPIRATION_TIME', 31540000)
    AWS_DYNAMO_TABLE_NAME = os.getenv('AWS_DYNAMO_TABLE_NAME', 'corji')

    # Stripe.
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    FREE_CONSUMPTIONS = 20
    CONSUMPTIONS_PER_RECHARGE = 50
    RECHARGE_PRICE = 199  # In cents.
