
import numpy as np
from collections import deque
import math
from datetime import datetime

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

    

def calculate_sigma(Fl: set[int], R_Fr_difference, L_h, R_h, matrix, sigma, omega):
    for l in Fl:
        for r in R_Fr_difference:
            temp = L_h[l] + R_h[r] - matrix[l][r]
            if temp < sigma[r]:
                sigma[r] = temp
                omega[r] = l
    
    return sigma, omega


def reconstruct_path(pi_L, pi_R, last_discovered_in_r, matched_l, matched_r, L_h, R_h):
    r = last_discovered_in_r
    l = pi_R[r]
    path = {(l,r)}
    matched_r[r] = l
    while pi_L[l] is not None:

        r = pi_L[l]
        path.add((l, r))  
        l = pi_R[r]
        path.add((l, r))
        matched_r[r] = l
    matched_l[l] = True
    return path, matched_l, matched_r
    

def find_augmenting_path(L: set[int], R: set[int], L_h, R_h, M: set[tuple], matrix, matched_l, matched_r):
    Q: deque[VertexInQueue] = deque()
    Fl = set()
    Fr = set()
    total_vertex = set(range(len(L)))
    pi_L = np.full(len(L), None) 
    pi_R = np.full(len(L), None)
    sigma = {x:math.inf for x in R}
    omega = {}
    for v in total_vertex:
        if not matched_l[v]:
            Q.append(VertexInQueue(v, False))
            Fl.add(v)
    

    sigma, omega = calculate_sigma(Fl, R, L_h, R_h, matrix, sigma, omega)
    
    found_augmenting_path = False
    last_discovered_in_r = None
    while not found_augmenting_path:
        vertex_item = None
        
        try:
            vertex_item = Q.popleft()
        except IndexError: 
            delta = math.inf
            for x in sigma:
                temp = sigma[x]
                if temp<delta:
                    delta = temp
    
            assert delta > 0

            for v in Fl:
                L_h[v] -= delta
               
            
            for v in Fr:
                R_h[v] += delta

            vertex_to_remove_from_R = []

            for x in sigma:
                sigma[x]-=delta
                # r = sigma[x]
                if sigma[x] == 0:
                    pi_R[x] = omega[x]
                    if matched_r[x] is None:
                            found_augmenting_path = True
                            last_discovered_in_r = x
                            break
                    else:
                        Q.append(VertexInQueue(x, True))
                        Fr.add(x)
                        vertex_to_remove_from_R.append(x)
            
            if found_augmenting_path:
                break
            
            for x in vertex_to_remove_from_R:
                del sigma[x]
                R.remove(x)
            
            
        
        if vertex_item is None:
            vertex_item = Q.popleft()

        if vertex_item.is_left:
            
            l = matched_r[vertex_item.v]
            pi_L[l] = vertex_item.v
            Fl.add(l)
           
            for r in R:
                temp = L_h[l] + R_h[r] - matrix[l,r]

                if temp>0 and temp < sigma[r] and (l, r) not in M:
                    sigma[r] = temp
                    omega[r] = l
               
            Q.append(VertexInQueue(l, False))
        
        else:
            assert vertex_item is not None
            vertex_to_remove_from_R = []
            for r in R:
                if L_h[vertex_item.v] + R_h[r] == matrix[vertex_item.v,r] and (vertex_item.v, r) not in M:
                    pi_R[r] = vertex_item.v
                    if matched_r[r] is None:
                        last_discovered_in_r = r
                        found_augmenting_path = True
                        break
                    else:
                        Q.append(VertexInQueue(r, True))
                        Fr.add(r)
                        del sigma[r]
                        
                        vertex_to_remove_from_R.append(r)

            R = R.difference(vertex_to_remove_from_R)
        
    return reconstruct_path(pi_L, pi_R, last_discovered_in_r, matched_l, matched_r,  L_h, R_h)
        

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
    matched_l, matched_r= update_matchings_from_M(M, len(L), matched_l, matched_r)
    L = set(L)
    R = set(R)
    while len(M) < len(L):
        
        path, matched_l, matched_r = find_augmenting_path(L, R, L_h, R_h, M, G_matrix, matched_l, matched_r)
        M ^= path
        # print('M len', len(M))
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
   



