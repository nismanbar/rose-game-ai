"""
This driver implement some logic.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "MCQUEENtnd"


def drive(world):
    """
    משדרג את הנהג כך שיחפש את הפינגווינים הקרובים ביותר במסך,
    יעקוף מכשולים, ויאסוף כמה שיותר פינגווינים.
    """
    x = world.car.x
    y = world.car.y

    # חפש את הפינגווין הקרוב ביותר בטווח ראייה של 5 שורות קדימה
    penguins = []
    for dy in range(1, 6):
        for dx in [-1, 0, 1]:
            nx = x + dx
            ny = y - dy
            if world.get((nx, ny)) == obstacles.PENGUIN:
                penguins.append((abs(dx) + dy, dx, dy))

    if penguins:
        # מצא את הפינגווין הקרוב ביותר לפי מרחק מנורמל
        penguins.sort()
        _, dx, dy = penguins[0]
        if dx < 0:
            return actions.LEFT
        elif dx > 0:
            return actions.RIGHT
        else:
            # אנחנו כבר בקו שלו, נתקדם
            obstacle = world.get((x, y - 1))
            if obstacle == obstacles.PENGUIN:
                return actions.PICKUP
            elif obstacle == obstacles.WATER:
                return actions.BRAKE
            elif obstacle == obstacles.CRACK:
                return actions.JUMP
            else:
                return actions.NONE

    # אם אין פינגווינים קרובים, נמשיך להתקדם בבטחה
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
        # כדי לא להיתקע, נזוז לסירוגין
        return actions.RIGHT if (x % 2) == 0 else actions.LEFT
