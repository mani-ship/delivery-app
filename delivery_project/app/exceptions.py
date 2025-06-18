from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, TokenError) or isinstance(exc, InvalidToken):
        if response is not None:
            # Overriding the default detail structure
            response.data = {'message': 'Token is expired'}

    elif isinstance(exc, NotAuthenticated):
        if response is not None:
            response.data = {'message': 'Authentication credentials were not provided'}

    elif isinstance(exc, AuthenticationFailed):
        if response is not None:
            response.data = {'message': str(exc)}

    return response