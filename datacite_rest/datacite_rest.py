from typing import Optional, Union, List, Dict
import logging

import requests

from .authentication import RespositoryAuth

log = logging.getLogger(__name__)


class DataCiteREST:
    _auth = None
    _base_path = 'dois'

    def __init__(
        self,
        id_: Optional[str] = None,
        password: Optional[str] = None,
        url: Optional[str] = None,
        prefix: Optional[str] = None
    ):
        """ pass through kwargs for RespositoryAuth"""
        self._auth = RespositoryAuth(id_, password, url, prefix)

    def request(
        self,
        url_path: str,
        method: str = 'GET',
        params: Optional[str] = None,
        json: Optional[Union[List, Dict]] = None,
        headers: Optional[Dict] = None,
    ) -> dict:
        """ proxy requests.request to add auth """
        url_base = self._auth.url.rstrip('/')  # support trailing slash
        try:
            res = requests.request(
                method=method,
                url=f'{url_base}/{url_path}',
                params=params,
                json=json,
                headers=headers,
                auth=requests.auth.HTTPBasicAuth(
                    self._auth.id,
                    self._auth.password
                )
            )
            res.raise_for_status()
            log.info(f'{self}.request - res.text: {res.text}')
            return res.json()
        except Exception as e:
            log.error(f'{self}.request - Exception: {e}')
            raise Exception(e)

    def list(self, query: Optional[str] = None) -> dict:
        """ https://support.datacite.org/docs/api-get-lists """
        url_path = f'{self._base_path}/'
        params = {}
        if query:
            params['query'] = query
        return self.request(url_path, params=params)

    def retrieve(self, doi: str) -> dict:
        """ https://support.datacite.org/docs/api-get-doi """
        url_path = f'{self._base_path}/{doi}'
        return self.request(url_path)
