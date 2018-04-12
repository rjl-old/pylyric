import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

MAX_RETRIES = 3


class ApiError(Exception):
    def __init__(self, status_code, reason, url):
        self.status_code = status_code
        self.reason = reason
        self.url = url

    def __str__(self):
        return f'{self.status_code} {self.reason} - {self.url}'


def protector(func):
    """Decorator for LyricAPI methods"""

    def retried_func(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if resp.status_code != 200:
                raise ApiError(
                        resp.status_code,
                        resp.reason,
                        resp.url)
            return resp

        except Exception as x:
            print(f'{x.__class__.__name__}::honeywellAPI.{func.__name__}() [{x}]')
            raise

    return retried_func


def requests_retry_session(
        retries=MAX_RETRIES,
        backoff_factor=0.3,
        status_forcelist=(400, 403, 404, 500, 503),
        session=None
) -> requests.Session:
    """see: https://www.peterbe.com/plog/best-practice-with-retries-with-requests"""
    session = session or requests.Session()
    retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
