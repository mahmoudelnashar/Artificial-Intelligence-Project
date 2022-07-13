import queue as q


def BFS(adjList, start, Goals):
    # set of visited nodes to prevent loops and queue for the fringe and dictionary to find the path to goal
    visited = set()
    visited_list = []
    fringe = q.Queue()
    parent = dict()
    # first we put the start in fringe and specify that it has no parent
    fringe.put(start)
    parent[start] = None
    path_found = False

    while not fringe.empty():
        current_node = fringe.get()
        while current_node in visited:
            current_node = fringe.get()
        # check if the current node is the goal before expanding it
        if current_node in Goals:
            path_found = True
            visited_list.append(current_node)
            break
        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if n not in visited:
                fringe.put(n)
                if n not in parent:
                    parent[n] = [current_node]
                else:
                    parent[n].append(current_node)
        # add the current node to the list of visited nodes
        visited.add(current_node)
        visited_list.append(current_node)


    # getting the solution path
    path = []
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            for p in visited_list:
                if p in parent[current_node]:
                    path.append(p)
                    current_node=p
                    break
        path.reverse()
    return path, visited_list


def DFS(adjList, start, Goals):
    # set of visited nodes to prevent loops and queue for the fringe and dictionary to find the path to goal
    visited = set()
    visited_list=[]
    fringe = []
    parent = dict()
    # first we put the start in fringe and specify that it has no parent
    fringe.append(start)
    parent[start] = None

    path_found = False
    while bool(fringe):
        current_node = fringe.pop()
        while current_node in visited:
            current_node = fringe.pop()
        # check if the current node is the goal before expanding it
        if current_node in Goals:
            path_found = True
            visited_list.append(current_node)
            break
        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if n not in visited:
                fringe.append(n)
                parent[n] = current_node
        # add the current node to the list of visited nodes
        visited.add(current_node)
        visited_list.append(current_node)

    # getting the solution path
    path = []
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            path.append(parent[current_node])
            current_node = parent[current_node]
        path.reverse()
    return path, visited_list


def UCS(adjList, start, Goals):
    # set of visited nodes, the parent to trace the solution path, and list of fringe
    # which will be sorted periodically based on the path cost
    visited = set()
    visited_list = []
    parent = dict()
    fringe = [(start, 0, None)]
    parent[start] = None
    path_found = False
    while fringe:
        # step1 sort the fringe to get the node with the least cost
        fringe.sort(key=lambda x: x[1])
        # get the node that is supposed to be explored
        current_node = fringe[0]
        del fringe[0]
        # check that current node isn't visited
        while current_node[0] in visited:
            fringe.sort(key=lambda x: x[1])
            current_node = fringe[0]
            del fringe[0]
        # check if the current node is in the goal list
        if current_node[0] in Goals:
            path_found = True
            visited_list.append(current_node[0])
            break

        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node[0]:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if n not in visited:
                fringe.append((n, current_node[1] + weight, current_node[0]))
        # add the current node to the list of visited nodes
        visited.add(current_node[0])
        visited_list.append(current_node[0])
        parent[current_node[0]] = current_node[2]
    # getting the solution path
    path = [current_node[0]]
    current_node = current_node[2]
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            path.append(parent[current_node])
            current_node = parent[current_node]
        path.reverse()
    return path, visited_list


def GreedySearch(nodeList, adjList, start, Goals):
    # convert the list of tuples into a dictionary
    Heuristic = dict(nodeList)
    # set of visisted nodes, the parent to trace the solution path, and list of fringe
    # which will be sorted periodically based on the path cost
    visited = set()
    visited_list = []
    parent = dict()
    fringe = [(start, Heuristic[start], None)]
    path_found = False
    while fringe:
        # step1 sort the fringe to get the node with the least cost
        fringe.sort(key=lambda x: x[1])
        # get the node that is supposed to be explored
        current_node = fringe[0]
        del fringe[0]
        # check that current node isn't visited
        while current_node[0] in visited:
            fringe.sort(key=lambda x: x[1])
            current_node = fringe[0]
            del fringe[0]
        # check if the current node is in the goal list
        if current_node[0] in Goals:
            path_found = True
            visited_list.append(current_node[0])
            break

        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node[0]:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if n not in visited:
                fringe.append((n, Heuristic[n], current_node[0]))
        # add the current node to the list of visited nodes
        visited.add(current_node[0])
        visited_list.append(current_node[0])
        parent[current_node[0]] = current_node[2]
    # getting the solution path
    path = [current_node[0]]
    current_node = current_node[2]
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            path.append(parent[current_node])
            current_node = parent[current_node]
        path.reverse()
    return path, visited_list


def AstarSearch(nodeList, adjList, start, Goals):
    # convert the list of tuples into a dictionary
    Heuristic = dict(nodeList)
    # set of visisted nodes, the parent to trace the solution path, and list of fringe
    # which will be sorted periodically based on the path cost
    visited = set()
    visited_list = []
    parent = dict()
    fringe = [(start, 0, None, Heuristic[start])]
    path_found = False
    while fringe:
        # step1 sort the fringe to get the node with the least cost
        fringe.sort(key=lambda x: x[3])
        # get the node that is supposed to be explored
        current_node = fringe[0]
        del fringe[0]
        # check that current node isn't visited
        while current_node[0] in visited and parent[current_node[0]] == current_node[2]:
            fringe.sort(key=lambda x: x[3])
            current_node = fringe[0]
            del fringe[0]
        # check if the current node is in the goal list
        if current_node[0] in Goals:
            path_found = True
            visited_list.append(current_node[0])
            break

        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node[0]:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if (n not in visited) or parent[n] != current_node[0]:  # this condition must be added
                fringe.append((n, current_node[1] + weight, current_node[0], current_node[1] + weight + Heuristic[n]))
        # add the current node to the list of visited nodes
        visited.add(current_node[0])
        visited_list.append(current_node[0])
        parent[current_node[0]] = current_node[2]
    # getting the solution path
    path = [current_node[0]]
    current_node = current_node[2]
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            path.append(parent[current_node])
            current_node = parent[current_node]
        path.reverse()
    return path, visited_list


def IDS(adjList, start, Goals):
    visited2 = set()
    visited_list1 = []
    for depth in range(0, 1000):
        path, visited_list, visited = DLS(adjList, start, Goals, depth)
        visited = set(visited)
        visited2 |= visited
        visited_list1.extend(visited_list)
        if path is not None:
            visited2 = list(visited2)
            return path, visited2, visited_list1


def DLS(adjList, start, Goals, Limit):
    # set of visited nodes to prevent loops and queue for the fringe and dictionary to find the path to goal
    visited = set()
    visited_list = []
    fringe = []
    parent = dict()
    # first we put the start in fringe and specify that it has no parent
    fringe.append((start, 0))
    parent[start] = None
    path_found = False
    while bool(fringe):
        current_node = fringe.pop()
        while (current_node[0] in visited) or (
                current_node[1] > Limit):  # this added condition is to remove nodes that are beyond the wanted depth
            if fringe:
                current_node = fringe.pop()
            else:
                return None, visited_list,visited
        # check if the current node is the goal before expanding it
        if current_node[0] in Goals:
            path_found = True
            visited_list.append(current_node[0])
            break
        # getting the children list of the current node
        children_list = []
        for e in adjList:
            if e[0] == current_node[0]:
                children_list = e[1]
                break
        for (n, weight) in children_list:
            if n not in visited:
                fringe.append((n, current_node[1] + 1))
                parent[n] = current_node[0]
        # add the current node to the list of visited nodes
        visited.add(current_node[0])
        visited_list.append(current_node[0])
    if not path_found:
        return None, visited_list, visited
    # getting the solution path
    path = []
    current_node = current_node[0]
    if path_found:
        path.append(current_node)
        while parent[current_node] is not None:
            path.append(parent[current_node])
            current_node = parent[current_node]
        path.reverse()
    return path, visited_list, visited


# =====================================================Tests============================================================
def TestBFS():
    adj = [('Sibiu', [('Fagaras', 99), ('Rimnicu', 80)]),
           ('Fagaras', [('Bucharest', 211), ('Sibiu', 99)]),
           ('Rimnicu', [('Pitesti', 97), ('Sibiu', 80)]),
           ('Pitesti', [('Rimnicu', 97), ('Bucharest', 101)]),
           ('Bucharest', [('Pitesti', 101), ('Fagaras', 211)])]
    start = 'Sibiu'
    goal = ['Bucharest']
    path, visited = BFS(adj, start, goal)
    print(path)
    print(visited)


def TestDFS():
    adj = [('A', [('B', 99), ('C', 80)]),
           ('B', [('D', 211), ('E', 99)]),
           ('C', [('F', 97), ('G', 80)]),
           ('D', [('H', 97), ('I', 101)]),
           ('E', [('J', 101), ('K', 211)]),
           ('F', [('L', 97), ('M', 80)]),
           ('G', [('N', 97), ('O', 80)])]
    start = 'A'
    goal = ['B', 'M']
    path, visited = DFS(adj, start, goal)
    print(path)
    print(visited)


def TestUCS():
    adj = [('A', [('B', 3), ('G1', 9)]),
           ('B', [('A', 2), ('C', 1)]),
           ('C', [('S', 6), ('G2', 5), ('F', 7)]),
           ('D', [('C', 2), ('E', 2), ('S', 1)]),
           ('E', [('G3', 7)]),
           ('F', [('D', 2), ('G3', 8)]),
           ('S', [('A', 5), ('B', 9), ('D', 6)]),
           ('G1', []),
           ('G2', []),
           ('G3', [])]
    start = 'S'
    goal = ['G1', 'G2', 'G3']
    path, visited = UCS(adj, start, goal)
    print(path)
    print(visited)


def TestGreedy():
    nodeList = [('A', 5),
                ('B', 6),
                ('C', 7),
                ('D', 2),
                ('E', 1),
                ('S', 6),
                ('G', 0)]
    adjList = [('A', [('B', 1), ('D', 3), ('E', 8)]),
               ('B', [('C', 1)]),
               ('C', []),
               ('D', [('G', 2)]),
               ('E', [('D', 1)]),
               ('S', [('A', 1)]),
               ('G', [])]
    start = 'S'
    goal = ['G']
    path, visited = GreedySearch(nodeList, adjList, start, goal)
    print(path)
    print(visited)


def TestGreedy2():
    nodeList = [('A', 90),
                ('B', 100),
                ('C', 120),
                ('D', 180),
                ('G', 0)]
    adjList = [('A', [('B', 10), ('C', 1000)]),
               ('B', [('D', 20), ('A', 10)]),
               ('C', [('A', 1000), ('G', 500)]),
               ('D', [('B', 20), ('G', 30)]),
               ('G', [('C', 500), ('D', 30)])]
    start = 'A'
    goal = ['G']
    path, visited = GreedySearch(nodeList, adjList, start, goal)
    print(path)
    print(visited)


def TestAstarSearch():
    nodeList = [('A', 4),
                ('B', 1),
                ('C', 1),
                ('S', 2),
                ('G', 0)]
    adjList = [('A', [('C', 1)]),
               ('B', [('C', 2)]),
               ('C', [('G', 3)]),
               ('S', [('B', 1), ('A', 1)]),
               ('G', [])]
    start = 'S'
    goal = ['G']
    path, visited = AstarSearch(nodeList, adjList, start, goal)
    print(path)
    print(visited)


def TestIDS():
    adjList = [('A', [('B', 1), ('C', 1)]),
               ('B', [('D', 2), ('E', 1)]),
               ('C', [('F', 3), ('G', 1)]),
               ('D', [('H', 1), ('I', 1)]),
               ('E', [('J', 1), ('K', 1)]),
               ('F', [('L', 1), ('M', 1)]),
               ('G', [('N', 1), ('O', 1)]),
               ('H', []),
               ('I', []),
               ('J', []),
               ('K', []),
               ('L', []),
               ('M', []),
               ('N', []),
               ('O', [])]
    start = 'A'
    goal = ['D', 'M']
    path, trash,visited = IDS(adjList, start, goal)
    print(path)
    print(visited)

def TestBFS2():
    adj = [('S', [('B', 99), ('C', 80),('D',99)]),
               ('B', [('S', 211), ('E', 99)]),
               ('C', [('S', 97), ('G', 80)]),
               ('D', [('S', 97)]),
               ('E', [('F', 97),('B', 97), ('G', 101)],),
               ('F', [('E', 101), ('G',21)])]
    start = 'S'
    goal = ['G']
    path, visited = BFS(adj, start, goal)
    print(path)
    print(visited)


def TestIDS2():
    adj = [('S', [('B', 99), ('C', 80),('D',99)]),
               ('B', [('S', 211), ('E', 99)]),
               ('C', [('S', 97), ('G', 80)]),
               ('D', [('S', 97)]),
               ('E', [('F', 97),('B', 97), ('G', 101)],),
               ('F', [('E', 101), ('G',21)])]
    start = 'S'
    goal = ['G']
    path, trash, visited = IDS(adj, start, goal)
    print(path)
    print(visited)

def TestIDS3():
    adj = [('S', [('A', 3), ('B', 2)]),
               ('A', [('C', 4), ('D', 1)]),
               ('B', [('E', 3), ('F', 1)]),
               ('E', [('H', 5)]),
               ('F', [('I', 2), ('G', 3)])]
    start = 'S'
    goal = ['G']
    path, trash, visited = IDS(adj, start, goal)
    print(path)
    print(visited)


def TestDFS1():
    adjList = [('A', [('B', 1), ('F', 1)]),
               ('B', [('A', 2), ('C', 2),('D', 1)]),
               ('C', [('B', 3), ('D', 2), ('E', 1)]),
               ('D', [('B', 1), ('C', 2), ('E', 1)]),
               ('E', [('C', 1), ('D', 2), ('J', 2), ('I', 1)]),
               ('F', [('A', 1), ('G', 2), ('H', 1)]),
               ('G', [('F', 1), ('I', 1)]),
               ('H', [('F', 2), ('I', 1)]),
               ('I', [('G', 3), ('H', 2), ('E', 2), ('J', 1)]),
               ('J', [('E', 1), ('I', 1)])]
    start = 'A'
    goal = ['J']
    path, visited = DFS(adjList, start, goal)
    print(path)
    print(visited)

