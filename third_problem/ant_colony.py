from utils import Node, add_node_to_solution, remove_node_from_solution
import random


class AntClique:
    def __init__(
        self,
        nodes: list[Node],
        target_k: int,
        num_ants=7,
        taomin=0.01,
        taomax=4,
        alpha=2,
        rho=0.995,
        max_cycles=3000,
    ):
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

    def build_clique(self):
        finded_initial_valid_node = False
        starting_nodes: list[Node] = []
        mask = [False] * len(self.nodes)
        dependencies = {}
        current_best_nodes: set[Node] = set()
        while not finded_initial_valid_node:
            initial_node: Node = random.sample(self.nodes, 1)[0]
            mask = [False] * len(self.nodes)
            starting_nodes, mask, dependencies = add_node_to_solution(
                initial_node, [], mask, {}
            )
            if len(starting_nodes) > self.target_k:
                continue

            finded_initial_valid_node = True

        selected_nodes = set()
        for x in starting_nodes:
            selected_nodes.add(x)

        candidates = set()
        for n in starting_nodes:
            candidates.union(n.get_adjecent_nodes())

        current_best_nodes.update(selected_nodes)
        while len(candidates) > 0:
            pheromone_factors = [
                self.__get_pheromone_factor(n, candidates) for n in candidates
            ]
            pheromone_probs = [f / sum(pheromone_factors) for f in pheromone_factors]
            selected_node = random.choices(
                list(candidates), weights=pheromone_probs, k=1
            )[0]
            updated_nodes, mask, dependencies = add_node_to_solution(
                selected_node, list(selected_nodes), mask, dependencies
            )
            selected_nodes = selected_nodes.union(set(updated_nodes))
            if len(selected_nodes) > self.target_k:
                break
            candidates = candidates.intersection(selected_node.get_adjecent_nodes())
            current_best_nodes.update(selected_nodes)

        return current_best_nodes

    def update_pheromone_trails(self, solutions: list[set[Node]]):
        best_solution = max(solutions, key=lambda x: len(x))
        if len(best_solution) > len(self.best_clique):
            self.best_clique = list(best_solution)

        if len(self.best_clique) == self.target_k:
            # Target clique found, stop algorithm
            return True

        # evaporate pheromone on all edges
        for node in self.nodes:
            for e in node.edges:
                e.pheromone = max(self.taomin, self.rho * e.pheromone)

        c_best = len(self.best_clique)
        c_k = len(best_solution)

        for node in best_solution:
            for e in node.edges:
                e.pheromone += min(self.taomax, (1 / (1 + c_best - c_k)))

        return False

    def run(self):
        pass

    def __get_pheromone_factor(self, node: Node, candidates: set[Node]):
        return sum([e.pheromone for e in node.get_outgoing_edges() if e in candidates])
