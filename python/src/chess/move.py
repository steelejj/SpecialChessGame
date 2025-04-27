import random
from enum import Enum


class MoveDirection(Enum):
    UP = "UP"
    RIGHT = "RIGHT"

def toss_coin():
    return MoveDirection.UP if random.choice([True, False]) else MoveDirection.RIGHT

def roll_dice():
    return random.randint(1, 6)

