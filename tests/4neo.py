import neomodel
class PersonalRelationship(neomodel.StructuredRel):
    """
    A very simple relationship between two BasePersons that simply
    records the date at which an acquaintance was established.
    """
    on_date = neomodel.DateProperty(default_now = True)

class BasePerson(neomodel.StructuredNode):
    """
    Base class for defining some basic sort of an actor in a system.

    The base actor is defined by its name and a `friends_with`
    relationship.
    """
    name = neomodel.StringProperty(required = True, unique_index = True)
    friends_with = neomodel.RelationshipTo("BasePerson", "FRIENDS_WITH", model = PersonalRelationship)

class TechnicalPerson(BasePerson):
    """
    A Technical person specialises BasePerson by adding their
    expertise.
    """
    expertise = neomodel.StringProperty(required = True)

class PilotPerson(BasePerson):
    """
    A pilot person specialises BasePerson by adding the type of
    airplane they can operate.
    """
    airplane = neomodel.StringProperty(required = True)
# Create some technical persons
A = TechnicalPerson(name = "Grumpy", expertise = "Grumpiness").save()
B = TechnicalPerson(name = "Happy", expertise = "Unicorns").save()
C = TechnicalPerson(name = "Sleepy", expertise = "Pillows").save()

# Create some Pilot Persons
D = PilotPerson(name = "Porco Rosso", airplane = "Savoia-Marchetti").save()
E = PilotPerson(name = "Jack Dalton", airplane = "Beechcraft Model 18").save()

# TechnicalPersons befriend Technical Persons
A.friends_with.connect(B)
B.friends_with.connect(C)
C.friends_with.connect(A)

# Pilot Persons befriend Pilot Persons
D.friends_with.connect(E)

# Technical Persons befriend Pilot Persons
A.friends_with.connect(D)
E.friends_with.connect(C)

for some_friend in A.friends_with:
    print(some_friend)