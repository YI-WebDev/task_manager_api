import os
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response

UNAUTHORIZED_ERROR_CODE = 401001
FORBIDDEN_ERROR_CODE = 403001
NOT_FOUND_ERROR_CODE = 404001
UNKNOWN_ERROR_CODE = 500001

UNAUTHORIZED_ERROR_DETAIL = _('認証に失敗しました。')
FORBIDDEN_ERROR_DETAIL = _('アクセス権限がありません。')
NOT_FOUND_ERROR_DETAIL = _('リソースが見つかりません。')
UNKNOWN_ERROR_DETAIL = _('不明なエラーが発生しました。')

class TaskManagerException(APIException):
    """
    Generic exception class
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('エラーが発生しました')
    default_code = 400000

    def __init__(self, detail=None, code=None, **kwargs):
        lang = os.getenv('LANG', 'en')
        if detail is None:
            detail = self.default_detail if lang == 'ja' else super().default_detail
        detail = detail.format(**kwargs)
        super().__init__(detail=detail, code=code or self.default_code)

def custom_exception_handler(exception, context):
    """
    Custom Exception Handler
    """
    response = exception_handler(exception, context)

    if response is not None:
        if isinstance(exception, TaskManagerException):
            response.data['code'] = exception.default_code
        else:
            status_code = response.status_code
            if status_code == 401:
                response.data['code'] = UNAUTHORIZED_ERROR_CODE
                response.data['detail'] = UNAUTHORIZED_ERROR_DETAIL
            elif status_code == 403:
                response.data['code'] = FORBIDDEN_ERROR_CODE
                response.data['detail'] = FORBIDDEN_ERROR_DETAIL
            elif status_code == 404:
                response.data['code'] = NOT_FOUND_ERROR_CODE
                response.data['detail'] = NOT_FOUND_ERROR_DETAIL
            else:
                response.data['code'] = UNKNOWN_ERROR_CODE
                response.data['detail'] = UNKNOWN_ERROR_DETAIL
    else:
        response = Response({
            'code': UNKNOWN_ERROR_CODE,
            'detail': UNKNOWN_ERROR_DETAIL
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
