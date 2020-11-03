import numpy as np
import time


class SolveNQueens:
    def __init__(self, size):
        self.size = size
        self.queens = np.zeros((size, ), dtype=int)
        self.row_queens = np.zeros((size, ), dtype=int)  # depends on initial placement strategy
        self.main_diagonal_queens = np.zeros((2 * size - 1, ), dtype=int)
        self.rev_diagonal_queens = np.zeros((2 * size - 1, ), dtype=int)

    def __str__(self):
        if self.size <= 50:
            return_string = ['_'] * self.size * (self.size + 1)
            for column, row in enumerate(self.queens):
                return_string[(self.size + 1) * column + self.size] = '\n'
                return_string[(self.size + 1) * row + column] = '*'
            return "".join(return_string)
        else:
            return "Board is too big. Printing time instead..."

    def initialize_random(self):
        """ Random initial board set-up.
            No two queens conflict row-wise or column-wise. """

        self.queens = np.random.choice(np.arange(self.size), replace=False,
                                       size=(self.size))
        print(self.queens)

        main_diagonal = self.queens - np.arange(self.size)
        rev_diagonal = self.queens + np.arange(self.size)

        unique, counts = np.unique(main_diagonal, return_counts=True)
        for _ in zip(unique, counts):
            self.main_diagonal_queens[unique + self.size - 1] = counts
        self.main_diagonal_queens = np.flip(self.main_diagonal_queens)

        unique, counts = np.unique(rev_diagonal, return_counts=True)
        for _ in zip(unique, counts):
            self.rev_diagonal_queens[unique] = counts

    def initialize_min_conflict(self):
        """ Best possible initialization.
            Greedy strategy (min-conflict) guarantees we always
            choose a less conflicted spot for the next queen. """
        self.queens[0] = np.random.choice(np.arange(self.size))
        self.row_queens[self.queens[0]] += 1
        self.main_diagonal_queens[-self.queens[0] + self.size - 1] += 1
        self.rev_diagonal_queens[self.queens[0]] += 1

        for column in range(1, self.size):
            conflicts_column = self.row_queens + \
                self.main_diagonal_queens[self.size + column - 1: column - 1: -1] + \
                self.rev_diagonal_queens[column : self.size + column : 1]
            place_queen_row = np.random.choice(np.where(conflicts_column == np.amin(conflicts_column))[0])
            self.queens[column] = place_queen_row
            self.row_queens[place_queen_row] += 1
            self.main_diagonal_queens[column - place_queen_row + self.size - 1] += 1
            self.rev_diagonal_queens[column + place_queen_row] += 1

    def solve(self):
        """ Solver method. """

        conflicts = self.get_conflicts()
        count = 0
        while np.amax(conflicts) > 0 and count < 60:
            max_conflicts = np.amax(conflicts)
            move_queen_from_column = np.random.choice(np.where(conflicts == np.amax(conflicts))[0])
            move_queen_from_row = self.queens[move_queen_from_column]

            conflicts_column = np.zeros((self.size, ), dtype=int)
            for queen_row in range(self.size):
                conflicts_column[queen_row] = self.row_queens[queen_row] + \
                    self.main_diagonal_queens[move_queen_from_column - queen_row + self.size - 1] + \
                    self.rev_diagonal_queens[move_queen_from_column + queen_row]
            conflicts_column[move_queen_from_row] = max_conflicts

            move_queen_to_row = np.random.choice(np.where(conflicts_column == np.amin(conflicts_column))[0]) 

            self.queens[move_queen_from_column] = move_queen_to_row

            self.row_queens[move_queen_from_row] -= 1
            self.main_diagonal_queens[move_queen_from_column - move_queen_from_row + self.size - 1] -= 1
            self.rev_diagonal_queens[move_queen_from_column + move_queen_from_row] -= 1

            self.row_queens[move_queen_to_row] += 1
            self.main_diagonal_queens[move_queen_from_column - move_queen_to_row + self.size - 1] += 1
            self.rev_diagonal_queens[move_queen_from_column + move_queen_to_row] += 1

            conflicts = self.get_conflicts()
            count += 1

        if count == 60:
            self.solve()
            return

    def get_conflicts(self):
        """ Calculate conflicts for current configuration. """
        conflicts = np.zeros((self.size, ), dtype=int)
        for queen_column in range(self.size):
            queen_row = self.queens[queen_column]
            conflicts[queen_column] += self.row_queens[queen_row] + \
                self.main_diagonal_queens[queen_column - queen_row + self.size - 1] + \
                self.rev_diagonal_queens[queen_column + queen_row] - 3
        return conflicts


def main():
    """ User interaction.
        Request desired input size."""
    size = int(input('Enter number of queens: ').strip())

    start_time = time.process_time()
    game = SolveNQueens(size)
    game.initialize_min_conflict()
    game.solve()
    print(game)
    print(" --- %.5f seconds ---" % (time.process_time() - start_time))


if __name__ == "__main__":
    main()
