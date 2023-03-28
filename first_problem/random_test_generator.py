import numpy as np 
import json


def generate_test_cases(n, min_players, max_players, min_specters, max_specters, min_score, max_score):
    """ Generate test cases to save them to json format """
    test_cases = []
    
    for i in range(100):
        n = 30
        players_count = np.random.randint(min_players,max_players)
        specters_count = np.random.randint(min_specters,max_specters)
        specters_points = np.random.randint(min_score, max_score, size=players_count).tolist()
        players_points = np.random.randint(min_score, max_score, size=n*players_count)
        players_points = players_points.reshape(n,players_count).tolist()
        
        test_cases.append({
            'players_count': players_count,
            'specters_count': specters_count,
            'players_points': players_points,
            'specters_points': specters_points
        })
    
    return test_cases

test_cases = generate_test_cases(n=30, min_players=4, max_players=12, min_specters=4, max_specters=20, min_score=1, max_score=100)
json.dump(test_cases, open('test_cases.json', 'w'))


