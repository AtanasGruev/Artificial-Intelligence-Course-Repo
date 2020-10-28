class Node:
    """Node information - parent, neighbours, cost"""
    def __init__(self, id):
        self._id = id
        self._parent = None
        self._neighbours = {}
        self._g = 0
        self._h = 0
        self._f = 0

    def __eq__(self, other):
        return self._id == other._id

    def __lt__(self, other):
        return self._f < other._f

    def set_parent(self, parent_node):
        self._parent = parent_node

    def add_neighbour(self, neighbour, weight):
        self._neighbours[neighbours] = weight

    def get_neighbours(self):
        return self._neighbours

    def get_weight(self, neighbour):
        return self._neighbour[neighbour]

class Graph:
    """Simple graph - supports adding nodes & edges"""
    def __init__(self):
        self._dict = {}

    def __iter__(self):
        return iter(self._dict.values())

    def add_node(self, node):
        dict_node = Node(node)
        self._dict[node] = dict_node

    def get_node(self, node):
        if node in self._dict:
            return self._dict[node]
        else:
            return None

    def 
