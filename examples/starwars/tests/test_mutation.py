import pytest
from unittest.mock import Mock

from ..data import initialize
from ..schema import schema

pytestmark = pytest.mark.django_db


class MockUserContext(object):

    def __init__(self, authenticated=True, is_staff=False, superuser=False, perms=()):
        self.user = self
        self.authenticated = authenticated
        self.is_staff = is_staff
        self.is_superuser = superuser
        self.perms = perms

    def is_authenticated(self):
        return self.authenticated

    def has_perm(self, check_perms):
        if check_perms not in self.perms:
            return False
        return True


anonymous = MockUserContext(authenticated=False)
luke = MockUserContext(
    authenticated=True,
    perms=('app.view_ship', 'app.create_ship',)
)
anakin = MockUserContext(
    authenticated=True,
    perms=('app.view_ship',)
)
storm_tropper = MockUserContext(
    authenticated=True,
    perms=()
)


def test_mutations():
    initialize()

    query = '''
    mutation MyMutation {
      introduceShip(shipName: "Peter", factionId: "1") {
        ship {
          id
          name
        }
        faction {
          name
          ships {
            edges {
              node {
                id
                name
              }
            }
          }
        }
      }
    }
    '''
    expected = {
        'introduceShip': {
            'ship': {
                'id': 'U2hpcDo5',
                'name': 'Peter'
            },
            'faction': {
                'name': 'Alliance to Restore the Republic',
                'ships': {
                    'edges': [{
                        'node': {
                            'id': 'U2hpcDox',
                            'name': 'X-Wing'
                        }
                    }, {
                        'node': {
                            'id': 'U2hpcDoy',
                            'name': 'Y-Wing'
                        }
                    }, {
                        'node': {
                            'id': 'U2hpcDoz',
                            'name': 'A-Wing'
                        }
                    }, {
                        'node': {
                            'id': 'U2hpcDo0',
                            'name': 'Millenium Falcon'
                        }
                    }, {
                        'node': {
                            'id': 'U2hpcDo1',
                            'name': 'Home One'
                        }
                    }, {
                        'node': {
                            'id': 'U2hpcDo5',
                            'name': 'Peter'
                        }
                    }]
                },
            }
        }
    }
    result = schema.execute(query, context_value=Mock(user=anonymous))
    assert result.errors[0].message == 'Permission Denied'
    result = schema.execute(query, context_value=Mock(user=storm_tropper))
    assert result.errors[0].message == 'Permission Denied'
    result = schema.execute(query, context_value=Mock(user=anakin))
    assert result.errors[0].message == 'Permission Denied'
    result = schema.execute(query, context_value=Mock(user=luke))
    assert not result.errors
    assert result.data == expected
