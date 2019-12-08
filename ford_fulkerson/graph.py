def create_graph(matrix):
    graph = []

    # add_grid_points
    for el in generate_list(matrix):
        graph_row = [0] * (len(matrix) ** 2 + 2)
        for e in find_neighbours(matrix, el):
            graph_row[e[0] * len(matrix) + e[1]] = e
        if matrix[el[0]][el[1]]:
            graph_row[len(matrix) ** 2] = "s"
        elif el[0] == 0 or el[1] == 0 or el[0] == len(matrix) - 1 or el[1] == len(matrix) - 1:
            graph_row[len(matrix) ** 2 + 1] = "t"
        graph.append(graph_row)

    # add_starting_points
    graph_row = [0] * (len(matrix) ** 2 + 2)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                graph_row[i * len(matrix) + j] = (i, j)
    graph.append(graph_row)

    # add_boundary_points
    graph_row = [0] * (len(matrix) ** 2 + 2)
    graph.append(graph_row)
    return graph


def generate_list(matrix):
    graph = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            graph.append((i, j))
    return graph


def find_neighbours(matrix, tuple):
    neighbours = []
    if tuple[0] + 1 <= len(matrix) - 1:
        neighbours.append((tuple[0] + 1, tuple[1]))
    if tuple[1] + 1 <= len(matrix) - 1:
        neighbours.append((tuple[0], tuple[1] + 1))
    if tuple[0] - 1 >= 0:
        neighbours.append((tuple[0] - 1, tuple[1]))
    if tuple[1] - 1 >= 0:
        neighbours.append((tuple[0], tuple[1] - 1))
    return neighbours


def add_capacities(matrix):
    g = create_graph(matrix)
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] == "s":
                g[i][j] = 0
            elif g[i][j]:
                g[i][j] = 1
    return g


from collections import defaultdict


class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)

    '''Returns true if there is a path from source 's' to sink 't' in 
    residual graph. Also fills parent[] to store the path '''

    def BFS(self, s, t, parent):
        visited = [False] * (self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    def FordFulkerson(self, source, sink, length):
        lst = []
        parent = [-1] * (self.ROW)
        max_flow = 0
        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow += path_flow
            v = sink
            parent_queue = []
            while (v != source):
                u = parent[v]
                if parent[v] != source:
                    parent_queue.append(u)
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
            parent_queue.reverse()
            coordinatesQueue = convert_path_to_coordinates(parent_queue, length)
            lst.append(coordinatesQueue)
        return max_flow, lst


def get_coordinates(num, matrix_size):
    return (num // matrix_size, num % matrix_size)


def convert_path_to_coordinates(parentQueue, matrix_size):
    coordinatesQueue = []
    for item in parentQueue:
        coordinatesQueue.append(get_coordinates(item, matrix_size))
    return coordinatesQueue


def escape_problem(matrix):
    graph_with_capacities = add_capacities(matrix)
    gr = Graph(graph_with_capacities)
    max_flow_graph = gr.FordFulkerson(len(matrix) ** 2, len(matrix) ** 2 + 1, len(matrix))
    return max_flow_graph[1]


matric = [[0, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
print(escape_problem(matric))


