# france-connect-py

**france-connect-py** is a Python client for integrating with the [FranceConnect](https://franceconnect.gouv.fr) authentication system, allowing secure and efficient authentication for users of FranceConnect services.

## Requirements

* `python >= 3.9`
* `pip => 22.3.0`


## Installation

1. Clone the repository.

    ```shell
    git clone git@github.com:Codoc-os/france-connect-py.git
    ```

2. Create a python virtual environment (*venv*).

    ```shell
    python3 -m venv {env_name}
    ```

3. Activate the created *venv*:

    ```shell
    source {env_name}/bin/activate
    ```

4. Install python's requirements : `pip install -r requirements.txt`

## Usage

Install package : `pip install france_connect`

## Example

For more information on the FranceConnect API, see the [FranceConnect API documentation](https://docs.partenaires.franceconnect.gouv.fr/fs/).
    
```python
from france_connect import FranceConnect, Scopes, ACRValues

fc_client = FranceConnect(
        client_id='client-id',
        client_secret='client-secret',
        scopes=[Scopes.OPENID, Scopes.PROFILE],
        login_callback_url='https://your-app.com/callback',
        logout_callback_url='https://your-app.com/logout',
)
# Get authentication URL
auth_url, nonce, state = fc_client.get_authentication_url()
print(f"Navigate to: {auth_url}")

# After receiving the authorization code, exchange it for an access token, it verifies signature and returns decoded token
token_not_verified, decoded_token = fc_client.get_access_token('authorization-code')
print(token_not_verified)
print(decoded_token)

# Get user info
user_info = fc_client.get_user_info('access-token')

# Get logout URL
logout_url = fc_client.get_logout_url(id_token, state, url) # url default to logout_callback_url
print(f"Navigate to: {logout_url}")
```