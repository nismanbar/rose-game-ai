from rose.common import obstacles, actions  # NOQA

driver_name = "MCQUEEN for real"

max_depth = 3

def evaluate_action(world, x, y, depth, memo, lane_group):
    if depth == 0 or y < 0:
        return 0

    key = (x, y, depth)
    if key in memo:
        return memo[key]

    best_score = float('-inf')
    possible_moves = ['NONE', 'LEFT', 'RIGHT', 'JUMP', 'BRAKE', 'PICKUP']

    for action in possible_moves:
        nx, ny = x, y - 1

        if action == 'LEFT':
            nx = x - 1
        elif action == 'RIGHT':
            nx = x + 1

        # בדיקת גבולות לפי קבוצת המסלול
        if lane_group == 0 and (nx < 0 or nx > 2):
            continue
        if lane_group == 1 and (nx < 3 or nx > 5):
            continue

        obstacle = world.get((nx, ny))

        legal = False
        score = 0

        if obstacle == obstacles.PENGUIN and action == 'PICKUP':
            legal = True
            score += 10
        elif obstacle == obstacles.WATER and action == 'BRAKE':
            legal = True
            score += 4
        elif obstacle == obstacles.CRACK and action == 'JUMP':
            legal = True
            score += 5
        elif obstacle in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
            # מעבר במכשול - legal רק אם פעולה לצד
            if action in ['LEFT', 'RIGHT']:
                legal = True
                # עונש כבד על מעבר במכשול
                score -= 8
            else:
                continue
        elif obstacle == obstacles.NONE:
            if action in ['NONE', 'LEFT', 'RIGHT']:
                legal = True

        if not legal:
            continue

        # עונש מעבר לצד אם המסלול משתנה, כדי למנוע תנועה מיותרת
        if action in ['LEFT', 'RIGHT']:
            score -= 2

        score += evaluate_action(world, nx, ny, depth - 1, memo, lane_group)

        if score > best_score:
            best_score = score

    memo[key] = best_score
    return best_score


def drive(world):
    x = world.car.x
    y = world.car.y

    lane_group = 0 if x <= 2 else 1
    memo = {}

    best_score = float('-inf')
    best_action = actions.NONE

    possible_actions = [actions.NONE, actions.LEFT, actions.RIGHT, actions.JUMP, actions.BRAKE, actions.PICKUP]

    for action in possible_actions:
        nx, ny = x, y - 1
        if action == actions.LEFT:
            nx = x - 1
        elif action == actions.RIGHT:
            nx = x + 1

        if lane_group == 0 and (nx < 0 or nx > 2):
            continue
        if lane_group == 1 and (nx < 3 or nx > 5):
            continue

        obstacle = world.get((nx, ny))

        legal = False
        score = 0

        if obstacle == obstacles.PENGUIN and action == actions.PICKUP:
            legal = True
            score += 10
        elif obstacle == obstacles.WATER and action == actions.BRAKE:
            legal = True
            score += 4
        elif obstacle == obstacles.CRACK and action == actions.JUMP:
            legal = True
            score += 5
        elif obstacle in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
            if action in [actions.LEFT, actions.RIGHT]:
                legal = True
                score -= 8
            else:
                continue
        elif obstacle == obstacles.NONE:
            if action in [actions.NONE, actions.LEFT, actions.RIGHT]:
                legal = True

        if not legal:
            continue

        if action in [actions.LEFT, actions.RIGHT]:
            score -= 2

        score += evaluate_action(world, nx, ny, max_depth - 1, memo, lane_group)

        if score > best_score:
            best_score = score
            best_action = action

    return best_action