"""
Simple set of classes for a Seek&Hit interview. Code should be
pretty self-explanatory (yay for Python), and I've tried to keep
to the coding style I would be using in a real life application.
"""
from abc import ABCMeta, abstractmethod
import sys

from shtypes import Direction, Facing, InvalidCommand


class Position(object):
    """Position of an item, described with X, Y, and Facing. """
    def __init__(self, x=0, y=0, facing=Facing.NORTH):
        if not isinstance(facing, Facing):
            raise ValueError("Facing must be an instance of Facing enum")
        self.x = int(x)
        self.y = int(y)
        self.facing = facing

    def __str__(self):
        return "%s,%s,%s" % (self.x, self.y, self.facing.name)

    def __eq__(self, other):
        """ Overriding the '==' operator to reference values in object. """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """ Overriding the '==' operator to reference values in object. """
        return not self.__dict__ == other.__dict__


class Terrain(object):
    """Terrain representing class, bound with X and Y dimensions. """
    def __init__(self, x=5, y=5):
        if x < 0 or y < 0:
            raise ValueError("Illegally defined terrain: requires positive X and Y size")
        self.x = int(x)
        self.y = int(y)


class Mobile(object):
    """Abstract interface for a mobile item."""
    __metaclass__ = ABCMeta
    position = None

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def rotate(self, direction):
        pass


class Robot(Mobile):
    """The robot is a mobile item intended to be deployed to a terrain in a cetain position."""
    # Dictionary describing a required movement vector
    _move = {
        Facing.NORTH : (0, 1),
        Facing.WEST : (-1, 0),
        Facing.SOUTH : (0, -1),
        Facing.EAST : (1, 0),
    }

    def __init__(self):
        self.active = False  # Robot is active when placed on terrain
        self.terrain = None
        self.position = None

    def deploy(self, terrain, position):
        if not (isinstance(position, Position) and isinstance(terrain, Terrain)):
            raise ValueError("Position and Terrain must be instances of their respective Classes")
        if not 0 <= position.x < terrain.x:
            raise ValueError("Robot would land out of terrain bounds horizontally (X)")
        if not 0 <= position.y < terrain.y:
            raise ValueError("Robot would land out of terrain bounds vertically (Y)")

        self.terrain = terrain
        self.position = position
        self.active = True

        return self

    def move(self):
        """
            Movement was a stylistic choice - there is also an alternative
            in which I'd calculate movement through sine/cosine and an actual
            rotation angle - I've decided that it's not required for a simple
            implementation like this. (and would be harder to read/debug)
        """
        if not self.active:
            raise InvalidCommand("Robot is inactive")

        delta_x, delta_y = self._move[self.position.facing]

        if not 0 <= (self.position.x + delta_x) < self.terrain.x:
            raise InvalidCommand("Robot would leave terrain bounds horizontally (X)")
        if not 0 <= (self.position.y + delta_y) < self.terrain.y:
            raise InvalidCommand("Robot would leave terrain bounds vertically (Y)")

        self.position.x += delta_x
        self.position.y += delta_y

        return self

    def rotate(self, direction):
        if not self.active:
            raise InvalidCommand("Robot is inactive")
        if not isinstance(direction, Direction):
            raise ValueError("Direction must be an instance of Direction enum")

        self.position.facing = self.position.facing.get_rotated(direction)

        return self

class CommandCenter(object):
    """Object representing the API for our user. """
    _string_to_facing = {
        'NORTH' : Facing.NORTH,
        'EAST' : Facing.EAST,
        'WEST' : Facing.WEST,
        'SOUTH' : Facing.SOUTH
    }

    def __init__(self, robot, terrain):
        self.robot = robot
        self.terrain = terrain
        self.buffer = None

        self._command_set = {
            'PLACE' : (self.deploy_robot, None),
            'MOVE' : (self.robot.move, None),
            'LEFT' : (self.robot.rotate, Direction.LEFT),
            'RIGHT' : (self.robot.rotate, Direction.RIGHT),
            'REPORT' : (self.get_robot_position, None)
        }

    def command(self, user_input):
        self.buffer = user_input.split(' ')
        while self.buffer:
            current_command = self.buffer.pop(0)
            function_to_call, argument = self._command_set[current_command]
            try:
                if argument:
                    function_to_call(argument)
                else:
                    function_to_call()
            except InvalidCommand:
                pass  # We want to ignore invalid commands (per requirements)

    def position_factory(self, position):
        pos_args = position.split(',')
        return Position(pos_args[0], pos_args[1], self._string_to_facing[pos_args[2].upper()])

    def get_robot_position(self):
        print self.robot.position

    def deploy_robot(self):
        self.robot.deploy(self.terrain, self.position_factory(self.buffer.pop(0)))

if __name__ == "__main__":
    command_center = CommandCenter(Robot(), Terrain())
    sys.argv.pop(0)
    for argument in sys.argv:
        print '==============='
        print argument
        print '---------------'
        command_center.command(argument)
    print '==============='
