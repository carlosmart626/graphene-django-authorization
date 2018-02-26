from django.core.exceptions import PermissionDenied
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.fields import DjangoConnectionField
from graphene_django import DjangoObjectType

from .utils import is_related_to_user, has_perm


class AuthDjangoFilterConnectionField(DjangoFilterConnectionField):
    """
    Django Filter Connection required a defined permission *_permission* this permission
    can be a *tuple* or a *str* to set a required or a set of required permissions.
    """
    _permissions = None

    def connection_resolver(self, resolver, connection, default_manager, max_limit,
                            enforce_first_or_last, filterset_class, filtering_args,
                            root, args, context, info):
        """
        Resolve the required connection if the user in context has the permission required. If the user
        does not have the required permission then returns a *Permission Denied* to the request.
        """
        assert self._permissions is not None
        if has_perm(self._permissions, context) is not True:
            print(DjangoConnectionField)
            return DjangoConnectionField.connection_resolver(
                resolver, connection, [PermissionDenied('Permission Denied'), ], max_limit,
                enforce_first_or_last, root, args, context, info)
        return super(AuthDjangoFilterConnectionField, self).connection_resolver(
            resolver, connection, default_manager, max_limit,
            enforce_first_or_last, filterset_class, filtering_args,
            root, args, context, info)


class AuthDjangoObjectType(DjangoObjectType):
    """
    Django Filter Connection required a defined permission *_permission* this permission
    can be a *tuple* or a *str* to set a required or a set of required permissions.
    """
    _permissions = None
    model = None
    related_field = None

    @classmethod
    def get_node(cls, id, context, info):
        assert cls._permissions is not None
        try:
            object_instance = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        user = context.user
        if cls.model or cls.related_field:
            assert cls.model is not None and cls.related_field is not None
            if is_related_to_user(object_instance, user):
                return object_instance
        if has_perm(cls._permissions, context):
            return object_instance
        return PermissionDenied('Permission Denied')
