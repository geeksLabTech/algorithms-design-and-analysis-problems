
from utils import Node, Student
    

best_k: int = 0
best_combination: list[int] = []


def add_node_to_solution(node: Node, current_nodes: list[Node], mask: list[bool], dependencies: dict[int, list[Node]]):
    nodes_to_process: list[Node] = []
    nodes_to_process.append(node)
    while len(nodes_to_process) > 0:
        # print(len(nodes_to_process))
        current = nodes_to_process.pop()
        if mask[current.id]:
            continue

        mask[current.id] = True 
        current_nodes.append(current)
        # edges_for_print = [(e.source.id, e.dest.id, e.is_negative) for e in current.edges]
        # print('look edges: ',  edges_for_print)
        nodes_that_think_negative = [e.source for e in current.edges if e.dest == current and e.is_negative]
        dependencies[current.id] = nodes_that_think_negative
        nodes_to_process.extend(nodes_that_think_negative)

    return current_nodes, mask, dependencies


def remove_node_from_solution(node: Node, current_nodes: list[Node], mask: list[bool], dependencies: dict[int, list[Node]]):
    nodes_to_process: list[Node] = []
    nodes_to_process.append(node)
    while len(nodes_to_process) > 0:
        current = nodes_to_process.pop()
        # if not mask[current.id]:
        #     continue

        mask[current.id] = False 
        nodes_to_remove = dependencies[current.id]
        nodes_to_remove.extend(current.get_negative_adjacent_nodes())
        nodes_to_process.extend(nodes_to_remove)
        dependencies[current.id] = []
        current_nodes.remove(current)
    
    return current_nodes, mask, dependencies


def backtrack(k: int, current_nodes: list[Node], mask: list[bool], dependencies: dict[int, list[Node]]):
    if len(current_nodes) > k:
        return 
    
    global best_k
    global best_combination
    # print(f'len current', len(current_nodes), k)
    if len(current_nodes) <= k and len(current_nodes) > 0 and len(current_nodes) > best_k:
        best_k = len(current_nodes)
        best_combination = [node.id for node in current_nodes]

    if best_k == k:
        return

    # Get all adjacents
    all_adjacents = set()
    for n in current_nodes:
        all_adjacents.union(n.get_adjecent_nodes())
    
    for n in all_adjacents:
        if not mask[n.id]: 
            current_nodes, mask, dependencies = add_node_to_solution(n, current_nodes, mask, dependencies)
            backtrack(k, current_nodes, mask, dependencies)
            current_nodes, mask, dependencies = remove_node_from_solution(n, current_nodes, mask, dependencies)


def brute_force(nodes: list[Node], k: int):
    global best_k
    global best_combination
    best_k = 0
    best_combination = []
    mask = [False] * len(nodes)
    for i in nodes:
        mask = [False] * len(nodes)
        starting_nodes, mask, dependencies = add_node_to_solution(i, [], mask, {})
        # Starting nodes exceed k, backtrack not needed
        if len(starting_nodes) > k:
            continue

        backtrack(k, starting_nodes, mask, dependencies)

        if best_k == k:
            break

    return best_k, best_combination


def solve(students: list[Student], k: int):
    total_nodes_ids = set(s.id for s in students)
    nodes = [Node(s.id, total_nodes_ids) for s in students]

    # Add_negative_edges_to_nodes
    for i in range(len(nodes)):
        for j in range(len(students[i].opinions)):
            # target_node = nodes[students[i].opinions[j]]
            nodes[i].add_edge(nodes[students[i].opinions[j]], True)

    # Add_neutral_edges_to_nodes
    for node in nodes:
        node.add_neutral_edges(nodes)

    results = brute_force(nodes, k)
    print(f'best_k: {results[0]}, best_combination: {results[1]}')
    return results

