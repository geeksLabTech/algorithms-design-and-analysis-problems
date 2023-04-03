from datetime import datetime
import numpy as np
from collections import deque
import math


class VertexInQueue:
    def __init__(self, v: int, is_left: bool) -> None:
        self.v = v
        self.is_left = is_left


def get_default_vertex_labeling(G_matrix, L, R):
    L_h = np.zeros(len(L), dtype=int)
    R_h = np.zeros(len(R), dtype=int)
    for i in range(len(L)):
        L_h[i] = G_matrix[L[i]].max()

    return L_h, R_h
    


def greedy_bipartite_matching(L, R, matrix, L_h, R_h) -> set[tuple]:
    # R_set = set(R)
    matched_in_R = [False] * (len(L))
    M: set[tuple] = set()
    for v in range(len(L)):
        for u in range(len(R)):
            if L_h[v] + R_h[u] == matrix[v,u] and not matched_in_R[u]:
                M.add((v,u))
                matched_in_R[u] = True
                break
    
    return M

# def get_equality_subgraph_edges(G_matrix, L_h, R_h) -> set[tuple]:
#     edges: set[tuple] = set()

#     for i in range(len(L_h)):
#         for j in range(len(R_h)):
#             if L_h[i] + R_h[j] == G_matrix[i][j]:
#                 edges.add((i,j))
    
#     return edges

# def get_directed_equality_subgraph_edges(E_h: set[tuple], M: set[tuple]) -> set[tuple]:
#     difference = E_h.difference(M)
#     inverted_edges = (tuple(reversed(e)) for e in M)
#     edges = difference.union(inverted_edges)

#     return edges
    

# def is_perfect_matching(total_vertex: int ,M: set[tuple]):
#     visited = set()
#     covered_vertex = 0
#     for v in M:
#         if v[0] in visited or v[1] in visited:
#             return False
#         visited.add(v[0])
#         visited.add(v[1])
#         covered_vertex+=2

#     return covered_vertex == total_vertex

# def convert_edges_set_to_vertex_set(edges: set[tuple]) -> set[int]:
#     vertex_set = set()
#     for e in edges:
#         vertex_set.add(e[0])
#         vertex_set.add(e[1])

#     return vertex_set

def calculate_delta(Fl: set[int], R_Fr_difference, L_h, R_h, matrix):
    # difference = R.difference(Fr)
    delta = math.inf
    for v in Fl:
        for u in R_Fr_difference:
            temp = L_h[v] + R_h[u] - matrix[v][u]
            if temp < delta:
                delta = temp
    
    return delta

def reconstruct_path(pi_L, pi_R, last_discovered_in_r):
    r = last_discovered_in_r
    l = pi_R[r]
    path = {(l,r)}
    while pi_L[l] is not None:

        r = pi_L[l]
        path.add((l, r))  
        l = pi_R[r]
        path.add((l, r))
        
    return path
    

def find_augmenting_path(L: set[int], R: set[int], L_h, R_h, M: set[tuple], matrix, matched_l, matched_r):
    Q: deque[VertexInQueue] = deque()

    Fl = set()
    Fr = set()
    total_vertex = set(range(len(L)))
    pi_L = [None] * (len(L))
    pi_R = [None] * (len(R))

    for v in total_vertex:
        if not matched_l[v]:
            Q.append(VertexInQueue(v, False))
            Fl.add(v)
    
    found_augmenting_path = False
    last_discovered_in_r = None
    while not found_augmenting_path:
        vertex_item = None
        
        try:
            vertex_item = Q.popleft()
        except IndexError: 
            
            old_L_h = np.array(L_h)
            old_R_h = np.array(R_h)
            R_Fr_difference = total_vertex.difference(Fr)
            delta = calculate_delta(Fl, R_Fr_difference, old_L_h, old_R_h, matrix)
            for v in Fl:
                L_h[v] -= delta

            for v in Fr:
                R_h[v] += delta

            
            for l in total_vertex:
                if found_augmenting_path:
                    break
                
                for r in total_vertex:
                    if r not in Fr and old_L_h[l] + old_R_h[r] > matrix[l,r] and L_h[l] + R_h[r] == matrix[l,r] and (l,r) not in M:
                        pi_R[r] = l

                        if matched_r[r] is None:
                            found_augmenting_path = True
                            last_discovered_in_r = r
                            break
                        else:
                            Q.append(VertexInQueue(r, True))
                            Fr.add(r)
                            
            
            if found_augmenting_path:
                break
        
        if vertex_item is None:
            vertex_item = Q.popleft()
        start = datetime.now()
        if vertex_item.is_left:
            l = matched_r[vertex_item.v]
            pi_L[l] = vertex_item.v
            Fl.add(l)
            Q.append(VertexInQueue(l, False))
        
        else:
            for r in total_vertex:
                if r not in Fr and L_h[vertex_item.v] + R_h[r] == matrix[vertex_item.v,r] and (vertex_item.v, r) not in M:
                    pi_R[r] = vertex_item.v
                    if matched_r[r] is None:
                        last_discovered_in_r = r
                        found_augmenting_path = True
                        break
                    else:
                        Q.append(VertexInQueue(r, True))
                        Fr.add(r)

    
        end = datetime.now()
        # print(f'como puede serrr {(end - start).total_seconds()} seconds')
    return reconstruct_path(pi_L, pi_R, last_discovered_in_r)
        

def update_matchings_from_M(M, n, matched_l, matched_r):
    matched_l = [False] * n
    matched_r = [None] * n
    for (l, r) in M:
        matched_l[l] = True
        matched_r[r] = l

    return matched_l, matched_r

def hungarian_algorithm(G_matrix: np.ndarray):
    L = np.array([i for i in range(G_matrix.shape[0])], dtype=int)
    R = np.array([i for i in range(G_matrix.shape[1])], dtype=int)
    
    L_h, R_h = get_default_vertex_labeling(G_matrix, L, R)
    M = greedy_bipartite_matching(L, R, G_matrix, L_h, R_h)
    matched_l = [False] * (len(L)) 
    matched_r = [None] * (len(R)) 
    
    L = set(L)
    R = set(R)
    while len(M) < len(L):
        matched_l, matched_r = update_matchings_from_M(M, len(L), matched_l, matched_r)
        path = find_augmenting_path(L, R, L_h, R_h, M, G_matrix, matched_l, matched_r)
        M ^= path
    
    return M


def solve(n, p, k, players_points, specters_points):
    """
    :param n: number of people
    :param p: number of players
    :param k: number of specters
    :param players_points: list of players points
    :param specters_points: list of specters points
    :return: total score
    """
    players_points = np.array(players_points)
    specters_points = np.array(specters_points)
    specters_points_column = specters_points.reshape(1,specters_points.size)
    
    for i in range(k):
        players_points = np.vstack((players_points, specters_points_column))
    
    zero_column = np.zeros(len(specters_points), dtype=int)
    zero_column = zero_column.reshape(1, zero_column.size)
    while players_points.shape[0] < n:
        players_points = np.vstack((players_points, zero_column))
    
    perfect_matching = hungarian_algorithm(players_points)
    return sum([players_points[l,r] for (l, r) in perfect_matching])
   



