from tests.run import run_app
import pytest
from requests_html import HTMLSession

@pytest.fixture
def app():
    app = run_app(wait_for_input=False)
    yield next(app)
    next(app)

def test_sanity(app):
    port, username, password = app
    session = HTMLSession()
    response = session.get('http://localhost:{}'.format(port))
    assert response.status_code == 200
