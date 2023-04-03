import numpy as np 
import json


def generate_test_cases(tests_number, n, min_players, max_players, min_specters, max_specters, min_score, max_score):
    """ Generate test cases to save them to json format """
    test_cases = []
    
    for i in range(tests_number):
        players_count = np.random.randint(min_players,max_players, dtype=int)
        specters_count = np.random.randint(min_specters,max_specters)
        specters_points = np.random.randint(min_score, max_score, size=n, dtype=int).tolist()
        players_points = np.random.randint(min_score, max_score, size=n*players_count, dtype=int)
        players_points = players_points.reshape(players_count,n).tolist()
        test_cases.append({
            'n': n,
            'players_count': players_count,
            'specters_count': specters_count,
            'players_points': players_points,
            'specters_points': specters_points,
            # 'result' : sol
        })
    
    return test_cases

test_cases = generate_test_cases(2, n=2000, min_players=1500, max_players=1800, min_specters=100, max_specters=200, min_score=1, max_score=100)
json.dump(test_cases, open('test_cases.json', 'w'))


