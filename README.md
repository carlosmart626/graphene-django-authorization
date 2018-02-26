# Graphene-Django-Authorization

This project enable Graphene Django to use Django Permissions and give some mixins to implement permissions.

### Examples
Example permission required in Node using `AuthNodeMixin`.

```python
from graphene_django.auth.mixins import AuthNodeMixin
from .models import Post

class PostNode(AuthNodeMixin, DjangoObjectType):
    _permission = ('app.add_post', 'app.delete_post',)

    class Meta:
        model = Post
        only_fields = ('title', 'content')
        interfaces = (relay.Node, )
```
Example permission required in Mutation using `AuthMutationMixin`.

```python
from graphene_django.auth.mixins import AuthMutationMixin


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
```

### Contribute
```bash
pip install -e ".[test]"
```