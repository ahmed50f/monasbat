from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid phone number or password."
    default_code = "invalid_credentials"


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this phone number already exists."
    default_code = "user_exists"
