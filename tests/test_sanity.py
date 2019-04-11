from requests_html import HTMLSession


def test_sanity(app):
    """Check if the basic functionaity works correctly."""
    port, username, password = app
    session = HTMLSession()
    response = session.get('http://localhost:{}'.format(port))
    assert response.status_code == 200
