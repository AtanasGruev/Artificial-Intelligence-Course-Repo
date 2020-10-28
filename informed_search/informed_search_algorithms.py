from heapq import heappush, heappop


def greedy_best_first_search(graph, heuristic, start, goal):
    """ Greedy best-first strategy. """
    fringe = [(heuristic[start], start)]
    visited = set()
    path = []
    while fringe:
        node = heappop(fringe)[1]
        path.append(node)
        if node == goal:
            return path
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour[1] not in visited:
                child = tuple((heuristic[neighbour[1]], neighbour[1]))
                heappush(fringe, child)


def a_star_search(graph, heuristic, start, goals):
    """A-star search. Optimizations due. """
    f_cost_dict = {}
    f_cost_dict[start] = heuristic[start]
    g_cost_dict = {}
    g_cost_dict[start] = 0
    pred_dict = {}
    pred_dict[start] = None
    fringe = [(f_cost_dict[start], start)]
    visited = set()
    while fringe:
        node = heappop(fringe)[1]
        if node in goals:
            pred_list = [(node, f_cost_dict[node])]
            current = pred_dict[node]
            while current is not None:
                pred_list.append((current, f_cost_dict[current]))
                current = pred_dict[current]
            return pred_list[::-1]
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour[1] not in visited:
                g_cost_dict[neighbour[1]] = g_cost_dict[node] + neighbour[0]
                f_cost_dict[neighbour[1]] = g_cost_dict[neighbour[1]] + \
                    heuristic[neighbour[1]]
                heappush(fringe, tuple((f_cost_dict[neighbour[1]], neighbour[1])))
                pred_dict[neighbour[1]] = node

def main():
    """ Main method """
    graph_dict = {'S': [(2, 'A'), (3, 'B'), (3, 'Z')],
                  'A': [(2, 'S'), (4, 'C')],
                  'B': [(3, 'S'), (2, 'D')],
                  'C': [(4, 'A'), (4, 'G')],
                  'D': [(2, 'B'), (3, 'H'), (3, 'I'), (2, 'E')],
                  'E': [(2, 'D'), (3, 'F'), (2, 'J')],
                  'F': [(3, 'E'), (3, 'G')],
                  'G': [(4, 'C'), (3, 'F')],
                  'H': [(3, 'D')],
                  'I': [(3, 'D')],
                  'J': [(2, 'E'), (2, 'K')],
                  'K': [(2, 'J')],
                  'Z': [(3, 'S')]}
    heuristic = {'S': 8, 'A': 7, 'B': 5, 'C': 4, 'D': 6, 'E': 6, 'F': 3,
                 'G': 0, 'H': 9, 'I': 8, 'J': 7, 'K': 8, 'Z': 11}

    print(greedy_best_first_search(graph_dict, heuristic, 'S', 'G'))
    print(a_star_search(graph_dict, heuristic, 'S', ['G']))

    new_graph_dict = {'S': [(5, 'A'), (9, 'B'), (6, 'D')],
                      'A': [(3, 'B'), (9, 'G1')],
                      'B': [(2, 'A'), (1, 'C')],
                      'C': [(6, 'S'), (5, 'G2'), (7, 'F')],
                      'D': [(1, 'S'), (2, 'C'), (2, 'E')],
                      'E': [(7, 'G3')],
                      'F': [(8, 'G3')],
                      'G1': [],
                      'G2': [],
                      'G3': []}
    new_heuristic = {'S': 5, 'A': 7, 'B': 3, 'C': 4, 'D': 6, 'E': 5, 'F': 6,
                     'G1': 0, 'G2': 0, 'G3': 0}

    print(greedy_best_first_search(new_graph_dict, new_heuristic, 'S', 'G2'))
    print(a_star_search(new_graph_dict, new_heuristic, 'S', ['G1', 'G2', 'G3']))


if __name__ == '__main__':
    main()
