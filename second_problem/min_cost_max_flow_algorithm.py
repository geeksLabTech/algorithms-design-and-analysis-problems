import math
from collections import deque
from utils import Edge, BIG_INT, bellman_ford, dijkstra


class MinCostMaxFlow:
    def __init__(self, n: int, source: int, sink: int, adjacents: dict[int, list[Edge]], edges: list[Edge]):
        self.n = n
        self.source: int = source
        self.sink: int = sink
        self.adjacents: dict[int, list[Edge]] = adjacents
        self.edges: list[Edge] = edges
        self.flow: list[int] = []
        self.sink_potential: int = 0
        # At current DAG
        self.dist_from_source: list[int] = []


    def is_in_current_dag(self, u: int, v: int):
        return self.dist_from_source[v] == self.dist_from_source[u] + 1;


    def apply_potentials_to_edges(self, distances: list[int]):
        for e in self.edges:
            if distances[e.origin] >= BIG_INT or distances[e.destiny] >= BIG_INT:
                continue

            e._cost += distances[e.origin] - distances[e.destiny]

        self.sink_potential += distances[self.sink]


    def dinitz_bfs(self):
        # A value greater than n denote "unexplored"
        self.dist_from_source = [self.n+10] * self.n
        Q: deque[int] = deque()
        Q.append(self.source)
        self.dist_from_source[self.source] = 0

        while len(Q) > 0:
            u = Q.popleft()
            for e in self.adjacents[u]:
                if not e.exist(u) or e.get_cost(u) != 0:
                    continue

                v = e.get_other_endpoint(u)
                
                if self.dist_from_source[v] > self.n:
                    self.dist_from_source[v] = self.dist_from_source[u] + 1
                    Q.append(v)


    def __dinitz_dfs(self, u: int, flow: int, blocked: list[bool]) -> tuple[int, list[bool]]:
        if u == self.sink:
            return flow, blocked

        flow_pushed = 0
        all_blocked = True
        for e in self.adjacents[u]:
            v = e.get_other_endpoint(u)
            if not self.is_in_current_dag(u, v):    
                continue
                
            if e.exist(u) and not blocked[v] and e.get_cost(u) == 0:
                flow_to_push, blocked = self.__dinitz_dfs(v, min(flow, e.capacity(u)), blocked)
                flow_pushed += flow_to_push
                flow -= flow_to_push
                e.add_flow(u, flow_to_push)
               
            if e.exist(u) and not blocked[v] and e.get_cost(u) == 0:
                all_blocked = False

        if all_blocked:
            blocked[u] = True
            
        return flow_pushed, blocked
    

    def dinitz_dfs(self):
        blocked = [False] * self.n
        return self.__dinitz_dfs(self.source, BIG_INT, blocked)[0]

    
    def calc_min_cost_max_flow(self) -> tuple[int, int]:
        any_path, potencials = bellman_ford(self.n, self.edges, self.source, self.sink)
        if not any_path:
            return 0,0
        
        self.apply_potentials_to_edges(potencials)
        total_flow = 0
        total_cost = 0
        while True:
            any_path, potencials = dijkstra(self.n, self.adjacents, self.source, self.sink)
            if not any_path:
                break

            self.apply_potentials_to_edges(potencials)
            while True:
                self.dinitz_bfs()
                if self.dist_from_source[self.sink] > self.n:
                    break

                current_flow = self.dinitz_dfs()
                total_flow += current_flow 
                total_cost += current_flow * self.sink_potential
                
        return total_flow, total_cost
