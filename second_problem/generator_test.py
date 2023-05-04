import numpy as np
import json

def generate_test(test_number):
    test_cases = []

    for i in range(test_number):
        length = np.random.randint(1, 10)
        n = [0]* length
        for i in range(length):
            n[i] = np.random.randint(1, 50)
        test_cases.append({
            'n': n
        })
    return test_cases

test_cases = generate_test(100)
json.dump(test_cases, open('test_cases.json', 'w'))
