from typing import Optional, List, Any
import datetime

from pydantic import BaseModel, HttpUrl, condecimal, conint

from .utils import to_camel


class JSONPayloadModel(BaseModel):
    data: Any


class DataCiteBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class DataCiteIdentifierModel(DataCiteBaseModel):
    identifier: HttpUrl
    identifier_type: str


class DataCiteTitleModel(DataCiteBaseModel):
    title: str


class DataCiteCreatorModel(DataCiteBaseModel):
    name: Optional[str]
    name_type: Optional[str]


class DataCiteTypeModel(DataCiteBaseModel):
    resource_type: str
    resource_type_general: Optional[str]


class DataCiteAttributesModel(DataCiteBaseModel):
    doi = Optional[str]
    identifiers: Optional[List[DataCiteIdentifierModel]]
    creators: List[Optional[DataCiteCreatorModel]]
    titles: List[DataCiteTitleModel]
    publisher: str
    publication_year: conint(ge=2021, le=datetime.datetime.utcnow().year)
    types: DataCiteTypeModel
    prefix: condecimal(ge=10, lt=11)
    suffix: Optional[str]
    # TODO: add more optional properties


class DataCiteModel(DataCiteBaseModel):
    type: str
    attributes: DataCiteAttributesModel


class RespositoryAuthModel(DataCiteBaseModel):
    id: str
    password: str
    url: HttpUrl
    prefix: condecimal(ge=10, lt=11)
