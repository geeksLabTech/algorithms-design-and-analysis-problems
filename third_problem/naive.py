from utils import Node, Student, add_node_to_solution, remove_node_from_solution


best_k: int = 0
best_combination: list[int] = []


def backtrack(
    k: int,
    current_nodes: list[Node],
    mask: list[bool],
    dependencies: dict[int, list[Node]],
):
    if len(current_nodes) > k:
        return

    global best_k
    global best_combination
    # print(f'len current', len(current_nodes), k)
    if (
        len(current_nodes) <= k
        and len(current_nodes) > 0
        and len(current_nodes) > best_k
    ):
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
            current_nodes, mask, dependencies = add_node_to_solution(
                n, current_nodes, mask, dependencies
            )
            backtrack(k, current_nodes, mask, dependencies)
            current_nodes, mask, dependencies = remove_node_from_solution(
                n, current_nodes, mask, dependencies
            )


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
    print(f"best_k: {results[0]}, best_combination: {results[1]}")
    return results
