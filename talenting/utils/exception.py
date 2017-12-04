from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        status_code = response.status_code
        errors = [error for error in response.data.values()]
        response.data = {
            'code': status_code,
            'msg': errors[0]
        }
    return response
