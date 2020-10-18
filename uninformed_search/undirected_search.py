from collections import deque  # collections.deque for bfs, dfs
from heapq import heappush, heappop  # heapq for ucs
from undirected_graph import UndirectedWeightedGraph


def bfs_undirected(graph, start):
    """ Breadh-First Search """
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        visited.add(node)
        print('Node: ' + str(node))
        for edge_tuple in graph.list_neighbours(node):
            if edge_tuple[1] not in visited:
                queue.append(edge_tuple[1])
                visited.add(edge_tuple[1])


def dfs_undirected_recursive_wrapper(graph, start):
    """ Depth-First Search (wrapper)"""
    visited = set()
    dfs_undirected_recursive(graph, start, visited)


def dfs_undirected_recursive(graph, start, visited):
    """ Depth-First Search (recursive) """
    visited.add(start)
    for edge_tuple in graph.list_neighbours(start):
        if edge_tuple[1] not in visited:
            dfs_undirected_recursive(graph, edge_tuple[1], visited)
    print('Node: ' + start)


def dfs_undirected_iterative(graph, start):
    """Depth-First Search (iterative)"""
    print_order = []
    visited = set()
    stack = deque([start])
    while stack:
        node = stack.pop()
        if node not in visited:
            print_order.append(node)
            visited.add(node)
        for edge_tuple in graph.list_neighbours(node):
            if edge_tuple[1] not in visited:
                stack.append(edge_tuple[1])
    for node in print_order[::-1]:
        print('Node:' + str(node))


def ucs_undirected(graph, start, goal):
    """ In order to find the shortest path,
        we delete nodes and edges from the graph. """
    node_cost_dict = {}  # acts as visited list & keeps current path costs
    node_cost_dict[start] = 0
    node_pred_dict = {}  # preserves a 'best' predecessor in terms of weight
    priority_queue = [(0, start)]
    pq_visited = []  # easier check whether an edge should be deleted
    while priority_queue:
        node = heappop(priority_queue)[1]
        pq_visited.append(node)
        if node == goal:
            return node_cost_dict
        for edge_tuple in graph.list_neighbours(node):
            # # UNCOMMENT FOR PROBLEM OBSERVATION
            # print(graph.list_neighbours(node))
            # print('Node:' + str(node) + ' ->' + str(edge_tuple[1]))

            # # NOTICE THE PROBLEM ONLY CONCERNS THE PATH TO THE
            # # SOLUTION. OTHERWISE THE IMPLEMENTATION CORRECTLY
            # # FINDS OPTIMAL COST VALUE FROM S TO G.
            if edge_tuple[1] not in node_cost_dict:
                heappush(priority_queue,
                         tuple((node_cost_dict[node] + edge_tuple[0],
                                edge_tuple[1])))
                node_cost_dict[edge_tuple[1]] = node_cost_dict[node] + \
                    edge_tuple[0]
                node_pred_dict[edge_tuple[1]] = node
            else:
                if node_cost_dict[edge_tuple[1]] > node_cost_dict[node] + \
                                                            edge_tuple[0]:
                    node_cost_dict[edge_tuple[1]] = node_cost_dict[node] + \
                                                            edge_tuple[0]
                    graph.remove_edge(edge_tuple[1],
                                      node_pred_dict[edge_tuple[1]])
                    node_pred_dict[edge_tuple[1]] = node
                else:
                    if edge_tuple[1] not in pq_visited:
                        graph.remove_edge(node, edge_tuple[1])
        # After deleting the unnecessary edges we are left with a tree.
        # Now we delete all leaves which don't lead to a solution.
    return 'No path found!'


def dls_recursive_undirected_wrapper(graph, start, goal_list, depth):
    """ Depth-Limited Search (wrapper)"""
    visited = set()
    return dls_recursive_undirected(graph, start, goal_list, depth, visited)


def dls_recursive_undirected(graph, start, goal_list, depth, visited):
    """ Depth-Limited Search (recursive) """
    if depth == 0:
        print(start)
        return start in goal_list
    else:
        visited.add(start)
        for edge_tuple in graph.list_neighbours(start):
            if edge_tuple[1] not in visited:
                if dls_recursive_undirected(graph, edge_tuple[1],
                                            goal_list, depth-1, visited):
                    return True
        print(start)
        return False


def ids_undirected(graph, start, goal_list):
    """ Iterative-Deepening Search emplots DLS """
    depth = 0
    while True:
        print('\nNEXT ITERATION with depth: ' + str(depth) + '\n')
        if dls_recursive_undirected_wrapper(graph, start, goal_list, depth):
            break
        else:
            depth += 1
    print('Depth reached until solution found --> ' + str(depth))


def main():
    """Playground for graph traversal algorithms"""
    graph_dict = {'A': [(1, 'B'), (1, 'S')],
                  'B': [(1, 'A')],
                  'S': [(1, 'A'), (1, 'C'), (1, 'G')],
                  'C': [(1, 'S'), (1, 'D'), (1, 'E'), (1, 'F')],
                  'G': [(1, 'S'), (1, 'F'), (1, 'H')],
                  'D': [(1, 'C')],
                  'E': [(1, 'C'), (1, 'H')],
                  'F': [(1, 'C'), (1, 'G')],
                  'H': [(1, 'E'), (1, 'G')]
                  }
    graph = UndirectedWeightedGraph(graph_dict)
    print(graph)
    graph.remove_edge('C', 'F')
    print(graph)
    bfs_undirected(graph, next(iter(graph_dict)))
    print('-'*20)
    dfs_undirected_recursive_wrapper(graph, next(iter(graph_dict)))
    print('-'*20)
    dfs_undirected_iterative(graph, next(iter(graph_dict)))
    print('-'*20)

    new_graph_dict = {'S': [(7, 'A'), (9, 'B'), (14, 'C')],
                      'A': [(7, 'S'), (10, 'B'), (15, 'D')],
                      'B': [(9, 'S'), (10, 'A'), (2, 'C'), (11, 'D')],
                      'C': [(14, 'S'), (2, 'B'), (9, 'G')],
                      'D': [(15, 'A'), (11, 'B'), (6, 'G')],
                      'G': [(9, 'C'), (6, 'D')]}

    new_graph = UndirectedWeightedGraph(new_graph_dict)
    print(new_graph)
    print(ucs_undirected(new_graph, 'S', 'G'))
    print(new_graph)  # Need to 'cut' non-goal leaves

    print('-'*20)
    print(graph)
    print(bool(dls_recursive_undirected_wrapper(graph, 'A', ['F'], 3)))
    print('-'*20)
    print(graph)
    ids_undirected(graph, 'A', ['F', 'E'])


if __name__ == "__main__":
    main()
