from evaluator import run_evaluator
import pytest



def test_random_cases():
    results = run_evaluator('generated_cases_for_testing.json', dump_to_json=False)
    for x in results:
        assert x['naive'] == x['hungarian']

