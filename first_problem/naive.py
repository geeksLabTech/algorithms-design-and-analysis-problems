
import numpy as np
import numpy.typing as npt

class Player:
    def __init__(self, i = -1, j = -1) -> None:
        self.i = i 
        self.j = j

class Team:
    def __init__(self, n: int, p: int, k: int, score_per_position) -> None:
        self.total_score = 0
        self.score_per_position = score_per_position
        
        self.selected_players: list[tuple[int,int]] = []
        self.selected_specters: list[int] = []
        self.p = p
        self.k = k 
        self.current_players = 0 
        self.current_specters = 0
        self.people_mask = np.full(n, False, dtype=bool)
        self.positions_mask = np.full(n, False, dtype=bool)

    def add_player(self, i: int, j: int):
        self.selected_players.append((i,j))
        if j == self.score_per_position.shape[1] - 1:
            self.current_specters += 1
        else:
            self.current_players += 1
            self.positions_mask[j] = True

        self.people_mask[i] = True
        self.total_score += self.score_per_position[i][j]

    def remove_player(self, i: int, j: int):
        self.selected_players.pop()
        if j == self.score_per_position.shape[1] - 1:
            self.current_specters -= 1
        else:
            self.current_players -= 1
        self.people_mask[i] = False
        self.positions_mask[j] = False
        self.total_score -= self.score_per_position[i][j]

    def is_team_complete(self) -> bool:
        return self.current_players == self.p and self.current_specters == self.k

    def is_person_assigned(self, i: int) -> bool:
        return self.people_mask[i]

    def is_position_assigned(self, j: int) -> bool:
        return self.positions_mask[j]

    def is_possible_to_add(self, i, j) -> bool:
        if j == self.score_per_position.shape[1] - 1:
            return self.current_specters < self.k
        else:
            return self.current_players < self.p

def __brute_force(solution: Team, best_score_finded: int) -> int:
    if solution.is_team_complete():
        # print('best:', solution.total_score)
        if solution.total_score > best_score_finded:
            # best_solution_finded = solution.copy()
            best_score_finded = solution.total_score
            
        return best_score_finded
    
    for i in range(len(solution.score_per_position)):
        if solution.is_person_assigned(i):
            continue
        
        for j in range(len(solution.score_per_position[i])):
            # print(j)
            if solution.is_position_assigned(j) or not solution.is_possible_to_add(i, j):
                continue

            solution.add_player(i,j)
            best_score_finded = __brute_force(solution, best_score_finded)
            solution.remove_player(i,j)

    return best_score_finded

def brute_force_sol(n: int, p: int, k: int, players_points, specters_points):
    players_points = np.array(players_points)
    specters_points = np.array(specters_points)
    # print(players_points, 'adentro')
    specters_points_column = specters_points.reshape(1,specters_points.size).transpose()
    # print(specters_points_column.shape, 'dentro')
    # print(players_points.shape, 'mmm')
    new_table = np.hstack((players_points, specters_points_column))
    # print('mm')
    team = Team(n, p, k, new_table)
    min_value = 0
    best_score = __brute_force(team, min_value)
    return best_score










    



