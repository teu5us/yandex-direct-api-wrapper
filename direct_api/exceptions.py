class YdException(Exception):
    pass


class YdAuthError(YdException):
    pass


class YdUnknownError(YdException):
    pass


class YdAPITimeOutException(YdException):

    def __init__(self, retry_in, scores) -> None:
        super().__init__()
        self.retry_in = retry_in
        self.scores = scores


class YdAPIError(YdException):
    __slots__ = ('error', 'code', 'message', 'request_params', 'request_id')

    def __init__(self, error, scores):
        super().__init__()
        self.error = error
        self.scores = scores
        self.code = error.get('error_code')
        self.message = error.get('error_string')
        self.description = error.get('error_detail')
        self.request_id = error.get('request_id')

    def __str__(self):
        return f'{self.code}. {self.message}. {self.description} request_id={self.request_id}'


class ParameterError(YdException):

    def __init__(self, params: list) -> None:
        super().__init__(params)
        self.params = params

    def __str__(self) -> str:
        return f'Must be implemented one of {self.params}'
