import random

import numpy as np
from utils import Student
from naive import solve
from ant_colony import solve_with_aproximation
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def generator(cases: int):
    generated_cases: list[tuple[list[Student], int]] = []

    while cases > 0:
        students_number = random.randint(5, 50)
        k = random.randint(3, students_number - 1)
        students_id = np.arange(students_number)
        students: list[Student] = []
        for i in students_id:
            opinions_number = random.randint(0, students_number - 1)
            opinions = np.random.choice(
                a=students_number, replace=False, size=opinions_number
            ).tolist()
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
            print(
                f"bad solution detected, student {s.id} have a bad opinion with {negative_opinions_to_populars}"
            )
            return False

    return True

def compare_aproximation(data):
    dataframe = pd.DataFrame(data, columns=['Tests', 'BruteForce', 'Aproximation'])
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(x="BruteForce", y="Tests", data=dataframe,
                label="Total", color="b")

    sns.set_color_codes("muted")
    sns.barplot(x="Aproximation", y="Tests", data=dataframe,
                label="Aproximation", color="b")

    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 24), ylabel="",
    )
    sns.despine(left=True, bottom=True)


def run_test_cases(cases: int, seed: int):
    generated_test = generator(cases)
    bad_solutions = 0
    registry: list[list] = []
    for i, t in enumerate(generated_test):
        print(f"starting solve for {len(t[0])} students and k: {t[1]}")
        solution = solve(t[0], t[1])
        
        r = verify_solution(t[0], t[1], solution[1])

        if r is False:
            bad_solutions += 1

        if r is True and solution[0] == t[1]:
            print(f"k matched")

        aproximation = solve_with_aproximation(t[0], t[1])
        registry.append([i, solution[0], aproximation[0]])
    if bad_solutions > 0:
        print(f"bad solutions finded: {bad_solutions}")

    else:
        print("yeah, all seems good")

    compare_aproximation(registry)



run_test_cases(20, 2)
