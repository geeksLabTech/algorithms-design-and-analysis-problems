from evaluator import run_evaluator

def test_random_cases():
    run_evaluator('test_cases_second_problem.json', dump_to_json=True)
    
test_random_cases()