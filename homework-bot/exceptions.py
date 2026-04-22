
class EmptyTokenError(Exception):
    """Исключение для обязательных токенов."""


class RequestApiError(Exception):
    """Исключение для API запроса."""


class ResponseApiError(Exception):
    """Исключение для API ответа."""