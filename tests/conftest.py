import pytest

from .run import run_app


@pytest.fixture
def app():
    app = run_app(wait_for_input=False)
    yield next(app)
    next(app, True)
