from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, context: dict) -> Response:
    response = exception_handler(exc, context)

    if response is not None:
        response.data['code'] = response.status_code

    return response
