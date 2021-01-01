def is_terminal(state):
    """ To make algorithm optimal, a way
        to record depth is required. TODO.

        Return 1 if maximizer (X) wins.
        Return (-1) if minimizer (O) wins.
        Return 0 if a tie occurs.

        is_terminal(state) integrates the
        utility function. """

    # Horizontal check
    for i in range(3):
        if state[i] == ['X', 'X', 'X']:
            return 'X'
        elif state[i] == ['O', 'O', 'O']:
            return 'O'

    # Vertical check
    for i in range(3):
        if state[0][i] != '_' and state[0][i] == state[1][i] and \
           state[1][i] == state[2][i]:
            return state[0][i]

    # Main diagonal check
    if state[0][0] != '_' and state[0][0] == state[1][1] and \
       state[1][1] == state[2][2]:
        return state[0][0]

    # Other diagonal check
    if state[0][2] != '_' and state[0][2] == state[1][1] and \
       state[1][1] == state[2][0]:
        return state[0][2]

    # The game continues if the board has empty squares
    for i in range(3):
        for j in range(3):
            if state[i][j] == '_':
                return None

    return '_'


def utility(result, depth):
    """ is_terminal(state) produces a result of
        type 'X', 'O' or '_'. These results can be
        translated to numeric values used by the
        minimax algorithm. """
    if result == 'X':
        return [10 - depth, [0, 0]]
    elif result == 'O':
        return [depth - 10, [0, 0]]
    else:
        return [0, [0, 0]]


def successors(state):
    """ Given a current board, possible actions are explored,
        i.e. all opportunities of placing a marker in a free square. """
    free_coordinates = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == '_':
                free_coordinates.append([i, j])

    return free_coordinates


def is_valid_move(state, move):
    """ Validates human player move. """
    row, col = move
    if row not in [1, 2, 3] or col not in [1, 2, 3]:
        print("Invalid move! Specify correct game square!")
        return False
    if state[row-1][col-1] != '_':
        print('Invalid move! Place your marker on a free square!')
        return False
    return True


def max_value(state, marker, depth, alpha, beta):
    """ Maximizer funcion. """
    result = is_terminal(state)
    if result is not None:
        return utility(result, depth)

    value = -10
    move = []
    alt_marker = 'O' if marker == 'X' else 'X'

    successors_list = successors(state)
    for row, col in successors_list:
        state[row][col] = marker
        alt_value = min_value(state, alt_marker, depth + 1, alpha, beta)[0]
        if alt_value > value:
            value = alt_value
            move = [row, col]
        state[row][col] = '_'
        if value >= beta:
            break
        if alpha < value:
            alpha = value

    return value, move, alpha, beta


def min_value(state, marker, depth, alpha, beta):
    """ Minimizer function. """
    result = is_terminal(state)
    if result is not None:
        return utility(result, depth)

    value = 10
    move = []
    alt_marker = 'X' if marker == 'O' else 'O'

    successors_list = successors(state)
    for row, col in successors_list:
        state[row][col] = marker
        alt_value = max_value(state, alt_marker, depth + 1, alpha, beta)[0]
        if alt_value < value:
            value = alt_value
            move = [row, col]
        state[row][col] = '_'
        if value <= alpha:
            break
        if beta > value:
            beta = value

    return value, move, alpha, beta


def draw_board(state):
    """ Serves visualisation purposes """
    print('-'*20)
    for i in range(3):
        print('|', end="")
        for j in range(3):
            print(state[i][j] + '|', end="")
        print()
    print('-'*20)


def play(state, player_turn, human_marker, depth):
    """ AI vs. Human - A game of Tic-Tac-Toe. """
    alpha = -10
    beta = 10
    while True:
        draw_board(state)
        marker = is_terminal(state)

        if marker is not None:
            if marker == 'X':
                print("The winner is 'X'!")
            elif marker == 'O':
                print("The winner is 'O'!")
            else:
                print("The game ended in a tie!")
            return

        # Presumably AI's turn.
        if player_turn == 0:
            ai_marker = 'X' if human_marker == 'O' else 'O'
            if ai_marker == 'X':
                value, move = max_value(state, ai_marker, depth, alpha, beta)[:2]
            else:
                value, move = min_value(state, ai_marker, depth, alpha, beta)[:2]
            depth = depth + 1
            state[move[0]][move[1]] = ai_marker
            player_turn = 1

        # Presumably human player's turn.
        else:
            move = list(map(int, input('Enter your move: ').strip('[]').split(',')))
            while not is_valid_move(state, move):
                move = list(map(int, input('Enter your move: ').strip('[]').split(',')))

            state[move[0]-1][move[1]-1] = human_marker
            depth = depth + 1
            player_turn = 0


def main():
    """ Plays a game of tic-tac-toe. """
    board_state = [['_', '_', '_'],
                   ['_', '_', '_'],
                   ['_', '_', '_']]

    player_turn = int(input("Who goes first - select AI(0) or Human(1)? ").strip())
    human_marker = input("Select marker - 'X' or 'O'? ").strip()
    
    play(board_state, player_turn, human_marker, 0)


if __name__ == "__main__":
    main()
