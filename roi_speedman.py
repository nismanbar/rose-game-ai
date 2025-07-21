"""
This driver implements some logic.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "MCQUEEN-Different3"


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

    # obstacles_matrix = []
    # for i in range(3 * x // 3, 3 * x // 3 + 3):
    #     obstacles_matrix.append([])
    #     for j in range(8):
    #         obstacles_matrix[i].append(world.get((i, j)))
    #
    # forward = most_point_path(obstacles_matrix, 0, x, y)
    # if x % 3 == 0:
    #     left = -100
    # else:
    #     left = most_point_path(obstacles_matrix, 0, x - 1, y)
    # if x % 3 == 2:
    #     right = -100
    # else:
    #     right = most_point_path(obstacles_matrix, 0, x + 1, y)
    # if right > forward and right > left:
    #     return actions.RIGHT
    # elif left > forward and left > right:
    #     return actions.LEFT

    chosen_action = find_path(world, x, y)
    if chosen_action != actions.NONE:
        print(chosen_action)
        return chosen_action
    elif obstacle == obstacles.PENGUIN:
        print("Penguin!")
        return actions.PICKUP
    elif obstacle == obstacles.WATER:
        print("Stop!")
        return actions.BRAKE
    elif obstacle == obstacles.CRACK:
        print("Jump!")
        return actions.JUMP
    elif obstacle == obstacles.NONE:
        print("Nothing!")
        return actions.NONE
    else:
        print("Turn!")
        return actions.RIGHT if (x % 3) == 0 else actions.LEFT


def most_point_path(obstacles_matrix, points, x, y):
    if y == 0:
        return points
    forward_points = calculate_forward_points(obstacles_matrix[x][y - 1])
    forward = most_point_path(obstacles_matrix, points + forward_points, x, y - 1)
    if x % 3 != 0:
        left_points = calculate_side_points(obstacles_matrix[x - 1][y - 1])
        right = most_point_path(obstacles_matrix, points + left_points, x - 1, y - 1)
    else:
        right = [0]
    if x % 3 != 2:
        right_points = calculate_side_points(obstacles_matrix[x + 1][y - 1])
        left = most_point_path(obstacles_matrix, points + right_points, x + 1, y - 1)
    else:
        left = [0]

    if forward > right and forward > left:
        return forward, actions.NONE
    elif right > left:
        return right, actions.RIGHT
    return left, actions.LEFT


def find_next_obstacle(world, x, car_y):
    y = car_y - 1
    obstacle = world.get((x, y))
    while obstacle == obstacles.NONE and y >= 0:
        y -= 1
        obstacle = world.get((x, y))
    if y < 0:
        return obstacles.NONE, -1
    return obstacle, y


def calculate_side_points(obstacle):
    if obstacle == obstacles.NONE:
        return 0
    elif obstacle == obstacles.PENGUIN:
        return 10
    else:
        return -10


def calculate_forward_points(obstacle):
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


def find_path(world, x, y):
    print("Shalom!")
    # Forward:
    current_y = y
    obstacle = world.get((x, current_y - 1))
    current_points = calculate_forward_points(obstacle)
    forward_points = current_points
    while current_points != -10 and current_y > 0:
        forward_points += current_points
        current_y -= 1
        obstacle = world.get((x, current_y - 1))
        current_points = calculate_forward_points(obstacle)
    forward_y = current_y

    # Left:
    if x % 3 != 0:
        current_y = y
        obstacle = world.get((x - 1, current_y - 1))
        current_points = calculate_side_points(obstacle)
        left_points = current_points
        while current_points != -10 and current_y > 0:
            left_points += current_points
            current_y -= 1
            obstacle = world.get((x - 1, current_y - 1))
            current_points = calculate_forward_points(obstacle)
        left_y = current_y
    else:
        left_points = -100
        left_y = y

    # Right:
    if x % 3 != 2:
        current_y = y
        obstacle = world.get((x + 1, current_y - 1))
        current_points = calculate_side_points(obstacle)
        right_points = current_points
        while current_points != -10 and current_y > 0:
            right_points += current_points
            current_y -= 1
            obstacle = world.get((x + 1, current_y - 1))
            current_points = calculate_forward_points(obstacle)
        right_y = current_y
    else:
        right_points = -100
        right_y = y

    print(left_y, forward_y, right_y)

    if right_points > left_points and right_points > forward_points and right_y < y - 1:
        return actions.RIGHT
    elif left_points > right_points and left_points > forward_points and left_y < y - 1:
        return actions.LEFT
    elif forward_points > left_points and forward_points > right_points and forward_y < y - 1:
        return actions.NONE
    elif right_y < y - 1:
        return actions.RIGHT
    elif left_y < y - 1:
        return actions.LEFT
    else:
        return actions.NONE
