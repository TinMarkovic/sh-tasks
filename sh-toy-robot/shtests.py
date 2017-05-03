"""
Test suite for the Seek and Hit application. I haven't "completely" covered the
application because of time constraints, but I hoped that this much is enough
to demonstrate some capability in testing.
"""
import unittest

from shtoyrobot import Robot, Terrain, Position, CommandCenter
from shtypes import Direction, Facing, InvalidCommand

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Robot()
        self.terrain = Terrain()
        self.position = Position()
        self.robot.deploy(self.terrain, self.position)

    def test_rotate_left(self):
        self.assertEqual(self.robot.position.facing, Facing.NORTH)
        self.robot.rotate(Direction.LEFT)
        self.assertEqual(self.robot.position.facing, Facing.WEST)
        self.robot.rotate(Direction.LEFT)
        self.assertEqual(self.robot.position.facing, Facing.SOUTH)
        self.robot.rotate(Direction.LEFT)
        self.assertEqual(self.robot.position.facing, Facing.EAST)
        self.robot.rotate(Direction.LEFT)
        self.assertEqual(self.robot.position.facing, Facing.NORTH)

    def test_rotate_right(self):
        self.assertEqual(self.robot.position.facing, Facing.NORTH)
        self.robot.rotate(Direction.RIGHT)
        self.assertEqual(self.robot.position.facing, Facing.EAST)
        self.robot.rotate(Direction.RIGHT)
        self.assertEqual(self.robot.position.facing, Facing.SOUTH)
        self.robot.rotate(Direction.RIGHT)
        self.assertEqual(self.robot.position.facing, Facing.WEST)
        self.robot.rotate(Direction.RIGHT)
        self.assertEqual(self.robot.position.facing, Facing.NORTH)

    def test_rotate_invalid_direction_argument_string(self):
        with self.assertRaises(ValueError):
            self.robot.rotate('right')

    def test_rotate_invalid_direction_argument_literal_enum_value(self):
        with self.assertRaises(ValueError):
            self.robot.rotate(90)

    def test_rotate_when_robot_is_inactive(self):
        inactive_robot = Robot()
        with self.assertRaises(InvalidCommand):
            inactive_robot.rotate(Direction.RIGHT)

    def test_move_by_y(self):
        self.robot.move()
        self.assertEqual(self.robot.position, Position(0, 1, Facing.NORTH))

    def test_move_by_x(self):
        self.robot.rotate(Direction.RIGHT).move()
        self.assertEqual(self.robot.position, Position(1, 0, Facing.EAST))

    def test_move_invalid_by_y(self):
        with self.assertRaises(InvalidCommand):
            self.robot.rotate(Direction.LEFT).rotate(Direction.LEFT).move()
            print self.robot.position

    def test_move_invalid_by_x(self):
        with self.assertRaises(InvalidCommand):
            self.robot.rotate(Direction.LEFT).move()

    def test_move_invalid_by_x_terrain_bound(self):
        self.robot.rotate(Direction.LEFT)
        with self.assertRaises(InvalidCommand):
            for i in range(1, 10):
                self.robot.move()

    def test_move_invalid_by_y_terrain_bound(self):
        with self.assertRaises(InvalidCommand):
            for i in range(1, 10):
                self.robot.move()

    def test_move_when_robot_is_inactive(self):
        inactive_robot = Robot()
        with self.assertRaises(InvalidCommand):
            inactive_robot.move()

    def test_deploy(self):
        robot2 = Robot()
        self.assertEqual(robot2.active, False)
        robot2.deploy(Terrain(2, 2), Position(1, 1))
        self.assertEqual(robot2.active, True)

    def test_deploy_invalid_args(self):
        robot2 = Robot()
        with self.assertRaises(ValueError):
            robot2.deploy({'x':6, 'y':6}, {'x':2, 'y':2, 'facing': Facing.NORTH})

    def test_deploy_invalid_position(self):
        robot2 = Robot()
        with self.assertRaises(ValueError):
            robot2.deploy(Terrain(2, 2), Position(3, 1))

    def test_deploy_invalid_position_negative_x(self):
        robot2 = Robot()
        with self.assertRaises(ValueError):
            robot2.deploy(Terrain(2, 2), Position(-1, 1))

    def test_deploy_invalid_position_negative_y(self):
        robot2 = Robot()
        with self.assertRaises(ValueError):
            robot2.deploy(Terrain(2, 2), Position(1, -1))

class TestTerrain(unittest.TestCase):
    def test_constructor_invalid_assignment_x(self):
        with self.assertRaises(ValueError):
            custom_terrain = Terrain(-10, 10)

    def test_constructor_invalid_assignment_y(self):
        with self.assertRaises(ValueError):
            custom_terrain = Terrain(10, -10)


class TestPosition(unittest.TestCase):
    def test_constructor_invalid_facing(self):
        with self.assertRaises(ValueError):
            position = Position(-10, 10, 'North')

    def test_eq_ne(self):
        self.assertEqual(Position(10, 10, Facing.NORTH), Position(10, 10, Facing.NORTH))
        self.assertNotEqual(Position(10, 10, Facing.NORTH), Position(10, 10, Facing.SOUTH))


class TestCommandCenter(unittest.TestCase):
    # Didn't consider it neccessary to cover this one with a full test suite, too, so it's
    # just a bigger detailed test case.
    def test_command_from_docs(self):
        cmnd = CommandCenter(Robot(), Terrain())
        print ''
        cmnd.command('PLACE 0,0,NORTH MOVE REPORT')
        self.assertEqual(cmnd.robot.position, Position(0, 1, Facing.NORTH))
        cmnd.command('PLACE 0,0,NORTH LEFT REPORT')
        self.assertEqual(cmnd.robot.position, Position(0, 0, Facing.WEST))
        cmnd.command('PLACE 1,2,EAST MOVE MOVE LEFT MOVE REPORT')
        self.assertEqual(cmnd.robot.position, Position(3, 3, Facing.NORTH))


if __name__ == '__main__':
    unittest.main(verbosity=2)
