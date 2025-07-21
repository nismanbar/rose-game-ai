"""
This driver implements some logic.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "MCQUEEN"


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


def find_next_obstacle(world, x, car_y):
    y = car_y - 1
    obstacle = world.get((x, y))
    while obstacle == obstacles.NONE and y >= 0:
        y -= 1
        obstacle = world.get((x, y))
    if y < 0:
        return obstacles.NONE, -1
    return obstacle, y
