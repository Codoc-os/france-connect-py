import datetime
import secrets
import urllib.parse
from unittest.mock import MagicMock, patch

import jwt
import pytest

from .fixtures import france_connect_client


def test_get_access_token_and_verify(france_connect_client):
    mock_code = secrets.token_urlsafe(8)
    access_token = secrets.token_urlsafe(32)
    id_token = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    # Decoded token expected (real answer from FranceConnectAPI)
    decoded_token_expected = {
        "sub": "sub",
        "auth_time": 1727813371,
        "acr": "eidas1",
        "nonce": nonce,
        "at_hash": "at_hash",
        "aud": "aud",
        "exp": 1727813431,
        "iat": 1727813371,
        "iss": "https://fcp-low.integ01.dev-franceconnect.fr/api/v2",
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "access_token": access_token,
            "id_token": id_token,
            "expires_in": 3600,
            "token_type": "Bearer",
        }
        mock_post.return_value.status_code = 200

        # Mocking the JWK client to return a valid signing key
        # needed to avoid the signature verification error
        with patch("france_connect.clients.PyJWKClient") as mock_jwks_client:
            mock_jwks_client.return_value.get_signing_key_from_jwt.return_value = MagicMock(key="public_key")

            # jwt.decode mocked for decoding the id_token
            with patch("france_connect.clients.jwt.decode") as mock_decode:
                mock_decode.return_value = decoded_token_expected

                token, decoded_token = france_connect_client.get_access_token(mock_code)

    assert token["access_token"] == access_token
    assert token["id_token"] == id_token

    assert decoded_token["sub"] == decoded_token_expected["sub"]
    assert decoded_token["nonce"] == decoded_token_expected["nonce"]
    assert decoded_token["acr"] == decoded_token_expected["acr"]
    assert decoded_token["iss"] == decoded_token_expected["iss"]


def test_get_user_info_and_verify(france_connect_client):
    # Simulates a real encoded user info response
    encoded_user_info = jwt.encode(
        {
            "sub": "1234567890",
            "given_name": "Angela",
            "family_name": "Doe",
            "birthdate": "1990-01-01",
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
        },
        "secret",
        algorithm="HS256",
        headers={"kid": "kid_key"},
    )

    access_token = "dummy_access_token"

    decoded_user_info_expected = {
        "sub": "1234567890",
        "given_name": "Angela",
        "family_name": "Doe",
        "birthdate": "1990-01-01",
    }

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = encoded_user_info.encode("utf-8")
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("france_connect.clients.PyJWKClient") as mock_jwks_client:
            mock_jwks_client.return_value.get_signing_key_from_jwt.return_value = MagicMock(key="mock_signing_key")

            with patch("france_connect.clients.jwt.decode") as mock_user_info_decode:
                mock_user_info_decode.return_value = decoded_user_info_expected

                user_info = france_connect_client.get_user_info(access_token)

    assert user_info["sub"] == decoded_user_info_expected["sub"]
    assert user_info["given_name"] == decoded_user_info_expected["given_name"]
    assert user_info["family_name"] == decoded_user_info_expected["family_name"]
    assert user_info["birthdate"] == decoded_user_info_expected["birthdate"]


def test_logout_url(france_connect_client):
    id_token = "dummy_id_token"
    state = "dummy_state"
    logout_url = france_connect_client.get_logout_url(id_token, state, "http://localhost:8080/contact")
    decoded_logout_url = urllib.parse.unquote(logout_url)
    expected_url = (
        "https://fcp-low.integ01.dev-franceconnect.fr/api/v2/session/end"
        "?id_token_hint=dummy_id_token"
        "&state=dummy_state"
        "&post_logout_redirect_uri=http://localhost:8080/contact"
    )
    assert decoded_logout_url == expected_url

    logout_url = france_connect_client.get_logout_url(id_token, state)
    decoded_logout_url = urllib.parse.unquote(logout_url)
    expected_url = (
        "https://fcp-low.integ01.dev-franceconnect.fr/api/v2/session/end"
        "?id_token_hint=dummy_id_token"
        "&state=dummy_state"
        f"&post_logout_redirect_uri={france_connect_client.logout_callback_url}"
    )

    assert decoded_logout_url == expected_url
