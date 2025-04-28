import random
from enum import Enum


class MoveDirection(Enum):
    """Enumeration of possible movement directions for a chess piece."""

    UP = "up"
    RIGHT = "right"


def toss_coin() -> MoveDirection:
    """Simulate a coin toss to choose a move direction.

    Returns:
        MoveDirection: UP if the coin toss is heads, otherwise RIGHT.
    """
    return MoveDirection.UP if random.choice([True, False]) else MoveDirection.RIGHT


def roll_dice() -> int:
    """Simulate rolling a six-sided die.

    Returns:
        int: A random integer between 1 and 6, inclusive.
    """
    return random.randint(1, 6)
