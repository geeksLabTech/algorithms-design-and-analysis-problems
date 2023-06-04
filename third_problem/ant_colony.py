from utils import Node, add_node_to_solution, remove_node_from_solution
import random

class AntClique:
    def __init__(self, nodes: list[Node], target_k: int, num_ants=7, taomin=0.01, taomax=4, alpha=2, rho=.995, max_cycles=3000):
        self.num_ants = num_ants
        self.taomin = taomin
        self.taomax = taomax
        self.alpha = alpha
        self.rho = rho
        self.max_cycles = max_cycles
        
        self.nodes = nodes
        self.target_k = target_k
        self.best_clique: list[Node] = []

    def initialize_pheromone_trails(self):
        for node in self.nodes:
            for e in node.edges:
                e.pheromone = self.taomax

    
    def run(self):
        finded_initial_valid_node = False
        starting_nodes: list[Node] = []
        mask = [False] * len(self.nodes)
        dependencies = {}
        while not finded_initial_valid_node:
            initial_node: Node = random.sample(self.nodes, 1)[0]
            mask = [False] * len(self.nodes)
            starting_nodes, mask, dependencies = add_node_to_solution(initial_node, [], mask, {})
            if len(starting_nodes) > self.target_k:
                continue

            finded_initial_valid_node = True

            selected_nodes = set()
            for x in starting_nodes:
                selected_nodes.add(x)
                
            candidates = set()
            for n in starting_nodes:
                candidates.union(n.get_adjecent_nodes())

            while len(candidates) > 0