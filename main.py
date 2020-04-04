import csv

from graph_allocation import GraphAllocation
from graph_composition import GraphComposition


def main():
    composition_results = {}  # результаты всех компоновок
    c = 0  # счетчик компоновок

    g = GraphComposition('graph.csv')
    constraints = range(3, 8)
    with open('containers.csv') as file:
        s = csv.reader(file, delimiter='\t')
        for config_row in s:
            for i, j in enumerate(config_row):
                config_row[i] = int(j)
            for i in config_row:
                if i not in constraints:
                    wrong_container_len = True
                    break
                else:
                    wrong_container_len = False
            if wrong_container_len:
                continue
            config_row.reverse()
            for n in config_row:
                if len(g.not_viewed_vertices) != n:
                    v = g.get_min_linked_vertex()
                    vertex_set = [v]
                    [vertex_set.append(j) for j in g.not_viewed_vertices if g.graph[v][j]]
                    while len(vertex_set) != n:
                        if len(vertex_set) > n:
                            g.remove_vertex_from_set(vertex_set)
                        else:
                            g.add_vertex_to_set(vertex_set)
                    g.add_to_vertex_sets(vertex_set)
                else:
                    last_set = g.not_viewed_vertices.copy()
                    g.add_to_vertex_sets(last_set)
            g.iterative_solution_improvement()
            composition_results.update({c: {'links': g.calculate_objective_function(), 'composition': g.vertex_sets}})
            c += 1
            g.not_viewed_vertices = g.initial_vertices.copy()
            g.vertex_sets = []
            g.sums_of_external_links.clear()
    get_min_composition(composition_results)

    g = GraphAllocation(g.graph)
    while len(g.viewed_vertices) < len(g.not_viewed_vertices):
        min_k = g.get_K()
        g.discrets.append(min_k)
        g.viewed_vertices.append(min_k)
    g.build_T()
    while True:
        max_L = g.get_L()
        mc = g.v_in_mass_center(max_L)
        dl = []
        for i in mc:
            dl.append(g.delta_L(i, max_L))
        m = dl.index(min(dl))
        if dl[m] < 0:
            mc = mc[m]
            g.swap_T_items(g.T, mc, max_L)
        else:
            get_min_allocation(g)
            break


def get_min_composition(compositions):
    links = [q['links'] for q in compositions.values()]
    min_links = min(links)
    print("min links: ", min_links)
    print("composition: ", compositions[links.index(min_links)]['composition'])


def get_min_allocation(g):
    print("min links: ", g.get_Q())
    print("allocation: ", g.T)


if __name__ == '__main__':
    main()
