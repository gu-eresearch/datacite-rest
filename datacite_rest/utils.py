from humps import camelize


def to_camel(value: str) -> str:
    try:
        return camelize(value)
    except Exception as e:
        raise Exception(e)
