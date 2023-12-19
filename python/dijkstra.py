import itertools
from utilities import neighbours4

def BuildGraph(data):

    width = len(data[0])
    height = len(data)
    graph = {}
    costs = {}
    for x, y in itertools.product(range(width), range(height)):

        # if x > width / 3 * 2 and y < height / 3:
        #     continue
        # if y > height / 3 * 2 and x < width / 3:
        #     continue

        costs[(x, y)] = 1e9
        neighbours = {}
        for nx, ny in neighbours4( x, y, (width, height) ):
            neighbours[(nx, ny)] = int(data[ny][nx])
        if len(neighbours) > 0:
            graph[(x, y)] = neighbours

    costs[(0, 0)] = 0
    parents = {}
    return graph, costs, parents

def Dijkstra(source, target, graph, costs, parents):

    nextNode = source

    while nextNode != target:

        for neighbor in graph[nextNode]:

            if graph[nextNode][neighbor] + costs[nextNode] < costs[neighbor]:
                costs[neighbor] = graph[nextNode][neighbor] + costs[nextNode]
                parents[neighbor] = nextNode

            del graph[neighbor][nextNode]

        del costs[nextNode]

        nextNode = min(costs, key=costs.get)

    return parents

def BackPedal(source, target, searchResult):

    node = target
    backpath = [target]
    path = []

    while node != source:
        backpath.append(searchResult[node])
        node = searchResult[node]

    for i in range(len(backpath)):
        path.append(backpath[-i - 1])

    return path

def DoDijkstra(data):

    width = len(data[0])
    height = len(data)

    print("Building Graph")
    graph, costs, parents = BuildGraph(data)

    print("Searching")
    result = Dijkstra((0, 0), (width - 1, height - 1), graph, costs, parents)
    path = BackPedal((0, 0), (width - 1, height - 1), result)
    return path
