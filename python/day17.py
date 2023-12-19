from queue import PriorityQueue
from aoc import Aoc
from canvas import Canvas
from utilities import neighbours4
from dijkstra import DoDijkstra
import heapq
import itertools
import math
import sys

# Day 17
# https://adventofcode.com/2023

class Day17Solution(Aoc):

    def Run(self):
        self.StartDay(17, "Clumsy Crucible")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(17)

        goal = self.TestDataA()
        self.PartA()
        self.Assert(self.GetAnswerA(), goal)

        goal = self.TestDataB()
        self.PartB()
        self.Assert(self.GetAnswerB(), goal)

    def TestDataA(self):
        self.inputdata.clear()
        testdata = \
        """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 102

    def TestDataB(self):
        self.inputdata.clear()
        # self.TestDataA()    # If test data is same as test data for part A
        testdata = \
        """
        1000
        2000
        3000
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return None

    def ParseInput(self):
        data = []
        for line in self.inputdata:
            data.append([int(c) for c in line])

        return data

    def TooManyStraight(self, next: tuple[int, int], current: tuple[int, int], came_from):
        x, y = current
        nx, ny = next
        dx = nx - x
        dy = ny - y
        
        if current not in came_from:
            return False
        cf1 = came_from[current]
        if cf1 is None:
            return False
        cx1, cy1 = cf1
        if not (cx1 + dx == x and cy1 + dy == y):
            return False
        
        if cf1 not in came_from:
            return False
        cf2 = came_from[cf1]
        if cf2 is None:
            return False
        cx2, cy2 = cf2
        if not (cx2 + dx == cx1 and cy2 + dy == cy1):
            return False
        
        if cf2 not in came_from:
            return False
        cf3 = came_from[cf2]
        if cf3 is None:
            return False
        cx3, cy3 = cf3
        if not (cx3 + dx == cx2 and cy3 + dy == cy2):
            return False

        return True

    def heuristicX(self, a, b) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def heuristic(self, p1, p2) -> int:
        """
        Takes two points and returns the euclidian distance
        """
        x1, y1 = p1
        x2, y2 = p2
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return int(distance)

    def astarXXX(self, graph, start, end):
        G = {} # Actual movement cost to each position from the start position
        F = {} # Estimated movement cost of start to end going via this position

        w = len(graph[0])
        h = len(graph)

        # Initialize starting values
        G[start] = 0 
        F[start] = self.heuristic(start, end)
    
        closedVertices = set()
        openVertices = set([start])
        cameFrom = {}
    
        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    current = pos
    
            # Check if we have reached the goal
            if current == end:
                # Retrace our route backward
                path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                path.reverse()
                return path #, F[end] #Done!
    
            # Mark the current vertex as closed
            openVertices.remove(current)
            closedVertices.add(current)
    
            # Update scores for vertices near the current position
            for neighbour in neighbours4(*current, (w, h)):
                if neighbour in closedVertices: 
                    continue # We have already processed this node exhaustively
 
                cost = graph[current[1]][current[0]]
                if self.TooManyStraight(neighbour, current, cameFrom):
                    cost = 1000
 
                candidateG = G[current] + cost

                if neighbour not in openVertices:
                    openVertices.add(neighbour) # Discovered a new vertex
                elif candidateG >= G[neighbour]:
                    continue # This G score is worse than previously found
    
                # Adopt this G score
                cameFrom[neighbour] = current
                G[neighbour] = candidateG
                H = self.heuristic(neighbour, end)
                F[neighbour] = G[neighbour] + H
    
        raise RuntimeError("A* failed to find a solution")

    def astarXX(self, graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = self.heuristic(start, goal)
        w = len(graph[0])
        h = len(graph)
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in neighbours4(*current, (w, h)):
                cost = graph[next[1]][next[0]]
                if self.TooManyStraight(next, current, came_from):
                    cost = 1000
                new_cost = cost_so_far[current] + cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    
    def astarX(self, graph, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        w = len(graph[0])
        h = len(graph)

        while frontier:
            current = heapq.heappop(frontier)[1]
            if current == goal:
                break

            for next in neighbours4(*current, (w, h)):
                cost = graph[next[1]][next[0]]
                if self.TooManyStraight(next, current, came_from):
                    cost = 1000
                new_cost = cost_so_far[current] + cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def CreatePng(self, grid, path, pngname: str) -> None:
        w = len(grid[0])
        h = len(grid)
        boxsize = 5
        canvas = Canvas(w * boxsize, h * boxsize)

        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                cc = 255 // 10 * c
                if cc > 255: cc = 255
                if cc < 0: cc = 0
                if (x, y) in path:
                    color = (cc, 0, 0)
                else:
                    color = (cc, cc, cc)
                canvas.set_big_pixel(x * boxsize, y * boxsize, color, boxsize)

        print(f"Saving {pngname}")
        canvas.save_PNG(pngname)

    # class Node():
    #     def __init__(self, pos, cost):
    #         self.pos = pos
    #         self.children = []  # [ ((x, y), cost), ... ]
    #         self.parent = None
    #         self.cost = cost

    #     def __str__(self) -> str:
    #         s = f"({self.pos[0]},{self.pos[1]}) [{self.cost}]"
    #         if self.parent is not None:
    #             s += f" <-- ({self.parent.pos[0]},{self.parent.pos[1]})"
    #         for c in self.children:
    #             s += f"\n  C: ({c.pos[0]},{c.pos[1]}) [{c.cost}]"
    #         return s
        
    # def FindPath(self, graph, start, goal):
    #     seen = {}
    #     w = len(graph[0])
    #     h = len(graph)
    #     q = [start]
    #     seen[start] = self.Node(start, 0)
    #     closed = []
    #     while len(q) > 0:
    #         current = q.pop()
    #         closed.append(closed)
    #         for next in neighbours4(*current, (w, h)):
    #             if next in closed:
    #                 continue
    #             cost = graph[next[1]][next[0]]
    #             if next not in seen:
    #                 nn = self.Node(next, cost + seen[current].cost)
    #                 nn.parent = seen[current]

    #                 seen[current].children.append(nn)
    #             else:

    #                 q.append(next)
    #                 seen[next] = nn
    #     print("Done")
    #     g = seen[goal]
    #     print(g)
    #     a = input()
    #     return None

    def PartA(self):
        self.StartPartA()

        data = self.ParseInput()
        w = len(data[0])
        h = len(data)
        # path = self.FindPath(data, (0, 0), (w - 1, h - 1))
        # path = self.astarXX(data, (0, 0), (w - 1, h - 1))
        path = self.astarXXX(data, (w - 1, h - 1), (0,0))
        # path = DoDijkstra(data)
        self.CreatePng(data, path, "day17a.png")
        answer = 0
        for x, y in path[1:]:
            answer += data[y][x]
        print(path)

        # Attempt 1: 1143 is too high
        # Attempt 2: 1012 is too high
        # Attempt 3: 1004 is too high
        # Attempt 4: 986 is wrong
        # Attempt 5: 983 is wrong

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        data = self.ParseInput()
        answer = None

        # Add solution here

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day17Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5

