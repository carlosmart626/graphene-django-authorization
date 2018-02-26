""""
Auth utils module.

Define some functios to authorize user to user mutations or nodes.
"""


def is_related_to_user(object_instance, user, field):
    """Return True when the object_instance is related to user."""
    user_instance = getattr(object_instance, field, None)
    if user:
        if user_instance == user:
            return True
    return False


def is_unauthorized_to_mutate_object(model, id, user, field):
    """Return True when the when the user is unauthorized."""
    object_instance = model.objects.get(id=id)
    if is_related_to_user(object_instance, user, field):
        return False
    return True


def has_perm(permissions, context):
    """
    Validates if the user in the context has the permission required.
    """
    if context is None:
        return False
    if type(context) is dict:
        user = context.get('user', None)
        if user is None:
            return False
    else:
        user = context.user
        if user.is_authenticated() is False:
            return False

    if type(permissions) is tuple:
        print("permissions", permissions)
        for permission in permissions:
            print("User has perm", user.has_perm(permission))
            if not user.has_perm(permission):
                return False
    if type(permissions) is str:
        if not user.has_perm(permissions):
            return False
    return True
