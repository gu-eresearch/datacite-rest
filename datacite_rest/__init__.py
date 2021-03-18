""" root module with metadata """
__title__ = 'datacite-rest'
__version__ = '0.0.1-dev0'
__author__ = 'Gary Burgmann'
__author_email__ = 'g.burgmann@griffith.edu.au'
__description__ = 'a package for managing dois'
__license__ = 'MIT'

try:
    from .datacite_rest import DataCiteREST  # noqa
except Exception:
    # preserve import here but stops setup.py breaking due to dependencies
    pass
