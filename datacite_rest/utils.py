from humps import camelize


def to_camel(value: str) -> str:
    """
    abstracts pyhumps camelize()

    https://humps.readthedocs.io/en/latest/
    """
    try:
        return camelize(value)
    except Exception as e:
        raise Exception(e)


def to_kebab(value: str) -> str:
    """ snake_case to kebab-case """
    try:
        return value.replace('_', '-')
    except Exception as e:
        raise Exception(e)
