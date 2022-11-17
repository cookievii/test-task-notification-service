import os
import sys

from dotenv import load_dotenv

load_dotenv()
BUILD_TYPE = os.getenv("BUILD_TYPE", "test")
TESTING = True if len(sys.argv) > 1 and sys.argv[1] == "test" else False

if TESTING:
    BUILD_TYPE = "test"

match BUILD_TYPE:

    case "dev":
        DEBUG = False
        SECRET_KEY = os.getenv('SECRET_KEY')
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

    case "test":
        DEBUG = True
        SECRET_KEY = os.getenv('SECRET_KEY')
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
