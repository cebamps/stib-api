from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


class ClientCredentialOAuth2Session(OAuth2Session):
    """OAuth2 client session with client credential grant renewal

    Subclass of requests_oauthlib.OAuth2Session for "client credential"
    grants that refreshes tokens automatically.

    See also
    https://github.com/requests/requests-oauthlib/issues/260
    """
    def __init__(self, *args, **kwargs):
        self.token_url = kwargs.pop('token_url', None)
        super().__init__(*args, **kwargs)
        assert isinstance(self._client, BackendApplicationClient)

    def request(self, *args, **kwargs):
        try:
            return super().request(*args, **kwargs)
        except TokenExpiredError:
            self.renew_token()
        return super().request(*args, **kwargs)

    def renew_token(self):
        self.fetch_token(token_url=self.token_url, **self.auto_refresh_kwargs)


class StibSession(ClientCredentialOAuth2Session):
    def __init__(self, base, client_id, client_secret):
        self.authenticated = False
        self.auth = HTTPBasicAuth(client_id, client_secret)
        oauth2_client = BackendApplicationClient(client_id)
        super().__init__(
            client=oauth2_client, token_url=base.rstrip('/')+'/token',
            auto_refresh_kwargs=dict(auth=self.auth)
        )

    def authenticate(self):
        if not self.authenticated:
            self.renew_token()
        self.authenticated = True
