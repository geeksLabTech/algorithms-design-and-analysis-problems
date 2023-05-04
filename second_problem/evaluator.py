import multiprocessing
import json
import numpy as np
from matplotlib.font_manager import json_dump
from brute_force import execute_brute_force
from efficient_solution import solve
from utils import load_json


def evaluate(data, id: int, return_dict, use_brute_force=True):
    print(f'started proccess {id}')
    n = data['n']
    shortest_path = solve(n)
    if use_brute_force:
        naive = execute_brute_force(n)
        if shortest_path != naive:
            print()
            print(f' shortest_path{shortest_path}, naive {naive}')
            print(n)
            
            print()
        return_dict[id] = (naive, shortest_path, shortest_path == naive)
    # print(f'finished brute force {id}')
    else:
        return_dict[id] = shortest_path
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
        
        for i in range(len(values_list)):
            if values_list[i][2]:
                passed += 1
            else:
                final_list.append(values_list[i])
        print(f'passed {passed} out of {len(values_list)}')
        print(f'failed {len(final_list)} out of {len(values_list)}')
        if dump_to_json:
            json_dump(final_list, open('failed_tests.json', 'w'))


