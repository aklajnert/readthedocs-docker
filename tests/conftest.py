import pytest

from .run import run_app


@pytest.fixture
def app(request):
    app = run_app(wait_for_input=False,
                  with_ldap=any(marker.name == 'with_ldap' for marker in request.node.own_markers))
    yield next(app)
    next(app, True)
