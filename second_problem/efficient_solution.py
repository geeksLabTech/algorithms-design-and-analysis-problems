
from utils import build_graph, connect_source_and_create_duplicates, Edge
from min_cost_max_flow_algorithm import MinCostMaxFlow

def solve(notes: list[int]):
    edges, adjacents = build_graph(notes)
    source = len(adjacents)
    
    edges, adjacents, duplicates = connect_source_and_create_duplicates(edges, adjacents, source, source+1)
    index_to_start_sinks = source+len(duplicates)+1
    first_sink = index_to_start_sinks
    second_sink = index_to_start_sinks + 1
    third_sink = index_to_start_sinks + 2
    fourth_sink = index_to_start_sinks + 3
    adjacents[first_sink] = []
    adjacents[second_sink] = []
    adjacents[third_sink] = []
    adjacents[fourth_sink] = []

    for i in duplicates:
        e = Edge(origin=i, destiny=first_sink, capacity=1, cost=0, flow=0)
        e2 = Edge(origin=i, destiny=second_sink, capacity=1, cost=0, flow=0)
        e3 = Edge(origin=i, destiny=third_sink, capacity=1, cost=0, flow=0)
        e4 = Edge(origin=i, destiny=fourth_sink, capacity=1, cost=0, flow=0)
        adjacents[i].extend([e, e2, e3, e4])
        edges.extend([e, e2, e3, e4])
        adjacents[first_sink].append(e)
        adjacents[second_sink].append(e2)
        adjacents[third_sink].append(e3)
        adjacents[fourth_sink].append(e4)

    super_sink = index_to_start_sinks + 4
    adjacents[super_sink] = []
    
    edges.append(Edge(origin=first_sink, destiny=super_sink, capacity=1, cost=0, flow=0))
    edges.append(Edge(origin=second_sink, destiny=super_sink, capacity=1, cost=0, flow=0))
    edges.append(Edge(origin=third_sink, destiny=super_sink, capacity=1, cost=0, flow=0))
    edges.append(Edge(origin=fourth_sink, destiny=super_sink, capacity=1, cost=0, flow=0))

    adjacents[first_sink].append(edges[-4])
    adjacents[second_sink].append(edges[-3])
    adjacents[third_sink].append(edges[-2])
    adjacents[fourth_sink].append(edges[-1])
    adjacents[super_sink].extend([edges[-4], edges[-3], edges[-2], edges[-1]])

    # print('inicio', len(adjacents), len(edges))
    mcmf = MinCostMaxFlow(n=len(adjacents), edges=edges, adjacents=adjacents, source=source, sink=super_sink)
    result = mcmf.calc_min_cost_max_flow()
    print(f'max_flow: {result[0]}, min_cost: {result[1]}')
    return result[0], abs(result[1])


# solve([1,3,4,7,8,2])
# solve([12, 38, 13, 41, 2, 39])
solve([9, 37, 31, 17, 9])