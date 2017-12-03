from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        request = context.get('request')
        view = context.get('view')
        model_name = view.get_model_name()
        error_response = response.data
        response.data = {}
        errors = []
        response.data[model_name] = request.data
        for field, value in error_response.items():
            errors.append('{}:{}'.format(field, ''.join(value)))
        response.data['code'] = response.status_code
        response.data['msg'] = errors

    return response
