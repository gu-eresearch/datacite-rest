from unittest import TestCase, mock
import copy

from datacite_rest import authentication
from .shared import VALID_AUTH


class TestRespositoryAuth(TestCase):
    obj = authentication.RespositoryAuth

    def _get_obj_properties(self, obj: authentication.RespositoryAuth):
        _ = obj.id
        _ = obj.password
        _ = obj.url
        _ = obj.prefix

    def test_create_obj_from_args(self):
        args = copy.deepcopy(VALID_AUTH)
        args['id_'] = args.pop('id')
        x = self.obj(**args)
        self._get_obj_properties(x)

    def test_create_obj_from_env_defaults(self):
        env = {}
        env['DOI_REPOSITORY_ID'] = VALID_AUTH['id']
        env['DOI_REPOSITORY_PASSWORD'] = VALID_AUTH['password']
        env['DOI_REPOSITORY_URL'] = VALID_AUTH['url']
        env['DOI_REPOSITORY_PREFIX'] = VALID_AUTH['prefix']

        with mock.patch.dict('os.environ', env):
            x = self.obj()
            self._get_obj_properties(x)

    def test_create_obj_without_env_or_args_fails(self):
        with mock.patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(Exception):
                x = self.obj()
                self._get_obj_properties(x)
