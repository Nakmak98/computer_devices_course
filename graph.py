class Graph():
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
