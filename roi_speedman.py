"""
This driver implements some logic.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "MCQUEEN-2"


def drive(world):
    """
    This method controls the car's movement based on the obstacle it encounters.

    Parameters:
    world (World): The game world object containing the car and obstacles.

    Returns:
    Action: An action to perform based on the obstacle encountered.
    """
    x = world.car.x
    y = world.car.y
    obstacle = world.get((x, y - 1))

    obstacles_matrix = [
        [world.get((0, y - 1)), world.get((1, y - 1)), world.get((2, y - 1))],
        [world.get((0, y - 2)), world.get((1, y - 2)), world.get((2, y - 2))],
        [world.get((0, y - 3)), world.get((1, y - 3)), world.get((2, y - 3))],
        [world.get((0, y - 4)), world.get((1, y - 4)), world.get((2, y - 4))],
        [world.get((0, y - 5)), world.get((1, y - 5)), world.get((2, y - 5))],
        [world.get((0, y - 6)), world.get((1, y - 6)), world.get((2, y - 6))]]

    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.NONE:
        return actions.NONE
    else:
        return actions.RIGHT if (x % 3) == 0 else actions.LEFT


def most_point_path(obstacles_matrix, points, x, y) -> list:
    if y == 0:
        return points
    if x == 1:
        middle_obstacles = [obstacles_matrix[y-1][x-1], obstacles_matrix[y-1][x], obstacles_matrix[y-1][x+1]]
        left_points = []
        forward_points = []
        right_points = []
        possible_points = [left_points, forward_points, right_points]
        options = [actions.LEFT, actions.NONE, actions.RIGHT]



    forward = most_point_path(obstacles_matrix, points, x, y - 1)
    if x <= 1:
        right = most_point_path(obstacles_matrix, points, x - 1, y - 1)
    else:
        right = 0
    if x >= 1:
        left = most_point_path(obstacles_matrix, points, x + 1, y - 1)
    else:
        left = 0


    if forward[0] > right[0] and forward[0] > left[0]:
        return forward
    elif right > left:
        return right
    return left


def find_next_obstacle(world, x, car_y):
    y = car_y - 1
    obstacle = world.get((x, y))
    while obstacle == obstacles.NONE and y >= 0:
        y -= 1
        obstacle = world.get((x, y))
    if y < 0:
        return obstacles.NONE, -1
    return obstacle, y


def calculate_points(obstacle):
    if obstacle == obstacles.NONE:
        return 0
    elif obstacle == obstacles.CRACK:
        return 5
    elif obstacle == obstacles.WATER:
        return 4
    elif obstacle == obstacles.PENGUIN:
        return 10
    else:
        return -10