import numpy as np

# Some additional sources were used to perform the GA's functionality

# 1)
# A route's distance is inversely proportional to expected fitness of a specimen
# To that end, I explored how we can assign a higher probability to shorter distances.
# https://stats.stackexchange.com/questions/277298/create-a-higher-probability-to-smaller-values

# 2)
# Once we have the points randomly in the grid, we can calculate all O(N^2) distances between each pair.
# compute_distance_matrix() utilises the good ideas discussed in the following thread:
# https://stackoverflow.com/questions/22720864/efficiently-calculating-a-euclidean-distance-matrix-using-numpy


def compute_distance_matrix(coordinates_matrix):
    """ Uses numpy to calculate Euclidean distance between
        any two points (towns). This can be done in more
        standard ways at the expense of extra time. """
    x_axis = coordinates_matrix[:, 0]  # extract x-coordinates
    y_axis = coordinates_matrix[:, 1]  # extract y-coordinates

    # Employs numpy broadcasting
    expand_x = x_axis[..., np.newaxis] - x_axis[np.newaxis, ...]
    expand_y = y_axis[..., np.newaxis] - y_axis[np.newaxis, ...]

    distance_matrix = np.array([expand_x, expand_y])
    return (distance_matrix**2).sum(axis=0)**0.5


class Solver:
    """ Solves TSP with genetic algorithm.

        Phases are:
        ->  evaluate: all specimens in the population are evaluated,
            meaning respective distances, fitness and probabilites
            are calculated. Best distance is preserved at each iteration.

        ->  selection: following the assignement of higher mating
            probabilities to better specimens, here we create a
            mating pool with size equal to that of the population.

        ->  crossover: one-point and two-point implementations.
            Each pair of parents produce a pair of children.

        ->  mutation: swap-mutation and insertion-mutation are
            available with some user-defined probability.

        GS performs a fixed number of iterations, printing best
        results in the process. """

    def __init__(self, distance_matrix, population_size):
        self.distance_matrix = distance_matrix
        self.population_size = population_size
        self.number_towns = distance_matrix.shape[0]
        self.best_distance = 0

        # population is a collection of permutations
        self.population = []
        for _ in range(self.population_size):
            self.population.append(np.random.permutation(self.number_towns))

        self.population = np.array(self.population)

        # these lists and dictionaries are used in the various phases
        self.probabilities = {}
        self.breeding_list = []
        self.offspring_list = []

    def evaluate(self):
        """ Each permutation of towns has a distance. This distance is 
            calculated and stored in individual distance for each specimen.
            Next, selection_probability() assigns probabilities of selecting
            a specimen for breeding in the next phase (of course, higher
            probability = better fitness = shorter distance). """
        self.probabilities = {}

        individual_distance = []
        total_distance = 0

        for individual in range(self.population_size):
            start = self.population[individual][0]
            route_length = 0
            for next_town in range(1, self.number_towns):
                route_length = route_length + \
                    self.distance_matrix[self.population[individual][next_town-1]][self.population[individual][next_town]]
            route_length = route_length + self.distance_matrix[self.population[individual][self.number_towns-1]][start]
            individual_distance.append(route_length)
            total_distance = total_distance + route_length

        def selection_probability(individual_distance, total_distance):
            normalizing_factor = np.sum(np.exp(- individual_distance / total_distance))
            probability = np.exp(-individual_distance / total_distance) / normalizing_factor
            return probability

        individual_distance = np.array(individual_distance)
        self.best_distance = np.amin(individual_distance)
        probability = selection_probability(individual_distance, total_distance)

        for individual in range(self.population_size):
            self.probabilities[individual] = probability[individual]

    def selection(self):
        """ At this point each individual in the population has a probability.
            These are now used to create a list of parent pairs. These pairs
            will be bred to produce offspring in the next phase. """
        self.breeding_list = []
        for _ in range(self.population_size):
            self.breeding_list.append(np.random.choice(list(self.probabilities.keys()),
                                      size=2, replace=False, p=list(self.probabilities.values())))

    def crossover(self, crossover_method):
        """ Deploy chosen crossover method. """
        if crossover_method == 1:
            self.one_point_crossover()
        else:
            self.two_point_crossover()

    def one_point_crossover(self):
        """ One-point crossover """
        self.offspring_list = []
        for pair in self.breeding_list:
            parent_one = self.population[pair[0]]
            parent_two = self.population[pair[1]]

            crossover_index = np.random.choice(np.arange(1, self.number_towns - 1))
            child_one = parent_one[:crossover_index]
            child_two = parent_two[:crossover_index]

            iterator = 0
            while len(child_one) < len(parent_one):
                if parent_two[iterator] not in child_one:
                    child_one = np.append(child_one, parent_two[iterator])
                iterator = iterator + 1

            iterator = 0
            while len(child_two) < len(parent_two):
                if parent_one[iterator] not in child_two:
                    child_two = np.append(child_two, parent_one[iterator])
                iterator = iterator + 1

            self.offspring_list.append(child_one)
            self.offspring_list.append(child_two)

    def two_point_crossover(self):
        """ Two-point crossover """
        self.offspring_list = []
        for pair in self.breeding_list:
            parent_one = self.population[pair[0]]
            parent_two = self.population[pair[1]]

            from_index, to_index = sorted(np.random.choice(np.arange(1, self.number_towns - 2),
                                                           size=2, replace=False))

            child_one = parent_one[from_index: to_index + 1]
            child_two = parent_two[from_index: to_index + 1]

            for index in range(to_index + 1, len(parent_one)):
                if parent_two[index] not in child_one:
                    child_one = np.append(child_one, parent_two[index])

            for index in range(to_index + 1, len(parent_two)):
                if parent_one[index] not in child_two:
                    child_two = np.append(child_two, parent_one[index])

            prepend_list = []
            for index in range(to_index + 1):
                if parent_two[index] not in child_one:
                    prepend_list.append(parent_two[index])
            prepend_list = np.array(prepend_list[::-1])
            child_one = np.concatenate((prepend_list, child_one))

            prepend_list = []
            for index in range(to_index + 1):
                if parent_one[index] not in child_two:
                    prepend_list.append(parent_one[index])
            prepend_list = np.array(prepend_list[::-1])
            child_two = np.concatenate((prepend_list, child_two))

            self.offspring_list.append(child_one)
            self.offspring_list.append(child_two)

    def mutation(self, mutation_type, mutation_rate):
        """ Deploy chosen mutation method. """
        if mutation_type == 1:
            self.swap_mutation(mutation_rate)
        else:
            self.insert_mutation(mutation_rate)

    def swap_mutation(self, mutation_rate):
        """ Swap mutation - with user-defined probability
            every element can swap places with another element
            in the specimen. """
        for individual in self.offspring_list:
            for swap_from in range(self.number_towns):
                if np.random.uniform(0, 1) < mutation_rate:
                    swap_to = int(np.random.uniform(0, 1) * len(individual))

                    town_one = individual[swap_from]
                    town_two = individual[swap_to]

                    individual[swap_from] = town_two
                    individual[swap_to] = town_one

    def insert_mutation(self, mutation_rate):
        """ Insert mutation - with some user-defined
            probability an element is selected for
            insertion in another place of the specimen. """
        for individual in self.offspring_list:
            for swap_from in range(self.number_towns):
                if np.random.uniform(0, 1) < mutation_rate:
                    swap_to = np.random.choice(np.arange(1, self.number_towns-2))
                    while swap_to == swap_from:
                        swap_to = np.random.choice(np.arange(self.number_towns))
                    swap_from, swap_to = sorted([swap_from, swap_to])
                    individual = np.concatenate((individual[:swap_from],
                                                 individual[swap_from + 1: swap_to],
                                                 [individual[swap_from]],
                                                 individual[swap_to:]))

    def next_generation(self, elitist_rate):
        """ Obtain only best individuals and consider elitism.
            Goal is to keep population size unchanged. """
        sorted_population = [item[0] for item in sorted(self.probabilities.items(),
                                                        key=lambda item: item[1])]
        best_individuals = sorted_population[-int(elitist_rate * self.number_towns)-1:]

        population = []
        for index in best_individuals:
            population.append(self.population[index])

        offspring_indices = np.random.choice(np.arange(len(self.offspring_list)),
                                             size=self.population_size - len(best_individuals), replace=False)
        for offspring_index in offspring_indices:
            population.append(self.offspring_list[offspring_index])

        self.population = np.array(population)

    def solve(self, crossover_method, elitist_rate, mutation_type, mutation_rate):
        """ True solver method. Iterates through generations.
            Involves printing best route's distance up to this generation. """
        for generation in range(101):
            self.evaluate()
            self.selection()
            self.crossover(crossover_method)
            self.mutation(mutation_type, mutation_rate)
            self.next_generation(elitist_rate)

            if generation in [10, 25, 50, 75, 100]:
                print("Generation " + str(generation) +
                      " -> best distance found is: " + str(self.best_distance))


def main():
    """ Main logic here... """

    # Receive user input.
    number_towns = int(input("Enter number of towns: ").strip())

    population_size = int(input("Population size: ").strip())
    crossover_method = int(input("Select crossover method: one-point crossover(1) or two-point crossover(2)? ").strip())
    elitist_rate = float(input("What percentage of a population's best indivudials are kept in the next (0 - 1 range)? ").strip())
    mutation_type = int(input("Select mutation type: swap-mutation(1) or insert-mutation(2)? ").strip())
    mutation_rate = float(input("Select mutation rate (0 - 1 range): ").strip())

    # Numpy creates a number_towns x 2 uniformly distributed matrix of x-y
    # coordinates. Each town's position will conform to a row-vector.
    coordinates_matrix = np.random.uniform(0, 10000, [number_towns, 2])
    distance_matrix = compute_distance_matrix(coordinates_matrix)

    solver = Solver(distance_matrix, population_size)
    solver.solve(crossover_method, elitist_rate, mutation_type, mutation_rate)


if __name__ == "__main__":
    main()
