from heapq import heappush, heappop  # priority queue operatins
from math import sqrt
from copy import deepcopy
import numpy as np


def tuplify(nested_list):
    """ A set is maintained to account for visied states.
        However, list is not hashable. For that reason we
        allow tuplifying of lists. """
    return tuple([tuple(row) for row in nested_list])


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


def is_solvable(game_board):
    """ Counting inversions ... """

    flat_board = [item for row in game_board for item in row]
    dimension_board = int(sqrt(len(flat_board)))
    row_blank_tile = int(flat_board.index('0') / dimension_board)
    flat_board.remove('0')
    inversions_count = (count_inversions_merge_sort(flat_board))[1]

    if dimension_board % 2 == 1 and inversions_count % 2 == 0:
        return True
    elif dimension_board % 2 == 0 and (inversions_count + row_blank_tile) % 2 == 1:
        return True
    else:
        return False


class Board:
    """ A class to represent a board state. Supplied with
        board representation; keeps tracks of g-score,
        f-score, neighbours and predecessor. """
    def __init__(self, state_board, dimension):
        self.state_board = state_board
        self.dimension = dimension
        self.f_score = 0
        self.g_score = 0
        self.predecessor = (None, None)

    def __str__(self):
        return ('\n'.join([''.join(['{:3}'.format(item) for item in row])
                           for row in self.state_board]))

    def __lt__(self, other):
        return self.f_score < other.f_score

    def manhattan_distance(self, goal_board):
        """ Calculate total manhattan distance as heuristic. """
        manhattan_distance = 0
        size = self.dimension**2
        game_board = np.array(self.state_board)
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

    def explore_neighbours(self):
        """ Depending on position of the blank tile,
            some moves can be perforemed. They result in
            neighbouring states. They are recored in a list.
            During the IDA* this method can be used to
            expand a given board state. """
        list_possible_moves = []
        game_board = np.array(self.state_board)
        index_blank = np.where(game_board == '0')
        index_blank_row, index_blank_col = index_blank[0][0], index_blank[1][0]

        if index_blank_row - 1 >= 0:
            list_possible_moves.append(tuple((index_blank_row - 1,
                                              index_blank_col, 'up')))
        if index_blank_row + 1 <= self.dimension - 1:
            list_possible_moves.append(tuple((index_blank_row + 1,
                                              index_blank_col, 'down')))
        if index_blank_col - 1 >= 0:
            list_possible_moves.append(tuple((index_blank_row,
                                              index_blank_col - 1, 'left')))
        if index_blank_col + 1 <= self.dimension - 1:
            list_possible_moves.append(tuple((index_blank_row,
                                              index_blank_col + 1, 'right')))

        list_neighbours = []
        for move_tuple in list_possible_moves:
            board_after_move = deepcopy(game_board)

            save_tile = board_after_move[move_tuple[0]][move_tuple[1]]
            direction_blank = move_tuple[2]
            board_after_move[move_tuple[0]][move_tuple[1]] = '0'

            if direction_blank == 'up':
                board_after_move[move_tuple[0] + 1][move_tuple[1]] = save_tile

            elif direction_blank == 'down':
                board_after_move[move_tuple[0] - 1][move_tuple[1]] = save_tile

            elif direction_blank == 'left':
                board_after_move[move_tuple[0]][move_tuple[1] + 1] = save_tile

            else:
                board_after_move[move_tuple[0]][move_tuple[1] - 1] = save_tile
            list_neighbours.append(([[item for item in row]
                                     for row in board_after_move],
                                    direction_blank))

        return list_neighbours


class PuzzleSolver:
    """ Uses the 'Board' class to build a 'board tree'.
        Naturally, this is traversed and built by means
        of the IDA* algorithm. """
    def __init__(self, board, goal_board):
        self._board = board  # an instance of Board class
        self._goal_board = goal_board  # NOT an instance of Board class
        self._dimension = self._board.dimension

    def ida_star_wrapper(self):
        """ The crux of the task. Solving N-puzzle with
            iterative deepening A* using the Manhattan heuristic. """
        if not is_solvable(self._board.state_board):
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
            method returns the new threshold. """

        visited = set()  # keeps track of nodes already visited
        fringe = [self._board]
        while fringe:
            board_instance = heappop(fringe)

            if board_instance.f_score > threshold:
                return board_instance.f_score  # new threshold

            if board_instance.state_board == self._goal_board:
                list_directions = []
                predecessor, direction = board_instance.predecessor
                while predecessor is not None:
                    list_directions.append(direction)
                    predecessor, direction = predecessor.predecessor
                return (len(list_directions), list_directions[::-1])

            visited.add(tuplify(board_instance.state_board))
            for neighbour_tuple in board_instance.explore_neighbours():
                if tuplify(neighbour_tuple[0]) not in visited:
                    neighbour = Board(neighbour_tuple[0], self._dimension)
                    neighbour.predecessor = (board_instance, neighbour_tuple[1])
                    neighbour.g_score = board_instance.g_score + 1
                    neighbour.f_score = neighbour.g_score + \
                        neighbour.manhattan_distance(self._goal_board)

                    heappush(fringe, neighbour)


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
        goal_board = list(map(lambda item: str(item),
                              range(1, size_puzzle + 1))) + [str(0)]

    goal_board = [goal_board[index:index + dimension_puzzle]
                  for index in range(0, size_puzzle + 1, dimension_puzzle)]

    start_board_instance = Board(start_board, dimension_puzzle)
    start_board_instance.f_score = start_board_instance.manhattan_distance(goal_board)
    puzzle = PuzzleSolver(start_board_instance, goal_board)

    total_moves, print_list = puzzle.ida_star_wrapper()
    print(total_moves)
    for item in print_list:
        print(item)


if __name__ == '__main__':
    main()
