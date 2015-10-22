from corji.app import app
from corji.api import attach_rest_api
import corji.settings as settings

application = app

if __name__ == '__main__':
    attach_rest_api(application)
    application.run(port=settings.Config.PORT)
