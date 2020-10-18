class UndirectedWeightedGraph(object):
    """ A simple Python Graph class (undirected, weighted) """

    def __init__(self, graph_dict=None):
        """ If a dict is given, it's used in initialization.
            Otherwise the graph is constructed with a []. """
        if graph_dict is None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def list_nodes(self):
        """ Nodes listing. """
        return list(self.__graph_dict.keys())

    def list_neighbours(self, node):
        return self.__graph_dict[node]

    def list_edges(self):
        """ Edges listing, weight is not displayed. """
        return self.__generate_edges(False)

    def list_edges_weighted(self):
        """ Edges listing, weight displayed. """
        return self.__generate_edges(True)

    def __generate_edges(self, weighted):
        """ Returns a list ot edges (also lists), depending on the 
            'weighted' flag. Pretty self explanatory really. """
        edges = []
        for node in self.__graph_dict:
            for neighbour_tuple in self.__graph_dict[node]:
                if weighted is True:
                    edges.append([node, neighbour_tuple[0], neighbour_tuple[1]])
                else:
                    edges.append([node, neighbour_tuple[0]])
        return edges

    def add_node(self, node):
        """ Addition of a single vertex """
        if node not in self.__graph_dict:
            self.__graph_dict[node] = []

    def add_edge(self, edge):
        """ Addition of a single edge """
        (node1, node2, weight) = tuple(edge)
        for node in [node1, node2]:
            if node not in self.__graph_dict:
                self.__graph_dict[node] = []
        self.__graph_dict[node1].append((weight. node2))
        self.__graph_dict[node2].append((weight, node1))

    def remove_node(self, node):
        """ Removal of nodes.
            If a node is removed, all associated
            edges are also removed! """
        try:
            del self.__graph_dict[node]
            for item in self.__graph_dict:
                for edge_tuple in self.__graph_dict[item]:
                    if edge_tuple[1] == node:
                        self.__graph_dict[item].remove(edge_tuple)
        except KeyError:
            print('Node specified not found in graph!')

    def __is_edge(self, node1, node2):
        try:
            for edge_tuple in self.__graph_dict[node1]:
                if edge_tuple[1] == node2:
                    return True
            return False
        except KeyError:
            print('One or both of the nodes specified not found in graph!')

    def remove_edge(self, node1, node2):
        """ Removes edges given two nodes. """
        if self.__is_edge(node1, node2):
            for edge_tuple in self.__graph_dict[node1]:
                if edge_tuple[1] == node2:
                    self.__graph_dict[node1].remove(edge_tuple)
            for edge_tuple in self.__graph_dict[node2]:
                if edge_tuple[1] == node1:
                    self.__graph_dict[node2].remove(edge_tuple)

    def __edges_to_printable(self, edge_tuple):
        return '(' + "".join(map(lambda expr: str(expr) + " ", edge_tuple))[:-1] + ')'

    def __str__(self):
        return_string = ""
        if bool(self.__graph_dict):
            for node in self.__graph_dict:
                return_string += str(node) + ': ['
                for edge in self.__graph_dict[node]:
                    return_string += self.__edges_to_printable(edge)
                    return_string += ', '
                if self.__graph_dict[node]:
                    return_string = return_string[:-2]
                return_string += ']\n'
        return return_string
