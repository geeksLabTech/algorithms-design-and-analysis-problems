import multiprocessing
import json

from matplotlib.font_manager import json_dump
from naive import brute_force_sol
from hungarian_algorithm import solve
import numpy as np

def load_json(json_name):
    data = {}

    with open(json_name) as file:
        data = json.load(file)

    return data

def evaluate(data, id: int, return_dict):
    print(f'started proccess {id}')
    n = data['n']
    players_count = data['players_count']
    specters_count = data['specters_count']
    players_points = data['players_points']
    specters_points = data['specters_points']
    print('hey', np.array(players_points).shape, players_count)
    naive = brute_force_sol(n,players_count,specters_count,players_points,specters_points)
    print(f'finished brute force {id}')
    hungarian = solve(n,players_count,specters_count,players_points,specters_points)
    print(f'finished proccess {id}')
    if hungarian != naive:
        print()
        print(f'hungarian {hungarian}, naive {naive}')
        print(n)
        print(players_count)
        print(specters_count)
        print(players_points)
        print(specters_points)
        print()
    return_dict[id] = (naive, hungarian, hungarian==naive)
    


def run_evaluator(json_name, dump_to_json=True):
    data = load_json(json_name)
    print('started')
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(len(data)):
        p = multiprocessing.Process(target=evaluate, args=(data[i], i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    
    values_list = list(return_dict.values())

    final_list = []
    passed = 0
    for i in range(len(return_dict.values())):
        if int(values_list[i][2]) == 1:
            passed+=1
        final_list.append({
            'naive': int(values_list[i][0]),
            'hungarian': int(values_list[i][1]),
            'Equal': int(values_list[i][2])

        })
    
    print(f'passed {passed} cases of {len(data)}')
    if dump_to_json:
        json.dump(final_list, open('results.json', 'w'))
    return final_list



run_evaluator('test_cases.json')