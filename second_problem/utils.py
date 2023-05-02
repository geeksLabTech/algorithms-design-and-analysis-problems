
def is_difference_one(x: int, y: int):
    return abs(x - y) == 1

def are_congruent(x: int, y: int, modulo: int):
    return x % modulo == y % modulo

def is_adyacent_valid(x: int, y: int, modulo: int):
    return is_difference_one(x, y) or are_congruent(x, y, modulo)



