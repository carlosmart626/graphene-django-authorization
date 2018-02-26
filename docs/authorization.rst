Graphene Authorization in Django
=======================

Adding permissions to Nodes
---------------------------
If you want to user the auth django permissions to access a node, we need to inheritance
from ``AuthNodeMixin`` and define a required permissions in the node. This will return
a ``PermissionDenied`` is the user does not have the required permissions.

.. code:: python

    from graphene_django.types import DjangoObjectType
    from graphene_django.auth.mixins import AuthNodeMixin
    from .models import Post

    class PostNode(AuthNodeMixin, DjangoObjectType):
        _permission = 'app.add_post'

        class Meta:
            model = Post
            only_fields = ('title', 'content')
            interfaces = (relay.Node, )

We can set multiple required permissions like this:

.. code:: python

    from graphene_django.types import DjangoObjectType
    from graphene_django.auth.mixins import AuthNodeMixin
    from .models import Post

    class PostNode(AuthNodeMixin, DjangoObjectType):
        _permission = ('app.add_post', 'app.delete_post',)

        class Meta:
            model = Post
            only_fields = ('title', 'content')
            interfaces = (relay.Node, )

Adding permissions to Mutations
---------------------------
If you want to user the auth django permissions to execute a mutation, we need to inheritance
from ``AuthMutationMixin`` and define a required permissions in the node. This will return
a ``PermissionDenied`` is the user does not have the required permissions.

.. code:: python

    class CreatePet(AuthMutationMixin, graphene.Mutation):
        _permission = 'app.create_pet'
        pet = graphene.Field(PetNode)

        class Input:
            name = graphene.String(required=True)

        @classmethod
        def mutate(cls, root, input, context, info):
            # Auth Required Virification
            if cls.has_permision(context) is not True:
                return cls.has_permision(context)
            # End Auth
            pet_name = input.get('name')
            pet = Pet.objects.create(name=pet_name)
            return CreatePet(pet=pet)

We can set multiple required permissions like this:

.. code:: python

    class CreatePet(AuthMutationMixin, graphene.Mutation):
        _permission = ('app.add_pet', 'app.delete_pet')
        pet = graphene.Field(PetNode)

        class Input:
            name = graphene.String(required=True)

        @classmethod
        def mutate(cls, root, input, context, info):
            # Auth Required Virification
            if cls.has_permision(context) is not True:
                return cls.has_permision(context)
            # End Auth
            pet_name = input.get('name')
            pet = Pet.objects.create(name=pet_name)
            return CreatePet(pet=pet)

Adding permissions to filters
-----------------------------
We use DjangoFilterConnectionField to create filters to our nodes. Graphene-django has a field with
permission required ``AuthDjangoFilterConnectionField``. This field requires permissions to access
to it's nodes and is simple to create your filters.

.. code:: python

    class MyCustomFilter(AuthDjangoFilterConnectionField):
        _permission = ('app.add_pet', 'app.delete_pet')

With this example code we can implement filters with required permissions.
