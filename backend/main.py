from flask import Flask, Response
from flask_cors import CORS
from logging.config import dictConfig
from logger import Logger
from globals import DEBUG_MODE, CORS_ALLOW
from api import api

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/server.log",
                "maxBytes": 31457280,
                "backupCount": 10,
                "delay": "True",
            },
        },
        "loggers": {
            "GPTscholar": {
                "handlers": [],
                "level": "DEBUG" if DEBUG_MODE else "INFO",
            },
        },
        "root": {
            "level": "DEBUG" if DEBUG_MODE else "INFO",
            "handlers": ["console", "file"],
        },
    }
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": CORS_ALLOW}})

app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    if DEBUG_MODE:
        Logger().info(
            """
            You are running the app in debug mode. This is not recommended for production environments.

            For production environments, please set the environment variable APP_ENV to 'production'
            before starting the server.
            """
        )

        app.run(host="0.0.0.0", debug=True)
    else:
        # Only import waitress if we are running in production mode
        from waitress import serve

        Logger().info("Server starting in production mode.")
        serve(app, host="0.0.0.0", port=5000)
