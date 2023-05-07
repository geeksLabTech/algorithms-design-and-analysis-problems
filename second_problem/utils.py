import json

import math
import heapq
import select

BIG_INT: int = 1000000000000000


def load_json(json_name):
    data = {}

    with open(json_name) as file:
        data = json.load(file)

    return data
def is_difference_one(x: int, y: int):
    return abs(x - y) == 1


def are_congruent(x: int, y: int, modulo: int):
    return x % modulo == y % modulo


def is_adyacent_valid(x: int, y: int, modulo: int):
    return is_difference_one(x, y) or are_congruent(x, y, modulo)


class Edge:
    def __init__(self, origin: int, destiny: int, capacity: int, cost: int, flow: int = 0):
        self.origin = origin
        self.destiny = destiny
        self.c = capacity
        self._cost = cost
        self.flow = 0
    
    def capacity(self, u: int):
        if u == self.origin:
            return self.c - self.flow
        else:
            return self.flow

    def add_flow(self, u: int, f: int):
        if u == self.origin:
            self.flow += f
        else:
            self.flow -= f

    def exist(self, u: int):
        return self.capacity(u) != 0
    
    def get_other_endpoint(self, u: int):
        return self.destiny if u == self.origin else self.origin

    def get_cost(self, u: int):
        return self._cost if u == self.origin else -self._cost

def build_graph(notes: list[int]):
    adjacents: dict[int, list[Edge]] = {}
    edges: list[Edge] = []

    for i in range(len(notes)):
        adjacents[i] = []
        for j in range(i+1, len(notes)):
            if not j in adjacents:
                adjacents[j] = []

            if is_adyacent_valid(notes[i], notes[j], 7):
                e = Edge(origin=i, destiny=j, capacity=1, cost=-1, flow=0)
                adjacents[i].append(e)
                adjacents[j].append(e)
                edges.append(e)

    return edges, adjacents

def connect_source_and_create_duplicates(edges: list[Edge], adjacents: dict[int, list[Edge]], source: int, index_to_start_duplicates: int):
    adjacents[source] = []
    # adjacents[sink] = []
    duplicates: list[int] = []
    for i in range(source):
        if i != source:
            e = Edge(origin=source, destiny=i, capacity=1, cost=-1, flow=0)
            adjacents[source].append(e)
            adjacents[i].append(e)
            edges.append(e)

            duplicate_edge = Edge(origin=i, destiny=index_to_start_duplicates, capacity=1, cost=0, flow=0)
            adjacents[index_to_start_duplicates] = [duplicate_edge]
            adjacents[i].append(duplicate_edge)
            edges.append(duplicate_edge)
            duplicates.append(index_to_start_duplicates)
            index_to_start_duplicates+=1

    return edges, adjacents, duplicates



def bellman_ford(n: int, edges: list[Edge], source: int, sink: int) -> tuple[bool, list[int]]: 
    dist = [BIG_INT] * n
    dist[source] = 0 
    for i in range(n):
        for e in edges:
            # Relax step
            dist[e.destiny] = min(dist[e.destiny], dist[e.origin] + e._cost)
    
    if dist[sink] >= BIG_INT:
        return False, dist
     
    print('belman ds', dist)
    return True, dist


def dijkstra(n: int, adjacents: dict[int, list[Edge]], source: int, sink: int) -> tuple[bool, list[int]]:
    dist = [BIG_INT] * n
    processed = [False] * n

    dist[source] = 0
    Q = []
    heapq.heappush(Q, (0, source))

    while len(Q) > 0:
        _, u = heapq.heappop(Q)
        if processed[u]:
            continue

        processed[u] = True
        for e in adjacents[u]:
            if not e.exist(u):
                continue

            v = e.get_other_endpoint(u)
            if dist[v] > dist[u] + e.get_cost(u):
                dist[v] = dist[u] + e.get_cost(u)
                heapq.heappush(Q, (dist[v], v))

    if dist[sink] >= BIG_INT:
        return False, dist
    
    return True, dist
