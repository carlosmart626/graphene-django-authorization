import graphene
from graphene import Schema, relay, resolve_only_args
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django_authorization.decorators import require_permission

from .data import (create_ship, get_empire, get_faction, get_rebels, get_ship,
                   get_ships)
from .models import Character as CharacterModel
from .models import Faction as FactionModel
from .models import Ship as ShipModel


class Ship(DjangoObjectType):

    class Meta:
        model = ShipModel
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, id, context, info):
        node = get_ship(id)
        return node


class Character(DjangoObjectType):

    class Meta:
        model = CharacterModel


class Faction(DjangoObjectType):

    class Meta:
        model = FactionModel
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, id, context, info):
        return get_faction(id)


class IntroduceShip(graphene.Mutation):

    class Input:
        ship_name = graphene.String(required=True)
        faction_id = graphene.String(required=True)

    ship = graphene.Field(Ship)
    faction = graphene.Field(Faction)

    @classmethod
    @require_permission(permissions=('app.create_ship', ))
    def mutate(cls, root, input, context, info):
        print("User", context.user)
        ship = create_ship(input.get("ship_name"), input.get("faction_id"))
        faction = get_faction(input.get("faction_id"))
        return IntroduceShip(ship=ship, faction=faction)


class Query(graphene.ObjectType):
    rebels = graphene.Field(Faction)
    empire = graphene.Field(Faction)
    node = relay.Node.Field()
    ships = DjangoConnectionField(Ship, description='All the ships.')

    @resolve_only_args
    def resolve_ships(self):
        return get_ships()

    @resolve_only_args
    def resolve_rebels(self):
        return get_rebels()

    @resolve_only_args
    def resolve_empire(self):
        return get_empire()


class Mutation(graphene.ObjectType):
    introduce_ship = IntroduceShip.Field()


# We register the Character Model because if not would be
# inaccessible for the schema
schema = Schema(query=Query, mutation=Mutation, types=[Ship, Character])
