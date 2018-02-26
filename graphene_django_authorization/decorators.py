from functools import wraps
from django.core.exceptions import PermissionDenied

from .utils import has_perm, is_unauthorized_to_mutate_object


def require_permission(permissions, model=None, id_field=None, user_field=None):
    def require_permission_decorator(func):
        @wraps(func)
        def func_wrapper(cls, root, input, context, info):
            if model or id_field or user_field:
                assert model is not None and id_field is not None and user_field is not None
                return is_unauthorized_to_mutate_object()
            if has_perm(permissions=permissions, context=context):
                return func(cls, root, input, context, info)
            return PermissionDenied('Permission Denied')
        return func_wrapper
    return require_permission_decorator
