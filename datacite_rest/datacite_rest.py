from typing import Optional, Union, List, Dict
import logging

import requests

from .authentication import RespositoryAuth
from .models import Schema43Model, Schema43BaseModel
from .utils import to_kebab

log = logging.getLogger(__name__)


class DataCiteREST:
    _auth = None
    # https://support.datacite.org/docs/api-get-lists
    # #what-kinds-of-lists-can-i-ask-for
    _resources = [
        'clients',
        'dois',
        'events',
        'prefixes',
        'providers',
        'reports'
    ]
    _base_path = _resources[1]  # default dois

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
        params: Optional[Dict] = None,
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

    def _append_slash_to_path(self, url_path: str) -> str:
        """
        docs detail trailing slash for list/create endpoints, but not detail

        https://support.datacite.org/docs/api
        """
        return f"{url_path.rstrip('/')}/"

    def list(
        self,
        resource: Optional[str] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """ https://support.datacite.org/docs/api-get-lists """
        url_path = resource if resource else self._base_path
        assert url_path in self._resources, f'{self._resources}'
        assert type(params) == dict, type(params)
        # datacite expects kebab-case params
        params = {to_kebab(k): v for k, v in params.items()}
        return self.request(
            self._append_slash_to_path(url_path),
            params=params
        )

    def create(self, json_body: Dict, draft=False) -> Dict:
        """ https://support.datacite.org/docs/api-get-lists """
        url_path = self._append_slash_to_path(self._base_path)
        payload = None

        try:
            if draft is True:
                payload = Schema43BaseModel(**json_body)
            else:
                payload = Schema43Model(**json_body)
        except Exception as e:
            raise Exception(e)

        json_ = payload.dict()
        return self.request(url_path, method='POST', json=json_)

    def retrieve(self, doi: str) -> Dict:
        """ https://support.datacite.org/docs/api-get-doi """
        url_path = f'{self._base_path}/{doi}'
        return self.request(url_path)

    def update(self, doi: str, json_body: Dict, partial=True) -> Dict:
        """
        https://support.datacite.org/docs/updating-metadata-with-the-rest-api
        """
        url_path = f'{self._base_path}/{doi}'
        payload = None
        try:
            # TODO: find a better way to validate partial update data
            if partial is True:
                payload = Schema43BaseModel(**json_body)
            else:
                payload = Schema43Model(**json_body)
        except Exception as e:
            raise Exception(e)

        json_ = payload.dict()
        return self.request(url_path, method='PUT', json=json_)
