from requests_html import HTMLSession

DESIRED_RTD_VERSION = '3.4.1'

def test_sanity(app):
    """Check if the basic functionaity works correctly."""
    port, username, password = app
    session = HTMLSession()
    response = session.get('http://localhost:{}'.format(port))

    assert len(response.html.find('a', containing=DESIRED_RTD_VERSION)) == 1

    login_link = response.html.find('a', containing='Log in')
    response.get(login_link)

    assert response.status_code == 200
