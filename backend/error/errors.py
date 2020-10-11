class APIError(Exception):
    def __init__(self, message=None):
        super().__init__()

        self.message = self.default_message if message is None else message

    def to_dict(self):
        return {
            'code': self.status_code,
            'message': self.message
        }


class BadRequest(APIError):
    status_code = 400
    default_message = 'Bad Request'


class NotFound(APIError):
    status_code = 404
    default_message = 'Resource not found'


class InternalServerError(APIError):
    status_code = 500
    default_message = 'Internal Server Error'
