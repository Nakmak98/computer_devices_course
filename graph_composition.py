import csv


class GraphComposition:
    """
    Класс реализует методы для решения задачи компоновки
    """

    def __init__(self, path_to_file):
        self.graph = self.read_graph(path_to_file)
        self.vertex_sets = []
        self.not_viewed_vertices = [i for i, j in enumerate(self.graph)]
        self.initial_vertices = self.not_viewed_vertices.copy()
        self.sums_of_external_links = []
        self.not_viewed_sets = []
        self.Q = {}

    @staticmethod
    def read_graph(path_to_file: str) -> list:
        """
        Читает матрицу смежности из файла в массив
        """
        with open(path_to_file, newline='') as graph_file:
            file = csv.reader(graph_file, delimiter='\t')
            matrix = []
            for row in file:
                for j, col in enumerate(row):
                    row[j] = int(col)
                matrix.append(row)
            return matrix

    def get_min_linked_vertex(self) -> int:
        """
        Возвращает индекс вершины с минимальным количеством внешних связей
        """
        self.sums_of_external_links = self.get_rows_sums(self.not_viewed_vertices, self.not_viewed_vertices)
        min_el = min(self.sums_of_external_links)
        candidates = []
        for v, s in enumerate(self.sums_of_external_links):
            if s <= min_el:
                candidates.append(v)
        if len(candidates) > 1:
            count_list = []
            for i in candidates:
                count = 0
                for j in self.not_viewed_vertices:
                    if self.graph[i][j]:
                        count += 1
                count_list.append(count)
            return candidates[count_list.index(min(count_list))]
        else:
            return candidates[0]

    def get_rows_sums(self, vertex_rows, vertex_cols, find='min') -> list:
        """
        Возвращает список сумм vertex_cols по vertex_rows.
        В общем случае список имеет пустые элементы, которые заполняются placeholder
        для возможности нахождения максимального или минимального элемента списка
        """
        placeholder = 1000
        if find == 'max':
            placeholder = -1
        rows_sum = [placeholder for i in range(len(self.graph))]
        for row in vertex_rows:
            row_sum = 0
            for col in vertex_cols:
                row_sum += self.graph[row][col]
            rows_sum[row] = row_sum
        return rows_sum

    def remove_vertex_from_set(self, vertices: list) -> None:
        """
        Удаление вершин из множества с помощью расчета дельта-функции
        """
        s = self.get_rows_sums(vertices, vertices)
        deltas = [(self.sums_of_external_links[v] - s[v]) for v in vertices]
        vertices.pop(deltas.index(max(deltas)))

    def add_to_vertex_sets(self, vertex_set: list):
        """
        Добавление нового множества в список сформированных множеств
        и удаляет элементы нового множества из списка просмотренных вершин
        """
        self.vertex_sets.append(vertex_set)
        for v in vertex_set:
            self.not_viewed_vertices.pop(self.not_viewed_vertices.index(v))

    def add_vertex_to_set(self, vertex_set: list) -> None:
        """
        Добавление вершины к неполному множеству
        """
        intended_vertices = self.get_intended_vertices(vertex_set)
        links_with_vertex_set = self.get_rows_sums(intended_vertices, vertex_set, 'max')
        vertex_set.append(links_with_vertex_set.index(max(links_with_vertex_set)))

    def get_intended_vertices(self, vertex_set: list) -> list:
        """
        Возвращает список инцидентных к вершинам из vertex_set вершин
        """
        intended_vertices = []
        for i in vertex_set:
            for j, val in enumerate(self.graph[i]):
                if val and (j in self.not_viewed_vertices and j not in vertex_set):
                    if j not in intended_vertices:
                        intended_vertices.append(j)
        return intended_vertices

    def iterative_solution_improvement(self):
        """
        Алгоритм итерационного улучшения решения
        :return:
        """
        from uuid import uuid1
        #self.vertex_sets = [[0, 1], [2, 3, 4], [5, 6, 7]] # для тестирования на примере из лекции
        self.not_viewed_sets = self.vertex_sets.copy()

        while len(self.not_viewed_sets) > 1:
            while self.calculate_r_function():
                pass
            self.not_viewed_sets.pop(0)


    def calculate_objective_function(self) -> int:
        """
        Вычисление целевой функции
        """
        q = 0
        veiwed_sets = []
        for v_set in self.vertex_sets:
            veiwed_sets.append(v_set)
            for i in v_set:
                for j, val in enumerate(self.graph[i]):
                    for k in veiwed_sets:
                        if j in k:
                            in_set = True
                            break
                        else:
                            in_set = False
                    if not in_set:
                        q += self.graph[i][j]
        return q

    def calculate_r_function(self) -> bool:
        """
        Вычисление разницы внешних свзяей при перестановках вершин из разных множеств
        Возвращает True, если был найден положительный элемент в матрице R
        """

        # формирование строк и столбцов матрицы R
        r_rows_set = self.not_viewed_sets[0]
        r_col_sets = []
        for v_set in self.not_viewed_sets[1:len(self.vertex_sets)]:
            r_col_sets.append(v_set)

        delta_r = {}
        for row in r_rows_set:
            delta_r.update({row: {}})
            for col_set in r_col_sets:
                for col in col_set:
                    s1 = self.set_in_row_sum(row, col_set) - self.set_in_row_sum(row, r_rows_set)
                    s2 = self.set_in_row_sum(col, r_rows_set) - self.set_in_row_sum(col, col_set)
                    r = s1 + s2 - 2 * self.graph[row][col]
                    delta_r[row].update({col: r})
        m = self.get_max_r(delta_r)
        if m[2] <= 0:
            return False
        r_rows_set[r_rows_set.index(m[0])] = m[1]
        for c_set in r_col_sets:
            if m[1] in c_set:
                c_set[c_set.index(m[1])] = m[0]
        return True

    def get_max_r(self, delta_r: dict) -> list:
        max_item = [0, 0, 0]
        for row in delta_r:
            for col, value in delta_r[row].items():
                if max_item[2] < value:
                    max_item[0] = row
                    max_item[1] = col
                    max_item[2] = value
        return max_item

    def set_in_row_sum(self, row: int, v_set: list) -> int:
        set_sum = 0
        for item in v_set:
            set_sum += self.graph[row][item]
        return set_sum


