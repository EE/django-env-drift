import os

import pytest


@pytest.fixture(autouse=True)
def empty_environ():
    """Each test starts from an empty environment, and what it sets goes with it."""
    saved = dict(os.environ)
    os.environ.clear()
    yield
    os.environ.clear()
    os.environ.update(saved)
