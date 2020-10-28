from heapq import heappush, heappop  # priority queue operatins
from math import sqrt
from copy import deepcopy
import numpy as np


def tuplify(game_board):
    """ Flattens lists to make them hashable objects. """
    return tuple([tuple(item) for item in game_board])


def count_inversions_merge_sort(flat_board):
    """ Counts inversions using recursive merge sort
        (divide-and_conquer). This count can be used
        to determine whether the puzzle is solvable. """
    if len(flat_board) < 2:
        return flat_board, 0
    else:
        left = flat_board[:len(flat_board)//2]
        right = flat_board[len(flat_board)//2:]

        left, left_inversions = count_inversions_merge_sort(left)
        right, right_inversions = count_inversions_merge_sort(right)
        result = []

        left_index, right_index = 0, 0
        number_inversions = left_inversions + right_inversions
        while left_index < len(left) and right_index < len(right):
            if int(left[left_index]) <= int(right[right_index]):
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
                number_inversions += len(left) - left_index

        result += left[left_index:]
        result += right[right_index:]

    return result, number_inversions


def perform_move(game_board, move_tuple):
    """ Returns a new game board, resulting from
        moving the blank tile acoordingly. """
    save_tile = game_board[move_tuple[0]][move_tuple[1]]
    direction_blank = move_tuple[2]
    game_board[move_tuple[0]][move_tuple[1]] = '0'
    if direction_blank == 'up':
        game_board[move_tuple[0] + 1][move_tuple[1]] = save_tile
    elif direction_blank == 'down':
        game_board[move_tuple[0] - 1][move_tuple[1]] = save_tile
    elif direction_blank == 'left':
        game_board[move_tuple[0]][move_tuple[1] + 1] = save_tile
    else:
        game_board[move_tuple[0]][move_tuple[1] - 1] = save_tile

    return game_board


def manhattan_distance(game_board, goal_board, dimension):
    """ Calculate total manhattan distance as heuristic. """
    manhattan_distance = 0
    size = dimension**2
    game_board = np.array(game_board)
    final_board = np.array(goal_board)
    for number in range(1, size):
        # Numpy makes indices checks easier
        current_index = np.where(game_board == str(number))
        goal_index = np.where(final_board == str(number))
        current_row, current_col = current_index[0][0], current_index[1][0]
        goal_row, goal_col = goal_index[0][0], goal_index[1][0]
        manhattan_distance += abs(current_row - goal_row) + \
            abs(current_col - goal_col)
    return manhattan_distance


class PuzzleBoard:
    """ Implementation of the N-puzzle class.
        It support methods for constructing the puzzle (initial state),
        moving tiles, storing heuristics (hamming / manhattan), detecting
        goal states, etc. """
    def __init__(self, start_board, goal_board, dimension):
        self._board = start_board
        self._goal_board = goal_board
        self._dimension = dimension

    def __str__(self):
        return ('\n'.join([''.join(['{:3}'.format(item) for item in row])
                           for row in self._board]))

    def is_solvable(self):
        """ Counting inversions ... """

        flat_board = [item for row in self._board for item in row]
        row_blank_tile = int(flat_board.index('0') / self._dimension)
        flat_board.remove('0')
        inversions_count = (count_inversions_merge_sort(flat_board))[1]

        if self._dimension % 2 == 1 and inversions_count % 2 == 0:
            return True
        elif self._dimension % 2 == 0 and (inversions_count + row_blank_tile) % 2 == 1:
            return True
        else:
            return False

    def possible_move_tiles(self):
        """ Method for expanding the nodes of the graph.
            Allowable moves are added to a list of
            "neighbour" states, employed in A* algorithm. """
        list_possible_moves = []
        game_board = np.array(self._board)
        index_blank = np.where(game_board == '0')
        index_blank_row, index_blank_col = index_blank[0][0], index_blank[1][0]

        if index_blank_row - 1 >= 0:
            list_possible_moves.append(tuple((index_blank_row - 1,
                                              index_blank_col, 'up')))
        if index_blank_row + 1 <= self._dimension - 1:
            list_possible_moves.append(tuple((index_blank_row + 1,
                                              index_blank_col, 'down')))
        if index_blank_col - 1 >= 0:
            list_possible_moves.append(tuple((index_blank_row,
                                              index_blank_col - 1, 'left')))
        if index_blank_col + 1 <= self._dimension - 1:
            list_possible_moves.append(tuple((index_blank_row,
                                              index_blank_col + 1, 'right')))
        return list_possible_moves

    def ida_star_wrapper(self):
        """ The crux of the task. Solving N-puzzle with
            iterative deepening A* using the Manhattan
            heuristic. """
        if not self.is_solvable():
            return 'Not solvable!'

        threshold = 1
        result = self.bounded_a_star(threshold)
        while not isinstance(result, tuple):
            threshold = int(result)
            result = self.bounded_a_star(threshold)

        return result

    def bounded_a_star(self, threshold):
        """ Performs A* algorithm with a given threshold.
            If the threshold (f-score) is exceeded, the
            method return the new threshold. """

        # LEGEND:
        #    (.) self._board -> 'board' data of the class, lists
        #    (.) tupled_board -> same as self._board, but tuples instead of lists
        #    (.) board -> head of fringe, lists; after tuplify() -> tuples
        #    (.) next_board -> board after performing a move
        #    (.) tupled_next_board -> same as next_board, but tuples instead of lists

        save_initial_board = deepcopy(self._board)
        tupled_board = tuplify(self._board)

        g_cost_dict = {}  # dictionary for g-values
        g_cost_dict[tupled_board] = 0

        f_cost_dict = {}  # dictionary for f-values
        f_cost_dict[tupled_board] = manhattan_distance(self._board,
                                                       self._goal_board,
                                                       self._dimension)

        pred_dict = {}
        pred_dict[tupled_board] = None  # keeps track of blank tile moves
        visited = set()  # keeps track of nodes already visited

        fringe = [(f_cost_dict[tupled_board], self._board)]
        while fringe:
            f_score, board = heappop(fringe)

            if f_score > threshold:
                self._board = save_initial_board
                return f_score  # new threshold for the next iteration

            if board == self._goal_board:
                print_list = []
                prev_state = pred_dict[tuplify(board)]
                while prev_state is not None:
                    board_np = np.array(board)
                    prev_state_np = np.array(prev_state)

                    succ_row, succ_col = np.where(board_np == '0')
                    prev_row, prev_col = np.where(prev_state_np == '0')
                    direction = (prev_row[0] - succ_row[0], prev_col[0] - succ_col[0])

                    if direction == (1, 0):
                        print_list.append('up')
                    elif direction == (-1, 0):
                        print_list.append('down')
                    elif direction == (0, 1):
                        print_list.append('left')
                    else:
                        print_list.append('right')
                        
                    board = prev_state
                    prev_state = pred_dict[tuplify(prev_state)]

                return (len(print_list), print_list[::-1])

            visited.add(tuplify(board))  # probably will need a fix later
            self._board = deepcopy(board)
            list_possible_moves = self.possible_move_tiles()

            for move_tuple in list_possible_moves:
                board = deepcopy(self._board)
                next_board = perform_move(board, move_tuple)  # board is affected
                tupled_next_board = tuplify(next_board)

                if tupled_next_board not in visited:
                    g_cost_dict[tupled_next_board] = g_cost_dict[tuplify(self._board)] + 1
                    f_cost_dict[tupled_next_board] = g_cost_dict[tuplify(self._board)] + \
                        manhattan_distance(next_board, self._goal_board,
                                           self._dimension)
                    heappush(fringe, (f_cost_dict[tupled_next_board], next_board))
                    pred_dict[tupled_next_board] = self._board


def main():
    """ Game and algorithm initialization. """

    # Expected values: 8, 15, 24
    size_puzzle = int(input('Enter number of tiles: ').strip())
    dimension_puzzle = int(sqrt(size_puzzle + 1))

    index_blank = input('Enter position of blank tile: ').strip()
    if index_blank == '-1':
        index_blank = size_puzzle
    elif int(index_blank) > size_puzzle:
        print('Invalid index for blank tile. Aborting...')
        return

    start_board = []
    for _ in range(dimension_puzzle):
        start_board.append(input().strip().split())

    if int(index_blank) < size_puzzle:
        goal_board = [str(item) for item in range(1, int(index_blank) + 1)] + \
                     [str(0)] + \
                     [str(item) for item in range(int(index_blank) + 1,
                                             size_puzzle + 1)]
    else:
        goal_board = list(map(lambda item: str(item), range(1, size_puzzle + 1))) + [str(0)]

    goal_board = [goal_board[index:index + dimension_puzzle]
                  for index in range(0, size_puzzle + 1, dimension_puzzle)]

    game = PuzzleBoard(start_board, goal_board, dimension_puzzle)

    total_moves, print_list = game.ida_star_wrapper()
    print(total_moves)
    for item in print_list:
        print(item)


if __name__ == '__main__':
    main()
