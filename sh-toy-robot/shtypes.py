"""File holding the Enums and Exceptions for the application. Constants, basically """
from enum import Enum

class Direction(Enum):
    """ Enum with possible rotations for the item. Its actual value is unimportant"""
    LEFT = -90
    RIGHT = 90


class Facing(Enum):
    """ Enum with possible facings for the item. """
    __order__ = 'NORTH WEST SOUTH EAST'  # Required because of backwards compatibility
    NORTH = 'North'
    WEST = 'West'
    SOUTH = 'South'
    EAST = 'East'

    def get_rotated(self, direction):
        """
            Again, a stylistic choice - I did not want to do "magic" list
            navigation. This is a "state" machine, and I've mapped the
            states to a simple dictionary. Alternative is calculating and
            then using modulo for the new direction, or even using nested ifs.
            (would be ugly and un-pythonic)
        """
        _rotate = {
            Direction.LEFT : {
                Facing.NORTH : Facing.WEST,
                Facing.WEST : Facing.SOUTH,
                Facing.SOUTH : Facing.EAST,
                Facing.EAST : Facing.NORTH
            },
            Direction.RIGHT : {
                Facing.NORTH : Facing.EAST,
                Facing.EAST : Facing.SOUTH,
                Facing.SOUTH : Facing.WEST,
                Facing.WEST : Facing.NORTH
            }
        }
        return _rotate[direction][self]


class InvalidCommand(Exception):
    """ Commands that cannot be executed and can safely be ignored. """
    pass
