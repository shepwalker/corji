from corji.app import app
import corji.settings as settings

application = app
if __name__ == '__main__':
    application.run(port=settings.Config.PORT)
