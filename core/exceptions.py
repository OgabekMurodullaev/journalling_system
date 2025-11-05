from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        message = "Xatolik yuz berdi",
        errors = response.data

        if isinstance(errors, dict):
            if 'detail' in errors:
                message = errors['detail']
            elif 'non_field_errors' in errors:
                message = errors['non_field_errors'][0]

        return Response(
            {
                "success": False,
                "message": str(message),
                "errors": errors
            }, status=response.status_code
        )

    return Response(
            {
            "success": False,
            "message": str(exc),
            "errors": {}
        }, status=500
    )
