from typing import Optional, List
import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    HttpUrl,
    condecimal,
    conint,
    validator
    # root_validator
)

from .utils import to_camel


class PrefixValidationModel(BaseModel):
    """ prefix should be deciaml, but stored as string """
    prefix: condecimal(ge=10, lt=11)


class BasePrefixModel(BaseModel):
    prefix: str

    @validator('prefix', check_fields=False, allow_reuse=True)
    def prefix_should_be_decimal(cls, v):
        try:
            _ = PrefixValidationModel(prefix=v)
        except Exception as e:
            raise ValueError(e)
        return v


class EventEnum(str, Enum):
    """
    Can be set to trigger a DOI state change.

    Possible actions:

    publish - Triggers a state move from draft or registered to findable
    register - Triggers a state move from draft to registered
    hide - Triggers a state move from findable to registered
    """
    publish = 'publish'
    register = 'register'
    hide = 'hide'


class ResourceTypeGeneralEnum(str, Enum):
    Audiovisual = 'Audiovisual'
    Collection = 'Collection'
    DataPaper = 'DataPaper'
    Dataset = 'Dataset'
    Event = 'Event'
    Image = 'Image'
    InteractiveResource = 'InteractiveResource'
    Model = 'Model'
    PhysicalObject = 'PhysicalObject'
    Service = 'Service'
    Software = 'Software'
    Sound = 'Sound'
    Text = 'Text'
    Workflow = 'Workflow'
    Other = 'Other'


class DataCiteBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True


class DataCiteIdentifierModel(DataCiteBaseModel):
    identifier: HttpUrl
    identifier_type: str


class DataCiteTitleModel(DataCiteBaseModel):
    title: str
    title_type: Optional[str]
    lang: Optional[str]


class DataCiteNameIdentifierModel(DataCiteBaseModel):
    name_identifier: Optional[str]
    name_identifier_scheme: Optional[str]
    scheme_uri: Optional[HttpUrl]


class DataCiteCreatorModel(DataCiteBaseModel):
    name: Optional[str]
    name_type: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    affiliation: Optional[str]
    name_identifiers: Optional[DataCiteNameIdentifierModel]


class DataCiteTypeModel(DataCiteBaseModel):
    resource_type: Optional[str]
    resource_type_general: ResourceTypeGeneralEnum


class DataCiteAttributesBaseModel(DataCiteBaseModel, BasePrefixModel):
    """
    this base class can be used for minting "state": "draft" dois.
    https://support.datacite.org/docs/api-create-dois#create-a-draft-doi
    """
    pass

    class Config(DataCiteBaseModel.Config):
        extra = 'allow'


class DataCiteRequiredAttributesModel(DataCiteAttributesBaseModel):
    """
    https://support.datacite.org/docs/api-create-dois#create-a-findable-doi
    https://support.datacite.org/docs/schema-mandatory-properties-v43#
    https://support.datacite.org/docs/schema-properties-overview-v43
    """
    doi: Optional[str]  # on condition that prefix exists
    identifiers: List[DataCiteIdentifierModel]
    creators: List[DataCiteCreatorModel]
    titles: List[DataCiteTitleModel]
    publisher: str
    publication_year: conint(ge=2021, le=datetime.datetime.utcnow().year + 1)
    types: DataCiteTypeModel
    url: HttpUrl

    @validator('doi', check_fields=False, allow_reuse=True)
    def doi_should_contain_slash(cls, v, values, **kwargs):
        if not v and 'prefix' not in values:
            raise ValueError(
                f"datacite should contain 'prefix' or 'doi': {values}"
            )
        elif v is not None:
            if '/' not in v or len(v.split('/')) != 2:
                raise ValueError(f'doi should contain a single "/": {v}')
            return v.strip()

        return v

    @validator('url', check_fields=False, allow_reuse=True)
    def url_to_string(cls, v, values, **kwargs):
        """ cast to str instead of HttpUrl model instance """
        return str(v)


class DataCiteAttributesModel(DataCiteRequiredAttributesModel):
    """
    https://support.datacite.org/docs/schema-optional-properties-v43
    https://support.datacite.org/docs/schema-properties-overview-v43
    """
    suffix: Optional[str]
    event: Optional[EventEnum]
    # TODO: add more optional properties


class DataCiteDraftModel(DataCiteBaseModel):
    id: Optional[str]
    type: str
    attributes: DataCiteAttributesBaseModel


class DataCiteModel(DataCiteDraftModel):
    attributes: DataCiteAttributesModel


class RespositoryAuthModel(DataCiteBaseModel, BasePrefixModel):
    id: str
    password: str
    url: HttpUrl
    # prefix: condecimal(ge=10, lt=11)


class JSONPayloadBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class JSONPayloadDraftModel(JSONPayloadBaseModel):
    """ for minting draft dois """
    data: DataCiteDraftModel

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class JSONPayloadModel(JSONPayloadDraftModel):
    """ for passing full models """
    data: DataCiteModel


class Schema43BaseModel(JSONPayloadDraftModel):
    """
    https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf
    """
    pass


class Schema43Model(JSONPayloadModel):
    """
    https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf
    """
    pass


# class DataCiteQueryParamsModel(BaseModel):
#     query = Optional[str]
#     created = Optional[float]
#     registered = Optional[float]
#     provider_id = Optional[str]
#     client_id = Optional[str]
#     person_id = Optional[str]
#     resource_type_id = Optional[str]
#     subject = Optional[str]
#     schema_version = Optional[str]
#     random = Optional[bool]
#     sample_size = Optional[float]
#     sample_group = Optional[str]
#     page[number] = Optional[float]
#     page[size] = Optional[float]
#     page[cursor] = Optional[float]
#     include = Optional[str]
#     sort = Optional[str]

#     class Config:
#         alias_generator = to_kebab
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
