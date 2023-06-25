import logging
import multiprocessing

from gunicorn.app.wsgiapp import WSGIApplication
from uvicorn import Config, Server

from core.config import settings
from core.logging import setup_logging


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_uri, options: dict = None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


if __name__ == "__main__":
    if settings.PROD:
        options = {
            "bind": "0.0.0.0:8000",
            "workers": (multiprocessing.cpu_count() * 2) + 1,
            "worker_class": "uvicorn.workers.UvicornWorker",
        }
        StandaloneApplication("app:app", options).run()
    else:
        log_level = logging.getLevelName(settings.LOG_LEVEL)
        server = Server(Config("app:app", log_level=log_level, reload=True, workers=1))
        setup_logging()

        server.run()
