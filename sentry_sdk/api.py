from contextlib import contextmanager

import sentry_minimal

from .hub import Hub
from .scope import Scope
from .client import Client


__all__ = ['Hub', 'Client', 'init'] + sentry_minimal.__all__


for _key in sentry_minimal.__all__:
    globals()[_key] = getattr(sentry_minimal, _key)


class _InitGuard(object):

    def __init__(self, client):
        self._client = client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        c = self._client
        if c is not None:
            c.close()


def init(*args, **kwargs):
    client = Client(*args, **kwargs)
    if client.dsn is not None:
        Hub.main.bind_client(client)
    return _InitGuard(client)