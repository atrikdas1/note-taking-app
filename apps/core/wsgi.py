"""
This file initializes the WSGI server which pairs with the Flask application
to serve HTTP requests in a production environment
"""

# Always do this the first thing before writing any code,
# otherwise it will cause bugs related to blocking processes.
# This allows processes to be done in a more efficient manner (called cooperative multitasking)
# by enabling coroutine handling by multiple workers (eg: cores on server infrastructure)
# Reference: https://eng.lyft.com/what-the-heck-is-gevent-4e87db98a8

import gevent.monkey

gevent.monkey.patch_all()

import gunicorn.app.base
import multiprocessing

# Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX
# Format is copy-pasted from: https://docs.gunicorn.org/en/stable/custom.html

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# This enable load balancing for computationally heavy tasks.
# The formula is based on the assumption that for a given core,
# one worker will be reading or writing from the socket while the other worker is processing a request
# Reference: https://docs.gunicorn.org/en/stable/design.html#how-many-workers

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


if __name__ == "__main__":
    from core.app import create_app

    application = create_app()

    options = {
        "print_config": True,
        "check_config": True,
        "worker_class": "gevent",  # asynchronous workers based on greenlets
        "bind": ["0.0.0.0:9700", "0.0.0.0:9800"],
        "workers": number_of_workers(),
        "timeout": 300,
    }
    StandaloneApplication(application, options).run()
