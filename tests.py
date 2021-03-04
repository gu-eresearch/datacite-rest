import datetime
import unittest
import copy

from pydantic import BaseModel

from doi_mgmt import models


class JSONPayloadModel(unittest.TestCase):
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


class TestRespositoryAuthModel(unittest.TestCase):
    model = models.RespositoryAuthModel

    def _create_valid_base_model(self) -> model:
        data = {
            'id': 'abc123',
            'password': 'secret',
            'url': 'http://example.com',
            'prefix': 10.123
        }
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


class TestDataCiteModel(unittest.TestCase):
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
