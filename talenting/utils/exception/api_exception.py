from rest_framework import status
from rest_framework.exceptions import APIException


class LogInException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RegistrationIdNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
