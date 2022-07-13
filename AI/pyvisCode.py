from pyvis.network import Network

def pyvisGraphGenerator(filename, nodesList, edges, mode, goals=None, visited=None, path=None):
    # creating a graph based on the graph type
    if mode == 'u':
        nt = Network(height='725px', width='875px', directed=False)
    else:
        nt = Network(height='725px', width='875px', directed=True)
    # specifying the color of nodes and getting a list for nodes and heuristics

    colour_map = []
    nodes = []
    heuristic = []
    order = []
    i = 0
    for (node, nodeHeuristic) in nodesList:
        if path is not None and node in path:
            colour_map.append('Green')
        elif visited is not None and node in visited:
            colour_map.append('Red')
        elif goals is not None and node in goals:
            colour_map.append('Blue')
        else:
            colour_map.append('Orange')

        nodes.append(node)
        heuristic.append(str(nodeHeuristic))
        i += 1
        order.append(i)
    # add the nodes to the graph
    nt.add_nodes(nodes=order, title=heuristic, label=nodes, color=colour_map)
    # mapping node names
    nodemap = {nodes[i]: order[i] for i in range(len(nodes))}
    # add edges to the graph
    for (s, e, w) in edges:
        nt.add_edge(nodemap[s], nodemap[e], title=w)
    nt.set_edge_smooth("dynamic")
    # first need to be commented
    nt.save_graph(filename)


def legend_creator(filename):
    nt = Network(height='185px', width='185px')
    nt.add_nodes([0, 1, 2, 3], value=[15, 15, 15, 15],
                 title=['not visited', 'goal', 'visited', 'in solution path'],
                 label=['Default', 'Goal', 'Visited', 'In Path'],
                 color=['Orange', 'Blue', 'Red', 'Green'])
    nt.save_graph(filename)


def test():
    nodes = [('A', 50),
             ('B', 50),
             ('C', 50),
             ('D', 50),
             ('E', 50),
             ('F', 50),
             ('G', 50),
             ('H', 50)]
    edges = [('A', 'B', 9),
             ('B', 'A', 4),
             ('A', 'C', 5),
             ('B', 'D', 20),
             ('B', 'F', 12),
             ('F', 'H', 3),
             ('C', 'E', 100),
             ('C', 'G', 150)]
    goals = ['G', 'H']
    visited = ['A', 'B', 'F', 'C', 'D']
    path = ['A', 'B', 'F', 'H']
    pyvisGraphGenerator("Graph.html", nodes, edges, 'd', goals, visited, path)
