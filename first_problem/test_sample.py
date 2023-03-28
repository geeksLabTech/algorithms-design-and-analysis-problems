from naive import brute_force_sol
import pytest

def test_brute_force():
    n = 6
    p = 3
    k = 2
    players_points = [
        [2,1,0],
        [0,0,0],
        [1,2,0],
        [0,0,0],
        [2,0,0],
        [0,0,0]
    ]
    # print(players_points)
    specters_points = [0, 2, 0, 4, 1, 2]
    # print(specters_points)
    solution = brute_force_sol(n, p, k, players_points, specters_points)
    assert solution == 10
    print('Solution:', solution)

test_brute_force()