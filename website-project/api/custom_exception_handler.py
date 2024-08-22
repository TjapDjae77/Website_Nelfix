from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data['status'] = 'error'
#         response.data['message'] = str(response.data.get('detail', 'An error occurred'))
#         response.data['data'] = None

#         # Remove unnecessary fields
#         response.data.pop('detail', None)

#     else:
#         # In case of a more generic error (like 500 internal server error)
#         return Response({
#             'status': 'error',
#             'message': 'An unexpected error occurred.',
#             'data': None
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = {
            'status': 'error',
            'message': response.data.get('detail', 'An error occurred'),
            'data': None
        }
    else:
        # In case of a more generic error (like 500 internal server error)
        return Response({
            'status': 'error',
            'message': 'An unexpected error occurred.',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
