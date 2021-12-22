import time
import math
from node import Node
from game_state import GameState
import copy


class Algorithm():
    def __init__(self, level):
        self.rows = level.height
        self.col = level.width
        self.matrix = level.matrix
        self.adj_matrix = []
        self.path = []
        self.createAdjMatrix()

    def getNeighbours(self, point):
        neighbours = []
        if point['x'] > 0 and point['x'] < self.col-1:
            if self.matrix[point['y']][point['x']-1] != 0:
                neighbours.append({"x": point['x']-1, "y": point['y']})
            if self.matrix[point['y']][point['x']+1] != 0:
                neighbours.append({"x": point['x']+1, "y": point['y']})
        if point['x'] == 0:
            if self.matrix[point['y']][point['x']+1] != 0:
                neighbours.append({"x": point['x']+1, "y": point['y']})
        if point['x'] == self.col-1:
            if self.matrix[point['y']][point['x']-1] != 0:
                neighbours.append({"x": point['x']-1, "y": point['y']})
        if point['y'] > 0 and point['y'] < self.rows-1:
            if self.matrix[point['y']-1][point['x']] != 0:
                neighbours.append({"y": point['y']-1, "x": point['x']})
            if self.matrix[point['y']+1][point['x']] != 0:
                neighbours.append({"y": point['y']+1, "x": point['x']})
        if point['y'] == 0:
            if self.matrix[point['y']+1][point['x']] != 0:
                neighbours.append({"y": point['y']+1, "x": point['x']})
        if point['y'] == self.rows-1:
            if self.matrix[point['y']-1][point['x']] != 0:
                neighbours.append({"y": point['y']-1, "x": point['x']})
        return neighbours

    def createAdjMatrix(self):
        for row in range(self.col * self.rows):
            self.adj_matrix.append([0]*self.rows * self.col)

        for i in range(self.rows):
            for j in range(self.col):
                neighbours = self.getNeighbours({"y": i, "x": j})
                if len(neighbours) != 0:
                    for point in neighbours:
                        self.adj_matrix[i*self.col +
                                        j][point['y']*self.col + point['x']] = 1

    def bfsSolve(self, start):
        q = []
        q.append(start)
        visited = [False]*self.rows*self.col
        visited[start['y'] * self.col + start['x']] = True
        prev = [None]*self.rows*self.col
        while len(q) > 0:
            point = q.pop(0)
            neighbours = self.getNeighbours(point)
            for element in neighbours:
                if visited[element['y']*self.col + element['x']] == False:
                    q.append(element)
                    visited[element['y']*self.col + element['x']] = True
                    prev[element['y']*self.col + element['x']] = point
        return prev

    def reconstructPath(self, start, end, prev):
        if len(prev) == 0:
            return []
        path = []
        at = end
        while at != None:
            path.append(at)
            at = prev[at['y']*self.col + at['x']]
        path.reverse()
        if path[0]['x'] == start['x'] and path[0]['y'] == start['y']:
            return path
        return []

    def restructPath(self):
        restructed_path = []
        for point in self.path:
            restructed_path.append((point['x'], point['y']))
        if len(restructed_path) > 0:
            restructed_path.pop(0)
        self.path = restructed_path

    def bfs(self, start, end):
        tic = time.perf_counter()
        prev = self.bfsSolve(start)
        self.path = self.reconstructPath(start, end, prev)
        toc = time.perf_counter()
        # print(f"Worked for {toc - tic:0.4f} seconds")

    def dfsSolve(self, visited, prev, point):
        visited[point['y'] * self.col + point['x']] = True
        neighbours = self.getNeighbours(point)
        for element in neighbours:
            if visited[element['y']*self.col + element['x']] == False:
                prev[element['y']*self.col + element['x']] = point
                self.dfsSolve(visited, prev, element)

    def dfs(self, start, end):
        tic = time.perf_counter()
        visited = [False]*self.rows*self.col
        prev = [None]*self.rows*self.col
        self.dfsSolve(visited, prev, start)
        self.path = self.reconstructPath(start, end, prev)
        toc = time.perf_counter()
        print(f"Worked for {toc - tic:0.4f} seconds")

    def findNodeCost(self, point1, point2):
        return self.adj_matrix[point1['y']*self.col+point1['x']][point2['y']*self.col+point2['x']]

    def ucsSolve(self, start, end):
        visited = [False]*self.col*self.rows
        cost = [10**3]*self.col*self.rows
        prev = [None]*self.col*self.rows
        q = []
        el = start
        q.append(el)
        cost[el['y']*self.col+el['x']] = 0
        visited[el['y']*self.col+el['x']] = True
        if start == end:
            return []
        while len(q) > 0:
            point = q.pop(0)
            neighbours = self.getNeighbours(point)
            for item in neighbours:
                if visited[item['y']*self.col+item['x']] == False:
                    q.append(item)
                    cost[item['y']*self.col+item['x']] = cost[point['y']
                                                              * self.col+point['x']] + self.findNodeCost(point, item)
                    prev[item['y']*self.col+item['x']] = point
                    if item == end:
                        return prev
                visited[item['y']*self.col+item['x']] = True
        return prev

    def ucs(self, start, end):
        prev = self.ucsSolve(start, end)
        self.path = self.reconstructPath(start, end, prev)

    def add_to_open(self, open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f >= node.f):
                return False
        return True

    def astar_search(self, start, end):
        opened = []
        closed = []
        start_node = Node(start, None)
        goal_node = Node(end, None)
        opened.append(start_node)
        while len(opened) > 0:
            opened.sort()
            current_node = opened.pop(0)
            closed.append(current_node)
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                self.path = path[::-1]
                return
            (x, y) = current_node.position
            point = {"x": x, "y": y}
            neighbors = self.getNeighbours(point)
            for next in neighbors:
                neighbor = Node((next['x'], next['y']), current_node)
                if(neighbor in closed):
                    continue
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                if(self.add_to_open(opened, neighbor) == True):
                    opened.append(neighbor)
        self.path = None
        return

    def astarSearchForState(self, state, start, end):
        opened = []
        closed = []
        start_node = Node(start)
        goal_node = Node(end)
        opened.append(start_node)
        while len(opened) > 0:
            opened.sort()
            current_node = opened.pop(0)
            closed.append(current_node)
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            neighbors = self.getNeighboursForState(state, current_node.position)
            for next in neighbors:
                neighbor = Node((next[0], next[1]), current_node)
                if(neighbor in closed):
                    continue
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                if(self.add_to_open(opened, neighbor) == True):
                    opened.append(neighbor)
        return []

    def getNeighboursForState(self, state, coords):
        (cx, cy) = coords
        neighbours = [(cx-1, cy), (cx, cy+1), (cx+1, cy), (cx, cy-1)]
        neighbours = list(filter(
            lambda node: node[0] >= 0 and node[0] < len(
                state.matrix) and node[1] >= 0 and node[1] < len(state.matrix[0]) and state.matrix[node[0]][node[1]] != 0,
            neighbours
        ))

        return neighbours

    def getVariantsRecursion(self, result, array_coords, curr_variant):
        if len(array_coords) == 0:
            result.append(curr_variant)
            return
        curr_arr = array_coords[0]
        for item in curr_arr:
            self.getVariantsRecursion(
                result, array_coords[1:], curr_variant + [item])

    def evaluation(self, node, target):
        delta = math.inf
        pacman_coord = node.state.player_coords
        if target == pacman_coord:
            return math.inf
        ghosts_coords = node.state.ghosts_coords

        for ghost in ghosts_coords:
            distance = len(self.astarSearchForState(
                node.state, pacman_coord, ghost))
            if delta is None or delta > distance:
                delta = distance
        target_distance = len(self.astarSearchForState(
            node.state, pacman_coord, target))
        result = -(target_distance + 0.1*delta)

        return result

    def generateTree(self, start_state, target):
        start_node = Node(state=start_state)
        self.generateTreeRecursion(start_node, 1, target)
        return start_node

    def generateTreeRecursion(self, curr_node, depth, target):
        if depth >= 3:
            curr_node.value = self.evaluation(curr_node, target)
            return 
        curr_state = curr_node.state
        pacman_coord = curr_state.player_coords
        ghosts_coords = curr_state.ghosts_coords
        if depth % 2 == 1:
            neighbours = list(filter(
                lambda x: x not in ghosts_coords, self.getNeighboursForState(curr_state, pacman_coord)))
            new_nodes = list(map(lambda node: Node(state=curr_state.change_player_position(node)), neighbours))
            curr_node.children = new_nodes
        else:
            neighbours = []
            for coord in ghosts_coords:
                neighbours.append(self.getNeighboursForState(curr_state, coord))
            variants = []
            self.getVariantsRecursion(variants, neighbours, [])
            new_nodes = []
            for variant in variants:
                if pacman_coord in variant:
                    continue
                state = curr_state
                for i in range(len(ghosts_coords)):
                    state = state.change_ghost_position(i, variant[i])
                new_nodes.append(Node(state=state))
            curr_node.children = new_nodes
        for child in curr_node.children:
            self.generateTreeRecursion(child, depth+1, target)

    def minimax(self, curr_node, alpha, beta, depth):
        is_max = depth % 2 == 0
        if len(curr_node.children) == 0:
            return curr_node.value

        if is_max:
            best_value = -math.inf
            for child in curr_node.children:
                value = self.minimax(child, alpha, beta, depth+1)
                best_value = max(
                    best_value, value) if value is not None else best_value
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            curr_node.value = best_value
            return best_value

        else:
            best_value = math.inf
            for child in curr_node.children:
                value = self.minimax(child, alpha, beta, depth+1)
                best_value = min(
                    best_value, value) if value is not None else best_value
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            curr_node.value = best_value
            return best_value

    def expectimax(self, curr_node, depth):
        is_max = depth % 2 == 0
        if len(curr_node.children) == 0:
            return curr_node.value

        if is_max:
            best_value = -math.inf
            for child in curr_node.children:
                value = self.expectimax(child, depth+1)
                best_value = max(
                    best_value, value) if value is not None else best_value
            curr_node.value = best_value
            return best_value

        else:
            values = 0
            for child in curr_node.children:
                value = self.expectimax(child, depth+1)
                values += value if value is not None else 0
            curr_node.value = values / len(curr_node.children)
            return curr_node.value
