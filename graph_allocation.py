class GraphAllocation:
    def __init__(self, vertex_graph, sets):
        # self.graph = self.get_adjacency_matrix(vertex_graph, sets)
        # тестовый пример из лекции
        self.graph = [[0, 0, 0, 3, 0, 0, 2, 3, 0], [0, 0, 2, 0, 2, 0, 0, 0, 0], [0, 2, 0, 1, 0, 0, 0, 0, 0],
                      [3, 0, 1, 0, 0, 5, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0, 4], [0, 0, 0, 5, 2, 0, 5, 0, 0],
                      [2, 0, 0, 0, 0, 5, 0, 6, 2], [3, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 4, 0, 2, 0, 0]]

    @staticmethod
    def get_adjacency_matrix(graph, sets):
        # возвращает матрицу смежности из скомпонованных в контейнеры элементов
        adjacency_graph = [[0 for x in sets] for y in sets]
        for set_i_id, set_i in enumerate(sets):
            for set_j_id, set_j in enumerate(sets):
                if set_i != set_j:
                    s = 0
                    for i in set_i:
                        for id, val in enumerate(graph[i]):
                            if id in set_j:
                                s += graph[i][id]
                        adjacency_graph[set_i_id][set_j_id] = s

    def rows_sum(self):
        self.sum_of_rows = []

        pass
