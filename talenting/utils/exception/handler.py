from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        status_code = response.status_code
        for error, error_message in response.data.items():
            break
        if type(error_message) == list:
            error = f'{error[0]}: {error_message[0]}'
        else:
            error = error_message
        response.data = {
            'code': status_code,
            'msg': error
        }
    return response
