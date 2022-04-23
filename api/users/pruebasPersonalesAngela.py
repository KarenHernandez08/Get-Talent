from django.db import models
from enum import Enum, unique
@unique

class Mistake(Enum):
     ONE = 'uno'
     TWO = 2
     THREE = 3
     FOUR = 4
from django.db import models
print(Mistake.ONE.value)

class Shake(Enum):
     VANILLA = 7
     CHOCOLATE = 4
     COOKIES = 9
     MINT = 3

for shake in Shake:
     print(shake)


class Vehicle(models.TextChoices):
     CAR = 'C'
     TRUCK = 'T'
     JETL_SKI = 'Jet Skis'

print(Vehicle.JETL_SKI.label)
print(Vehicle.JETL_SKI)

class Card(models.Model):

    class Suit(models.IntegerChoices):
        DIAMOND = 1
        SPADE = 2
        HEART = 3
        CLUB = 4

    suit = models.IntegerField(choices=Suit.choices)
    

print(Card.suit)
