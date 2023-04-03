import multiprocessing
import json

from matplotlib.font_manager import json_dump
from naive import brute_force_sol
# from hungarian_algorithm import solve
from optimized_hungarian_algorithm import solve
import numpy as np
from utils import load_json


def evaluate(data, id: int, return_dict, use_brute_force=True):
    print(f'started proccess {id}')
    n = data['n']
    players_count = data['players_count']
    specters_count = data['specters_count']
    players_points = data['players_points']
    specters_points = data['specters_points']
    hungarian = solve(n,players_count,specters_count,players_points,specters_points)
    print(f'finished hungarian {id}')

    if use_brute_force:
        naive = brute_force_sol(n,players_count,specters_count,players_points,specters_points)
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
    # print(f'finished brute force {id}')
    else:
        return_dict[id] = hungarian
    print(f'finished proccess {id}')
    
    


def run_evaluator(json_name, dump_to_json=True, use_brute_force=True):
    data = load_json(json_name)
    print('started')
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(len(data)):
        p = multiprocessing.Process(target=evaluate, args=(data[i], i, return_dict, use_brute_force))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    
    values_list = list(return_dict.values())
    if use_brute_force:
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
    
    print(values_list)



run_evaluator('generated_cases_for_testing.json', use_brute_force=False)