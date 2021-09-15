import time

class Algorithm():
    def __init__(self,level):
        self.rows = level.height
        self.col = level.width
        self.matrix = level.matrix
        self.path = []

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
        path = []
        at = end
        while at != None:
            path.append(at)
            at = prev[at['y']*self.col +at['x']]
        path.reverse()
        if path[0]['x']==start['x'] and path[0]['y']==start['y']:
            return path
        return []

    def bfs(self, start, end):
        # tic = time.perf_counter()
        prev = self.bfsSolve(start)
        self.path = self.reconstructPath(start, end, prev)
        # toc = time.perf_counter()
        # print(f"Worked for {toc - tic:0.4f} seconds")
        

    def dfsSolve(self, visited, prev, point):
        visited[point['y'] * self.col + point['x']] =True
        neighbours = self.getNeighbours(point)
        for element in neighbours:
            if visited[element['y']*self.col +element['x']] == False:
                prev[element['y']*self.col +element['x']] = point
                self.dfsSolve(visited, prev, element)
        

    def dfs(self, start, end):
        # tic = time.perf_counter()
        visited = [False]*self.rows*self.col
        prev = [None]*self.rows*self.col
        self.dfsSolve(visited, prev, start)
        self.path = self.reconstructPath(start, end, prev)
        # toc = time.perf_counter()
        # print(f"Worked for {toc - tic:0.4f} seconds")

    # def ucsSolve(self, start):
    #     q = []
    #     q.append(start)
    #     visited = [False]*self.rows*self.col
    #     visited[start['y'] * self.col + start['x']] = True
    #     path_cost = [0]*self.rows*self.col
    #     prev = [None]*self.rows*self.col
    #     while len(q)>0:
    #         point = q.pop(0)
    #         neighbours = self.getNeighbours(point)
    #         for element in neighbours:
    #             if visited[element['y']*self.col +element['x']] == False:
    #                 q.append(element)
    #                 visited[element['y']*self.col +element['x']] = True
    #                 prev[element['y']*self.col +element['x']] = point
    #     return prev