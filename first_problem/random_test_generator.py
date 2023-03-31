import numpy as np 
import json
from naive import brute_force_sol

def generate_test_cases(n, min_players, max_players, min_specters, max_specters, min_score, max_score):
    """ Generate test cases to save them to json format """
    test_cases = []
    
    for i in range(100):
        players_count = np.random.randint(min_players,max_players, dtype=int)
        specters_count = np.random.randint(min_specters,max_specters)
        specters_points = np.random.randint(min_score, max_score, size=n, dtype=int).tolist()
        # print(specters_points, 'point rcs' '\n')
        players_points = np.random.randint(min_score, max_score, size=n*players_count, dtype=int)
        players_points = players_points.reshape(players_count,n).tolist()
        # print(players_points, 'kkk')
        # sol = brute_force_sol(n,players_count,specters_count,players_points,specters_points)
        test_cases.append({
            'n': n,
            'players_count': players_count,
            'specters_count': specters_count,
            'players_points': players_points,
            'specters_points': specters_points,
            # 'result' : sol
        })
    
    return test_cases

test_cases = generate_test_cases(n=8, min_players=3, max_players=5, min_specters=2, max_specters=3, min_score=1, max_score=20)
json.dump(test_cases, open('test_cases.json', 'w'))


