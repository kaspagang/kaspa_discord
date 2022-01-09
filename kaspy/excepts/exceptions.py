class RPCResponseException(Exception):
    def __init__(self, code, details):
        super().__init__(f'{code}: {details}')