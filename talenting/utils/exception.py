from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
   response = exception_handler(exc, context)
   if response is not None:
       status_code = response.status_code
       errors = [error for error in response.data.values()]
       if type(errors[0]) == list:
           error = errors[0][0]
       else:
           error = errors[0]
       response.data = {
           'code': status_code,
           'msg': error
       }
   return response