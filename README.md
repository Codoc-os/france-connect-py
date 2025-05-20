France Connect Py
=====================

[![PyPI Version](https://badge.fury.io/py/france-connect-py.svg)](https://badge.fury.io/py/france-connect-py)
![Tests](https://github.com/Codoc-os/france-connect-py/workflows/Tests/badge.svg)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)](#)
[![License MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/Codoc-os/france-connect-py/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Codoc-os/france-connect-py/branch/main/graph/badge.svg)](https://codecov.io/gh/Codoc-os/france-connect-py)
[![CodeFactor](https://www.codefactor.io/repository/github/Codoc-os/france-connect-py/badge)](https://www.codefactor.io/repository/github/Codoc-os/france-connect-py)

`france-connect-py` is a package allowing to interact with FranceConnect V2
through a single and easy-to-use class.

## Requirements

`france-connect-py` only support the supported version of each dependency (mainstream & lts).

* `Python` ([supported versions](https://devguide.python.org/versions/))

## Installation 

The easiest way to install `france-connect-py` is through `pip`:

* `pip install france-connect-py`

## How to use

You only need to import the `FranceConnect` class and create an instance to
start using the France Connect API.

```python
from france_connect.clients import FranceConnect
from france_connect.scopes import ACRValues, Scopes

fc = FranceConnect(
    client_id="<client_id>",
    client_secret="<client_secret>",
    scopes=[Scopes.PROFILE, Scopes.IDENTITE_PIVOT],
    # Must be THE SAME url as defined in FranceConnect
    # No additional query params
    # Do not forget the potential trailing slash
    login_callback_url="<login_callback_url>",
    logout_callback_url="<logout_callback_url>",
    fc_base_url="https://fcp-low.integ01.dev-franceconnect.fr",
)

# You can retrieve the FranceConnect's OpenID configuration as follow.
fc.get_configuration()

# Get the authorization URL.
#
# You can provide a specific `nonce` and `state` if needed, or let the class
# generate them as a random 64 bytes hex string. You can also inherit
# `FranceConnect` and override `generate_nonce()` and `generate_state()` to change
# the way they are generated.
# 
# `eidas1` is used as the default level of end user assurance, you can provide
# a different value using the `acr_values` parameter.
# For more information, see:
#   https://docs.partenaires.franceconnect.gouv.fr/fs/fs-technique/fs-technique-eidas-acr/
# 
# The `login_callback_url` provided at instantiation will be used as the
# callback URL, you can override it using the `callback_url` parameter.
url, nonce, state = fc.get_authentication_url(acr_values=[ACRValues.EIDAS2])


# The following code must be called when the user is redirected back to the
# service provider after a successful authentication of FranceConnect.
#
# Retrieve the code from the FranceConnect request
code = ...


# Retrieve the ID Token (the signature is verified automatically)
raw_token, decoded_token = fc.get_id_token(code)


# Retrieve the user's information using the ID Token (the signature is also
# verified automatically) `user_info` is a dictionary containing the user's
# information asked in the scopes.
user_info = fc.get_user_info(raw_token["access_token"])


# To retrieve the logout url, uses `get_logout_url()`.
#
# The `logout_callback_url` provided at instantiation will be used as the
# callback URL, you can override it using the `callback_url` parameter.
logout_url = fc.get_logout_url(raw_token["id_token"], state)
```

## Other

`france-connect-py` uses the `requests` library to interact with the France
Connect API. You can override how the library is used using the following
`FranceConnect` class parameters:

* `timeout: int = 10`
* `verify_ssl: bool = True`
* `allow_redirects: bool = True`
