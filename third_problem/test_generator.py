import random

import numpy as np
from utils import Student
from naive import solve

def generator(cases: int):
    generated_cases: list[tuple[list[Student], int]] = []
    
    while cases > 0:
        students_number = random.randint(5, 50)
        k = random.randint(3, students_number-1)
        students_id = np.arange(students_number)
        students: list[Student] = []
        for i in students_id:
            opinions_number = random.randint(0, students_number-1)
            opinions = np.random.choice(a=students_number, replace=False, size=opinions_number).tolist()
            if i in opinions:
                opinions.remove(i)
            students.append(Student(i, opinions))
        
        generated_cases.append((students, k))
        cases -= 1
    
    return generated_cases


def verify_solution(students: list[Student], k: int, result: list[int]):
    ids = set([s.id for s in students])
    students_ids_to_check = ids - set(result)
    students_to_check = [s for s in students if s.id in students_ids_to_check]
    for s in students_to_check:
        negative_opinions_to_populars = set(s.opinions).intersection(result)
        if len(negative_opinions_to_populars) > 0:
            print(f'bad solution detected, student {s.id} have a bad opinion with {negative_opinions_to_populars}')
            return False

    return True

def run_test_cases(cases: int, seed: int):
    generated_test = generator(cases)
    bad_solutions = 0
    for t in generated_test:
        print(f'starting solve for {len(t[0])} students and k: {t[1]}')
        solution = solve(t[0], t[1])
        r = verify_solution(t[0], t[1], solution[1])

        if r is False:
            bad_solutions+=1

        if r is True and solution[0] == t[1]:
            print(f'k matched')

    if bad_solutions > 0:
        print(f'bad solutions finded: {bad_solutions}')

    else:
        print('yeah, all seems good')


run_test_cases(20, 2)


