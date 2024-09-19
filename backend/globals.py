import os

DEBUG_MODE = os.environ.get("APP_ENV", None) != "production"
FRONTEND_URL = os.environ.get('FRONTEND_URL', None)
PROTOCOL = "http"

CORS_ALLOW = f"{PROTOCOL}://{FRONTEND_URL}"
