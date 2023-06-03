

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

    def __eq__(self, __value: Self) -> bool:
        return self.id == __value.id
    
    def __hash__(self) -> int:
        return hash(self.id)
