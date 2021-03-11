from unittest import TestCase
import copy

from datacite_rest import DataCiteREST

from .constants import VALID_DRAFT_FMT, VALID_DOI_FMT


class TestDataCiteREST(TestCase):
    """ must have valid env var set for endpoints """
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
        json_body = copy.deepcopy(VALID_DRAFT_FMT)
        x = DataCiteREST()
        with self.assertRaises(Exception):
            _ = x.create(json_body=json_body)

    def test_draft_create(self):
        json_body = copy.deepcopy(VALID_DRAFT_FMT)
        x = DataCiteREST()
        res = x.create(json_body=json_body, draft=True)
        self._validate_response_detail(res)
        self.assertEqual(
            res['data']['id'].split('/')[0],
            json_body['data']['attributes']['prefix']
        )

    def test_publish_create(self):
        json_body = copy.deepcopy(VALID_DOI_FMT)
        json_body['data']['attributes']['event'] = 'publish'
        x = DataCiteREST()
        res = x.create(json_body=json_body)
        self._validate_response_detail(res)
        self.assertEqual(
            res['data']['id'].split('/')[0],
            json_body['data']['attributes']['prefix']
        )

    def test_retrieve(self):
        json_body = copy.deepcopy(VALID_DRAFT_FMT)
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
        json_body = copy.deepcopy(VALID_DRAFT_FMT)
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
