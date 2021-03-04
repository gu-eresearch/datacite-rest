import datetime
from unittest import TestCase, mock
import copy

from pydantic import BaseModel

from datacite_rest import models, authentication

VALID_AUTH = {
    'id': 'abc123',
    'password': 'secret',
    'url': 'http://example.com',
    'prefix': '10.123'
}


class JSONPayloadModel(TestCase):
    model = models.JSONPayloadModel

    def test_payload_list(self):
        _ = self.model(data=[1, 2, 3])

    def test_payload_dict(self):
        _ = self.model(data={'1': 2, '3': 4})

    def test_payload_model(self):
        class TestModel(BaseModel):
            x: str
        m = TestModel(x='test')
        _ = self.model(data=m)


class TestRespositoryAuthModel(TestCase):
    model = models.RespositoryAuthModel

    def _create_valid_base_model(self) -> model:
        data = VALID_AUTH
        return self.model(**data)

    def test_create_auth(self):
        _ = self._create_valid_base_model()

    def test_invalid_url(self):
        m1 = self._create_valid_base_model()
        data = m1.dict()
        data['url'] = 'test'
        with self.assertRaises(Exception):
            _ = self.model(**data)

    def test_invalid_prefix(self):
        m1 = self._create_valid_base_model()
        data = m1.dict()
        data['prefix'] = 'test'
        with self.assertRaises(Exception):
            _ = self.model(**data)


class TestDataCiteModel(TestCase):
    model = models.DataCiteModel

    def _create_valid_base_model(self) -> model:
        data = {
            'type': 'dois',
            'attributes': {
                'identifiers': [],
                'creators': [],
                'titles': [
                    {'title': 'test'}
                ],
                'publisher': 'test',
                'publication_year': datetime.datetime.utcnow().year,
                'types': {
                    'resource_type': 'Text'
                },
                'prefix': 10.111
            }
        }
        return self.model(**data)

    def test_create_doi(self):
        """
        https://support.datacite.org/docs/schema-properties-overview-v43
        #table-1-datacite-mandatory-properties
        """
        _ = self._create_valid_base_model()

    def test_create_doi_with_creators(self):
        """
        https://support.datacite.org/docs/schema-properties-overview-v43
        #table-1-datacite-mandatory-properties
        """
        m1 = self._create_valid_base_model()
        self.assertFalse(getattr(m1, 'creators', False))

        data = copy.deepcopy(m1.dict())
        data['attributes']['creators'] = [{'name': 'test'}]

        m2 = self.model(**data)

        self.assertTrue(m2.attributes.creators[0].name)
        self.assertEqual(
            m2.attributes.creators[0].name,
            data['attributes']['creators'][0]['name']
        )


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
        with self.assertRaises(Exception):
            x = self.obj()
            self._get_obj_properties(x)
