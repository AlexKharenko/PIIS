from copy import deepcopy, copy

class GameState:
    def __init__(self, matrix, player_coords=None, ghosts_coords=[], score=0):
        self.matrix = matrix
        self.score = score
        self.player_coords = player_coords
        self.ghosts_coords = ghosts_coords

    def setPlayerAndGhostsCords(self, player, ghosts):
        self.player_coords = player.coord
        self.ghosts_coords = []
        for ghost in ghosts:
            self.ghosts_coords.append(ghost.coord)

    def change_player_position(self, new_coord):
        new_matrix = deepcopy(self.matrix)
        new_score = self.score
        if(new_matrix[new_coord[0]][new_coord[1]] == 1):
            new_score += 10
        new_matrix[new_coord[0]][new_coord[1]] = 2
        new_player_coords = new_coord
        return GameState(new_matrix, new_player_coords, self.ghosts_coords, new_score)

    def change_ghost_position(self, ghost_id, new_coord):
        new_matrix = deepcopy(self.matrix)
        new_ghost_coords = copy(self.ghosts_coords)
        new_ghost_coords[ghost_id] = new_coord
        return GameState(new_matrix, self.player_coords, new_ghost_coords, self.score)