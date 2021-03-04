import os
import logging

from .models import RespositoryAuthModel

log = logging.getLogger(__name__)


class RespositoryAuth:
    _auth = None
    _model = RespositoryAuthModel
    """ bootstrap credentials from env vars """
    def __init__(
        self,
        id_=os.getenv('DOI_REPOSITORY_ID'),
        password=os.getenv('DOI_REPOSITORY_PASSWORD'),
        url=os.getenv('DOI_REPOSITORY_URL'),
        prefix=os.getenv('DOI_REPOSITORY_PREFIX')
    ):
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
