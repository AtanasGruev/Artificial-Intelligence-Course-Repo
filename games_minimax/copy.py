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


def utility(marker, depth):
    """ is_terminal(state) produces a marker of
        type 'X', 'O' or '_'. These markers can be
        translated to numeric values used by the
        minimax algorithm. """
    if marker == 'X':
        return [10 - depth, [0, 0]]
    elif marker == 'O':
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


def max_value(state, depth):
    """ Maximizer funcion. Player 'X'. """
    marker = is_terminal(state)
    if marker is not None:
        return utility(marker, depth)

    value = -10
    move = []

    successors_list = successors(state)
    for row, col in successors_list:
        state[row][col] = 'X'
        alt_value, alt_move = min_value(state, depth + 1)
        if alt_value > value:
            value = alt_value
            move = [row, col]
        state[row][col] = '_'

    return value, move


def min_value(state, depth):
    """ Minimizer function. Player 'O'. """
    marker = is_terminal(state)
    if marker is not None:
        return utility(marker, depth)

    value = 10
    move = []

    successors_list = successors(state)
    for row, col in successors_list:
        state[row][col] = 'O'
        alt_value, alt_move = max_value(state, depth)
        if alt_value < value:
            value = alt_value
            move = [row, col]
        state[row][col] = '_'

    return value, move


def draw_board(state):
    """ Serves visualisation purposes """
    print('-'*20)
    for i in range(3):
        print('|', end="")
        for j in range(3):
            print(state[i][j] + '|', end="")
        print()
    print('-'*20)


def play(state, current_player, first_player, depth):
    """ AI vs. Human - A game of Tic-Tac-Toe. """
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
        if current_player == 'X':
            value, move = max_value(state, depth)
            depth = depth + 1
            state[move[0]][move[1]] = 'X'
            current_player = 'O'

        # Presumably human player's turn.
        else:
            move = list(map(int, input('Enter your move: ').strip('[]').split(',')))
            while not is_valid_move(state, move):
                move = list(map(int, input('Enter your move: ').strip('[]').split(',')))

            state[move[0]-1][move[1]-1] = 'O'
            depth = depth + 1
            current_player = 'X'


def main():
    """ Plays a game of tic-tac-toe. """
    board_state = [['_', '_', '_'],
                   ['_', '_', '_'],
                   ['_', '_', '_']]

    first_player = int(input("Who goes first - select AI(0) or Human(1)? ").strip())
    human_marker = input("Select marker - 'X' or 'O'? ").strip()
    
    play(board_state, first_player, human_marker, 0)


if __name__ == "__main__":
    main()
