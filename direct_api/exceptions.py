# API Error Codes
AUTHORIZATION_FAILED = 5  # Invalid access token
PERMISSION_IS_DENIED = 7
CAPTCHA_IS_NEEDED = 14
ACCESS_DENIED = 15  # No access to call this method
INVALID_USER_ID = 113  # User deactivated


class YdException(Exception):
    pass


class YdAuthError(YdException):
    pass


class YdAPIError(YdException):
    __slots__ = ['error', 'code', 'message', 'request_params', 'request_id']

    def __init__(self, error_data):
        super(YdAPIError, self).__init__()
        self.error_data = error_data
        self.code = error_data.get('error_code')
        self.message = error_data.get('error_string')
        self.description = error_data.get('error_detail')
        self.request_id = error_data.get('request_id')

    def __str__(self):
        return f'{self.code}. {self.message}. {self.description} request_id={self.request_id}'
