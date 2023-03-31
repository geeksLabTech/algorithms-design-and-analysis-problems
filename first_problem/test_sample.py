from naive import brute_force_sol
import pytest
from hungarian_algorithm import solve

def test_brute_force():
    n = 6
    p = 3
    k = 2
    players_points = [
        [2,0,1,0,2,0],
        [1,0,0,0,0,0],
        [0,0,0,0,0,0]
    ]
    # print(players_points)
    specters_points = [0, 2, 0, 4, 1, 2]
    # print(specters_points)
    solution = brute_force_sol(n, p, k, players_points, specters_points)
    assert solution == 9
    efficient_solution = solve(n, p, k, players_points, specters_points)
    print('Backtrack:', solution)
    print('efficient solution', efficient_solution)
    assert efficient_solution == 9
    

test_brute_force()