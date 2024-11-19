from email.policy import default
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status


class BadRequestException(APIException):
    status_code = 400
    default_detail = "درخواست ارسالی شما معتبر نیست"
    default_code = "bad_request"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response.data = {
                "success": False,
                "code_name": "invalid_input",
                "details": response.data,
            }
        elif isinstance(exc, BadRequestException):
            response.status_code = BadRequestException.status_code
            details = exc.detail

            response.data = {
                "success": False,
                "code_name": BadRequestException.default_code,
                "details": details or BadRequestException.default_detail,
            }
        else:
            response.data = {
                "success": False,
                "error": "خطایی رخ داد لطفا بعدا تلاش کنید",
                "details": response.data,
            }

    return response
