import jwt
import pytest

from france_connect.clients import FranceConnect
from france_connect.enums import Scopes


@pytest.fixture
def france_connect_client():
    """Create a FranceConnect client for testing."""
    return FranceConnect(
        client_id="0fe88d0ab61bbd95e6f8e7f8d7e4fadb0c721c2ab0f520a506a519643d8f6826",
        client_secret="6a4f704f8241232902b436a9dd06cf2d68c7f9ce40a297a41854615e2b2bc39d",
        scopes=[Scopes.OPEN_ID, Scopes.PROFILE],
        login_callback_url="http://localhost:8080/login",
        logout_callback_url="http://localhost:8080/callback",
    )
