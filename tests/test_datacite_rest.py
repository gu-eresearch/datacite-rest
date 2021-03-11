from unittest import TestCase
import copy

from datacite_rest import DataCiteREST


class TestDataCiteREST(TestCase):
    """ must have valid env var set for endpoints """
    VALID_DRAFT = {
        'data': {
            'type': 'dois',
            'attributes': {
                'prefix': '10.17623'
            }
        }
    }
    VALID_PUBLISH = {
        'data': {
            'type': 'dois',
            'attributes': {
                'event': 'publish',
                'prefix': '10.17623',
                'creators': [
                    {
                        'name': 'Data CO-OP'
                    }
                ],
                'titles': [
                    {
                        'title': 'DataCite test'
                    }
                ],
                'types': {
                    'resourceTypeGeneral': 'Text'
                },
                'publisher': 'DataCite e.V.',
                'publicationYear': 2021,
                'url': 'https://datacoop.com.au/jedi'
            }
        }
    }

    def _validate_response_detail(self, res: dict) -> None:
        """ recycle across tests """
        self.assertTrue(type(res) == dict)
        self.assertTrue('data' in res, res)
        self.assertTrue(type(res['data']) == dict)
        self.assertTrue('id' in res['data'], res)
        id_data = res['data']['id'].split('/')
        self.assertTrue(len(id_data) == 2)

    def test_draft_create_fails(self):
        """ should fail without draft=True when missing required data """
        json_body = copy.deepcopy(self.VALID_DRAFT)
        x = DataCiteREST()
        with self.assertRaises(Exception):
            _ = x.create(json_body=json_body)

    def test_draft_create(self):
        json_body = copy.deepcopy(self.VALID_DRAFT)
        x = DataCiteREST()
        res = x.create(json_body=json_body, draft=True)
        self._validate_response_detail(res)
        self.assertEqual(
            res['data']['id'].split('/')[0],
            json_body['data']['attributes']['prefix']
        )

    def test_publish_create(self):
        json_body = copy.deepcopy(self.VALID_PUBLISH)
        x = DataCiteREST()
        res = x.create(json_body=json_body)
        self._validate_response_detail(res)
        self.assertEqual(
            res['data']['id'].split('/')[0],
            json_body['data']['attributes']['prefix']
        )

    def test_retrieve(self):
        json_body = copy.deepcopy(self.VALID_DRAFT)
        x = DataCiteREST()
        res = x.create(json_body=json_body, draft=True)
        self._validate_response_detail(res)
        res_detail = x.retrieve(doi=res['data']['id'])
        self._validate_response_detail(res_detail)
        self.assertEqual(
            res['data']['id'],
            res_detail['data']['id']
        )

    def test_update(self):
        json_body = copy.deepcopy(self.VALID_DRAFT)
        x = DataCiteREST()
        res = x.create(json_body=json_body, draft=True)
        self._validate_response_detail(res)

        test_key = 'publisher'
        test_value = 'foobar'

        self.assertEqual(
            res['data']['attributes'][test_key],
            None
        )

        json_body_update = copy.deepcopy(res)
        json_body_update['data']['attributes'][test_key] = test_value

        res_update = x.update(
            doi=res['data']['id'],
            json_body=json_body_update,
            partial=True
        )
        self._validate_response_detail(res_update)
        self.assertNotEqual(
            res_update['data']['attributes'][test_key],
            res['data']['attributes'][test_key]
        )
        self.assertEqual(
            res_update['data']['attributes'][test_key],
            test_value
        )
