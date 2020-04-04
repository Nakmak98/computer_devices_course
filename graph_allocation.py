from graph import Graph


class GraphAllocation(Graph):
    """
    Класс реализует методы для решения задачи размещения
    """

    def __init__(self, vertex_graph):
        super(GraphAllocation, self).__init__()
        # тестовый пример из лекции
        # self.graph = [[0, 0, 0, 3, 0, 0, 2, 3, 0], [0, 0, 2, 0, 2, 0, 0, 0, 0], [0, 2, 0, 1, 0, 0, 0, 0, 0],
        #               [3, 0, 1, 0, 0, 5, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0, 4], [0, 0, 0, 5, 2, 0, 5, 0, 0],
        #               [2, 0, 0, 0, 0, 5, 0, 6, 2], [3, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 4, 0, 2, 0, 0]]
        self.graph = vertex_graph
        self.viewed_vertices = []
        self.not_viewed_vertices = [i for i, j in enumerate(self.graph)]
        self.sums_of_external_links = self.get_rows_sums(self.not_viewed_vertices, self.not_viewed_vertices)
        self.discrets = [0]
        self.x_axis = 3
        self.y_axis = 10
        self.T = []
        self.viewed_vertices.append(0)

    def delta_L(self, v_i, v_j):
        """
        Расчет изменения количества связей при перемещении элементов
        """
        import copy
        t = copy.deepcopy(self.T)
        self.swap_T_items(t, v_i, v_j)
        Li = self.get_q_for_v(v_i, self.graph[v_i], t) / self.sums_of_external_links[v_i]
        Lj = self.get_q_for_v(v_j, self.graph[v_j], t) / self.sums_of_external_links[v_j]
        return (Li - self.L[v_i]) + (Lj - self.L[v_j])

    def swap_T_items(self, t, v_i, v_j):
        m, i = self.find_v_in_T(v_i, t)
        n, j = self.find_v_in_T(v_j, t)
        t[m][i], t[n][j] = t[n][j], t[m][i]

    def v_in_mass_center(self, vertex) -> list:
        from math import ceil
        self.T_rev = self.T.copy()
        self.T_rev.reverse()
        Xc, Yc, mass_center = [], [], []
        for i, val in enumerate(self.graph[vertex]):
            if i != vertex:
                y, x = self.find_v_in_T(i, self.T_rev)
                y += 1
                x += 1
                Xc.append(x * val)
                Yc.append(y * val)
        Xc = sum(Xc) / self.sums_of_external_links[vertex] - 1
        Yc = sum(Yc) / self.sums_of_external_links[vertex] - 1

        Xc = [round(Xc), ceil(Xc)]
        Yc = [round(Yc), ceil(Yc)]

        for i, row in enumerate(self.T_rev):
            for j, val in enumerate(row):
                if i in Yc and j in Xc:
                    mass_center.append(val)
        return mass_center

    def build_T(self):
        for i in range(self.y_axis):
            t = []
            for j in range(self.x_axis):
                t.append(self.discrets[i * self.x_axis + j])
            self.T.append(t)

    def get_Q(self):
        q = []
        viewed_v = []
        for id, row in enumerate(self.graph):
            q.append(self.get_q_for_v(id, row, self.T, viewed_v))
            viewed_v.append(id)
        return sum(q)

    def get_L(self):
        self.L = []
        for id, row in enumerate(self.graph):
            self.L.append(self.get_q_for_v(id, row, self.T) / self.sums_of_external_links[id])
        return self.L.index(max(self.L))

    def get_q_for_v(self, id, row, T, viewed_v=[]):
        q = 0
        n, i = self.find_v_in_T(id, T)
        for k, val in enumerate(row):
            if val and k not in viewed_v:
                m, j = self.find_v_in_T(k, T)
                y = abs(m - n)
                x = abs(i - j)
                q += (y + x) * val
        return q

    def find_v_in_T(self, k, T):
        for i, t in enumerate(T):
            if k in t:
                j = t.index(k)
                return i, j

    def get_K(self):
        """
        Расчет коэффициента связности вершин
        """
        k = []
        placeholder = -1000
        for i, row in enumerate(self.graph):
            allocated = []
            if i in self.viewed_vertices:
                k.append(placeholder)
                continue
            for j, val in enumerate(row):
                if j in self.viewed_vertices:
                    allocated.append(val)
            k.append(2 * sum(allocated) - self.sums_of_external_links[i])
        return k.index(max(k))
