import secrets
import urllib.parse
from typing import Any, List, Tuple

import jwt
import requests
from jwt import PyJWKClient

from .enums import ACRValues, Scopes


class FranceConnect:
    """Client allowing interaction with the FranceConnect API.

    Provides methods for authentication, token exchange, and user information
    retrieval.

    Attibutes
    ---------
    client_id: str
        The client ID for the FranceConnect application.
    client_secret: str
        The client secret for the FranceConnect application.
    scopes: List[Scopes]
        The list of scopes to request during authentication.
    login_callback_url: str
        The URL to redirect to after successful login.
    logout_callback_url: str
        The URL to redirect to after logout.
    fc_base_url: str
        The base URL of the FranceConnect API.
    fc_authorization_url: str, optional
        The authorization URL of the FranceConnect API.
    fc_token_url: str, optional
        The token URL of the FranceConnect API.
    fc_jwks_url: str, optional
        The JWKS URL of the FranceConnect API.
    fc_userinfo_url: str, optional
        The userinfo URL of the FranceConnect API.
    fc_logout_url: str, optional
        The logout URL of the FranceConnect API.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scopes: List[Scopes],
        login_callback_url: str,
        logout_callback_url: str,
        fc_base_url: str,
        fc_authorization_url: str = "/api/v2/authorize",
        fc_token_url: str = "/api/v2/token",
        fc_jwks_url: str = "/api/v2/jwks",
        fc_userinfo_url: str = "/api/v2/userinfo",
        fc_logout_url: str = "/api/v2/session/end",
        timeout: int = 10,
        verify_ssl: bool = True,
        allow_redirects: bool = True,
        jwt_algorithms: List[str] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.login_callback_url = login_callback_url
        self.logout_callback_url = logout_callback_url
        self.fc_base_url = fc_base_url
        self.fc_authorization_url = fc_authorization_url
        self.fc_token_url = fc_token_url
        self.fc_jwks_url = fc_jwks_url
        self.fc_userinfo_url = fc_userinfo_url
        self.fc_logout_url = fc_logout_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.allow_redirects = allow_redirects
        self.jwt_algorithms = jwt_algorithms or ["RS256", "ES256"]

    @staticmethod
    def generate_nonce() -> str:
        """Generate a random nonce in hexadecimal string (64 characters)."""
        return secrets.token_hex(64)

    @staticmethod
    def generate_state() -> str:
        """Generate a random state in hexadecimal string (64 characters)."""
        return secrets.token_hex(64)

    def get_authentication_url(
        self, acr_values: List[ACRValues] = None, nonce: str = None, state: str = None, callback_url: str = None
    ) -> Tuple[str, str, str]:
        """Return the authentication URL, nonce, and state.

        Parameters
        ----------
        acr_values: List[ACRValues], optional
            The list of ACR values used for the authentication process, defaults
            to `[ACRValues.EIDAS1]`.
        nonce: str, optional
            The `nonce` used for the authentication process, generated using
            `generate_nonce()` if not provided.
        state: str, optional
            The `state` used for the authentication process, generated using
            `generate_state()` if not provided.
        callback_url: str, optional
            The callback URL used by FranceConnect after successful
            authentication, defaults to `self.login_callback_url`.

        Returns
        -------
        Tuple[str, str, str]
            The authentication URL, `nonce` and `state`.
        """
        acr_values = acr_values or [ACRValues.EIDAS1]
        nonce = nonce or self.generate_nonce()
        state = state or self.generate_state()
        redirect_url = callback_url or self.login_callback_url
        params = urllib.parse.urlencode(
            {
                "client_id": self.client_id,
                "response_type": "code",
                "scope": " ".join(self.scopes),
                "acr_values": " ".join(acr_values),
                "nonce": nonce,
                "state": state,
                "redirect_uri": redirect_url,
            }
        )
        url = urllib.parse.urljoin(self.fc_base_url, self.fc_authorization_url)
        return f"{url}?{params}", nonce, state

    def get_configuration(self) -> dict:
        """Return the OpenID configuration."""
        url = urllib.parse.urljoin(self.fc_base_url, "/api/v2/.well-known/openid-configuration")
        response = requests.get(url, timeout=self.timeout, verify=self.verify_ssl, allow_redirects=self.allow_redirects)
        response.raise_for_status()
        return response.json()

    def verify_jwt(self, token: str) -> dict:
        """Verify and decode the give token."""
        jwks_client = PyJWKClient(urllib.parse.urljoin(self.fc_base_url, self.fc_jwks_url))
        # Get the signing key from the JWT
        key = jwks_client.get_signing_key_from_jwt(token)
        # Decode and verify the JWT with the signing key
        return jwt.decode(token, key.key, algorithms=self.jwt_algorithms, audience=self.client_id)

    def get_id_token(self, code: str) -> Tuple[dict, dict]:
        """Exchange the authorization code for an ID Token.

        Parameters
        ----------
        code: str
            The authorization code received after successful authentication.

        Returns
        -------
        Tuple[dict, dict]
            The raw token and verified token.
        """
        token_url = urllib.parse.urljoin(self.fc_base_url, self.fc_token_url)
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.login_callback_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(
            token_url,
            data=data,
            headers={"Accept": "application/json"},
            timeout=self.timeout,
            verify=self.verify_ssl,
            allow_redirects=self.allow_redirects,
        )
        response.raise_for_status()
        token = response.json()
        return token, self.verify_jwt(token.get("id_token"))

    def get_user_info(self, token: str) -> dict:
        """Retrieve user information using `token`."""
        url = urllib.parse.urljoin(self.fc_base_url, self.fc_userinfo_url)
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(
            url, headers=headers, timeout=self.timeout, verify=self.verify_ssl, allow_redirects=self.allow_redirects
        )
        response.raise_for_status()
        return self.verify_jwt(response.content.decode("utf-8"))

    def get_logout_url(self, id_token: str, state: str, callback_url: str = None) -> str:
        """Compute the logout URL for FranceConnect.

        Parameters
        ----------
        id_token: str
            The id token to use for the logout.
        state: str
            The state to use for the logout.
        callback_url: str, optional
            The callback URL used by FranceConnect after successful
            logout, defaults to `self.logout_callback_url`.
        """
        logout_url = callback_url or self.logout_callback_url

        parameters = urllib.parse.urlencode(
            {"id_token_hint": id_token, "state": state, "post_logout_redirect_uri": logout_url}
        )
        return f"{urllib.parse.urljoin(self.fc_base_url, self.fc_logout_url)}?{parameters}"
