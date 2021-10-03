import time
from node import Node

class Algorithm():
    def __init__(self,level):
        self.rows = level.height
        self.col = level.width
        self.matrix = level.matrix
        self.adj_matrix = []
        self.path = []
        self.createAdjMatrix()

    def getNeighbours(self, point):
        neighbours = []
        if point['x'] > 0 and point['x'] < self.col-1:
            if self.matrix[point['y']][point['x']-1] != "=":
                neighbours.append({ "x": point['x']-1, "y":point['y']})
            if self.matrix[point['y']][point['x']+1] != "=":
                neighbours.append({ "x": point['x']+1, "y":point['y']})
        if point['x'] == 0:
            if self.matrix[point['y']][point['x']+1] != "=":
                neighbours.append({"x":point['x']+1, "y":point['y']})
        if point['x'] == self.col-1:
            if self.matrix[point['y']][point['x']-1] != "=":
                neighbours.append({ "x": point['x']-1, "y":point['y']})
        if point['y'] > 0 and point['y'] < self.rows-1:
            if self.matrix[point['y']-1][point['x']] != "=":
                neighbours.append({ "y": point['y']-1, "x":point['x']})
            if self.matrix[point['y']+1][point['x']] != "=":
                neighbours.append({ "y": point['y']+1, "x":point['x']})
        if point['y'] == 0:
            if self.matrix[point['y']+1][point['x']] != "=":
                neighbours.append({"y":point['y']+1, "x":point['x']})
        if point['y'] == self.rows-1:
            if self.matrix[point['y']-1][point['x']] != "=":
                neighbours.append({"y":point['y']-1, "x":point['x']})
        return neighbours

    def createAdjMatrix(self):
        for row in range(self.col * self.rows):
            self.adj_matrix.append([0]*self.rows * self.col)
        
        for i in range(self.rows):
            for j in range(self.col):
                neighbours = self.getNeighbours({"y": i, "x": j})
                if len(neighbours) != 0:
                    for point in neighbours:
                        self.adj_matrix[i*self.col + j][point['y']*self.col + point['x']] = 1
                        

    def bfsSolve(self, start):
        q = []
        q.append(start)
        visited = [False]*self.rows*self.col
        visited[start['y'] * self.col + start['x']] = True
        prev = [None]*self.rows*self.col
        while len(q)>0:
            point = q.pop(0)
            neighbours = self.getNeighbours(point)
            for element in neighbours:
                if visited[element['y']*self.col +element['x']] == False:
                    q.append(element)
                    visited[element['y']*self.col +element['x']] = True
                    prev[element['y']*self.col +element['x']] = point
        return prev

    def reconstructPath(self, start, end, prev):
        if len(prev)==0:
            return []
        path = []
        at = end
        while at != None:
            path.append(at)
            at = prev[at['y']*self.col +at['x']]
        path.reverse()
        if path[0]['x']==start['x'] and path[0]['y']==start['y']:
            return path
        return []

    def restructPath(self):
        restructed_path = []
        for point in self.path:
            restructed_path.append((point['x'], point['y']))
        if len(restructed_path)>0:
            restructed_path.pop(0)
        self.path = restructed_path

    def bfs(self, start, end):
        tic = time.perf_counter()
        prev = self.bfsSolve(start)
        self.path = self.reconstructPath(start, end, prev)
        toc = time.perf_counter()
        # print(f"Worked for {toc - tic:0.4f} seconds")      

    def dfsSolve(self, visited, prev, point):
        visited[point['y'] * self.col + point['x']] =True
        neighbours = self.getNeighbours(point)
        for element in neighbours:
            if visited[element['y']*self.col +element['x']] == False:
                prev[element['y']*self.col +element['x']] = point
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
        while len(q)>0:
            point = q.pop(0)
            neighbours = self.getNeighbours(point)
            for item in neighbours:
                if visited[item['y']*self.col+item['x']] == False:
                    q.append(item)
                    cost[item['y']*self.col+item['x']] = cost[point['y']*self.col+point['x']] + self.findNodeCost(point, item)
                    prev[item['y']*self.col+item['x']] = point
                    if item == end: 
                        return prev
                visited[item['y']*self.col+item['x']] = True
        return prev

    def ucs(self, start, end):
        prev = self.ucsSolve(start, end)
        self.path= self.reconstructPath(start, end, prev)

    
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
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                if(self.add_to_open(opened, neighbor) == True):
                    opened.append(neighbor)
        self.path = None
        return 
