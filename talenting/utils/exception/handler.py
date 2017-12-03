from inspect import isfunction
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    custom_view_exception_handlers = {
        'SignUp': signup_exception,
        'LogIn' : login_exception,
    }

    response = exception_handler(exc, context)
    if response is not None:
        view = context.get('view')
        view_name = str(view.__class__.__name__)

        status_code = response.status_code
        error_response = response.data

        if hasattr(view, 'get_fields_info') and isfunction(getattr(view, 'get_fields_info')):
            model_name, fields = view.get_fields_info()
            if view_name in custom_view_exception_handlers:
                response.data = custom_view_exception_handlers[view_name](fields, model_name, error_response, status_code)
            else:
                response.data = custom_exception_base(fields, model_name, error_response, status_code)
    return response


def custom_exception_base(fields, model_name, error_response, status_code):
    base_dict = dict()
    base_dict[model_name] = dict()
    fields_dict = dict()
    for field in fields:
        fields_dict[field] = None
    base_dict[model_name].update(fields_dict)
    errors = []
    for field, value in error_response.items():
        errors.append("{} : {}".format(field, " ".join(value)))

    base_dict['code'] = status_code
    base_dict['msg'] = errors
    return base_dict


def signup_exception(fields, model_name, error_response, status_code):
    base_dict = custom_exception_base(fields, model_name, error_response, status_code)
    del base_dict[model_name]['password1']
    del base_dict[model_name]['password2']
    return base_dict

def login_exception(fields, model_name, error_response, status_code):
    base_dict = {'token': None}
    base_dict.update(custom_exception_base(fields, model_name, error_response, status_code))
    del base_dict[model_name]['password']

    return base_dict
