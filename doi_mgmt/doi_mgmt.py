from .authentication import RespositoryAuth


class Doi:
    @staticmethod
    def get_auth():
        x = RespositoryAuth(id_=999)
        print(x.id)
