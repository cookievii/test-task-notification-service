import os

from dotenv import load_dotenv

load_dotenv()

TESTING = False

match TESTING:

    case False:
        DEBUG = False
        SECRET_KEY = os.getenv('SECRET_KEY')
        REDIS_HOST = os.getenv('REDIS_HOST')
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": os.getenv('DB_HOST'),
                "PORT": os.getenv('DB_PORT'),
                "NAME": os.getenv('POSTGRES_DB'),
                "USER": os.getenv('POSTGRES_USER'),
                "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
            }
        }

    case True:
        DEBUG = True
        SECRET_KEY = os.getenv('SECRET_KEY')
        REDIS_HOST = '127.0.0.1'
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": "localhost",
                "PORT": "5432",
                "NAME": "postgres",
                "USER": "postgres",
                "PASSWORD": "postgres",
            }
        }
