import datetime
import os

# default from docs: https://support.datacite.org/docs/api-create-dois
PREFIX = os.getenv('DATACITE_REPOSITORY_PREFIX', '10.5438')
DOMAINS = [
    x for x
    in os.getenv('DATACITE_REPOSITORY_DOMAINS', '').split(',')
    if x  # weed out empty value
]
# TODO: handle wildcards later(?)
DOMAIN = f"https://{next((x for x in DOMAINS if x[0] != '*'), 'example.com')}"
NOW = datetime.datetime.utcnow()

VALID_AUTH_FMT = {
    'id': 'abc123',
    'password': 'secret',
    'url': f'{DOMAIN}/test',
    'prefix': PREFIX
}

VALID_DRAFT_FMT = {
    'data': {
        'type': 'dois',
        'attributes': {
            'prefix': PREFIX
        }
    }
}

VALID_DOI_FMT = {
    'data': {
        'type': 'dois',
        'attributes': {
            'identifiers': [],
            'creators': [{}],
            'titles': [
                {'title': 'test'}
            ],
            'publisher': 'test',
            'publication_year': NOW.year,
            'types': {
                'resource_type_general': 'Text'
            },
            'prefix': PREFIX,
            'url': f'{DOMAIN}/test'
        }
    }
}
