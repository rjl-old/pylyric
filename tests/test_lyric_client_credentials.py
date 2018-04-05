from unittest import TestCase

from pylyric.oauth2 import ApiCredentials
import server.config as cfg


class CredentialsTest(TestCase):
    """
    A series of tests to evaluate the behaviour of
    the client credentials class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Run once to set up the client credentials.
        """
        cls.lcc = ApiCredentials(
            client_id=cfg.CLIENT_ID,
            client_secret=cfg.CLIENT_SECRET,
            access_token=cfg.ACCESS_TOKEN,
            refresh_token=cfg.REFRESH_TOKEN
        )

    def test_refresh_token(self):
        """
        Tests the refresh token function to make sure
        a new api key is given from the server.
        """
        token = self.lcc.access_token
        self.lcc._refresh_token()
        self.assertNotEqual(self.lcc.access_token, token)
