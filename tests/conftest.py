import pytest

from france_connect.clients import FranceConnect
from france_connect.enums import Scopes

TEST_CLIENT_ID = "0fe88d0ab61bbd95e6f8e718d7e4fadb0c721c2ab0f520a506a519643d8f6826"
TEST_CLIENT_SECRET = "6a4f704f8241232902b236a9dd06cf2d68c7f9ce40a297a41854615e2b2bc39d"
TEST_CLIENT_SCOPES = [Scopes.OPEN_ID, Scopes.PROFILE]
TEST_CLIENT_LOGIN_CALLBACK_URL = "http://localhost:8080/login"
TEST_CLIENT_LOGOUT_CALLBACK_URL = "http://localhost:8080/callback"
TEST_CLIENT_FC_BASE_URL = "https://fcp-low.integ01.dev-franceconnect.fr"


@pytest.fixture
def france_connect_client():
    """Create a FranceConnect client for testing."""
    return FranceConnect(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        scopes=TEST_CLIENT_SCOPES,
        login_callback_url=TEST_CLIENT_LOGIN_CALLBACK_URL,
        logout_callback_url=TEST_CLIENT_LOGOUT_CALLBACK_URL,
        fc_base_url=TEST_CLIENT_FC_BASE_URL,
    )
