

from typing import Self


class Student:
    def __init__(self, id: int, opinions: list[int]) -> None:
        self.id = id 
        self.opinions = opinions
        

class Edge:
    def __init__(self, source: 'Node', dest: 'Node', is_negative: bool) -> None:
        self.source = source
        self.dest = dest
        self.is_negative = is_negative
        self.pheromone: float = 0.0

class Node:
    def __init__(self, id: int, total_nodes_ids) -> None:
        self.id = id 
        self.total_nodes_ids: set[int] = total_nodes_ids
        self.edges: list[Edge] = []
    

    def add_edge(self, target_node: Self, is_negative: bool):
        edge = Edge(self, target_node, is_negative)
        self.edges.append(edge)
        target_node.edges.append(edge)


    def add_neutral_edges(self, total_nodes: list[Self]):
        used_ids = [e.dest.id for e in self.edges if e.source == self]
        target_nodes = [node for node in total_nodes if node.id != self.id and not node.id in used_ids]
        for node in target_nodes:
            self.add_edge(node, False)


    def get_negative_incoming_edges(self):
        return [e for e in self.edges if e.source != self and e.is_negative]
    

    def get_adjecent_nodes(self):
        return [e.dest for e in self.edges if e.source == self]
    
    def get_negative_adjacent_nodes(self):
        return [e.dest for e in self.edges if e.source == self and e.is_negative]

    
    def get_outgoing_edges(self):
        return [e for e in self.edges if e.dest != self]


    def __eq__(self, __value: Self) -> bool:
        return self.id == __value.id
    
    def __hash__(self) -> int:
        return hash(self.id)


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