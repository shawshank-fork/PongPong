from math import inf

CAP_A = 4
CAP_B = 3
GOAL = 2


def goal_state(state):
    a, b = state
    return a == GOAL or b == GOAL


def get_moves(state):
    a, b = state
    moves = []

    moves.append((CAP_A, b))     # Fill A
    moves.append((a, CAP_B))     # Fill B
    moves.append((0, b))         # Empty A
    moves.append((a, 0))         # Empty B

    # Pour A -> B
    pour = min(a, CAP_B - b)
    moves.append((a - pour, b + pour))

    # Pour B -> A
    pour = min(b, CAP_A - a)
    moves.append((a + pour, b - pour))

    return list(set(moves))


def minimax(state, depth, maximizing):

    if goal_state(state):
        return 10 - depth

    if depth == 0:
        return 0

    if maximizing:
        best = -inf
        for move in get_moves(state):
            score = minimax(move, depth - 1, False)
            best = max(best, score)
        return best

    else:
        best = inf
        for move in get_moves(state):
            score = minimax(move, depth - 1, True)
            best = min(best, score)
        return best


def alphabeta(state, depth, alpha, beta, maximizing):

    if goal_state(state):
        return 10 - depth

    if depth == 0:
        return 0

    if maximizing:
        value = -inf
        for move in get_moves(state):

            value = max(value,
                        alphabeta(move, depth - 1, alpha, beta, False))

            alpha = max(alpha, value)

            if beta <= alpha:
                break

        return value

    else:
        value = inf
        for move in get_moves(state):

            value = min(value,
                        alphabeta(move, depth - 1, alpha, beta, True))

            beta = min(beta, value)

            if beta <= alpha:
                break

        return value


def best_move_minimax(state):

    best_score = -inf
    best = None

    for move in get_moves(state):

        score = minimax(move, 5, False)

        if score > best_score:
            best_score = score
            best = move

    return best


def best_move_alphabeta(state):

    best_score = -inf
    best = None

    for move in get_moves(state):

        score = alphabeta(move, 5, -inf, inf, False)

        if score > best_score:
            best_score = score
            best = move

    return best

state = (0, 0)

print("Initial State:", state)

while not goal_state(state):

    state = best_move_alphabeta(state)

    print("AI Move ->", state)

    if goal_state(state):
        print("AI Wins!")
        break

    print("Enter opponent move (a b): ")

    a, b = map(int, input().split())

    state = (a, b)


