import os
import logging
from typing import Optional

from .models import RespositoryAuthModel

log = logging.getLogger(__name__)


class RespositoryAuth:
    _auth = None
    _model = RespositoryAuthModel

    def __init__(
        self,
        id_: Optional[str] = None,
        password: Optional[str] = None,
        url: Optional[str] = None,
        prefix: Optional[str] = None
    ):
        """ bootstrap credentials from env vars if args not passed """
        if id_ is None:
            id_ = os.getenv('DOI_REPOSITORY_ID')
        if password is None:
            password = os.getenv('DOI_REPOSITORY_PASSWORD')
        if url is None:
            url = os.getenv('DOI_REPOSITORY_URL')
        if prefix is None:
            prefix = os.getenv('DOI_REPOSITORY_PREFIX')

        self._auth = self._model(
            id=id_,
            password=password,
            url=url,
            prefix=prefix
        )

    @property
    def id(self):
        return self._auth.id

    @property
    def password(self):
        return self._auth.password

    @property
    def url(self):
        return self._auth.url

    @property
    def prefix(self):
        return self._auth.prefix
