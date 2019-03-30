"""
包含一些异常类型等
"""


class RestError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

        super(RestError, self).__init__()


class AuthenticationError(RestError):
    pass


class InvalidTokenError(RestError):
    pass
