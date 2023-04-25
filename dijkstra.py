class Vertex:
    def __init__(self, name) -> None:
        self.name = name
        self.dist = 1000000
        self.outgoing = []

class Edge:
    def __init__(self, head, length) -> None:
        self.head = head
        self.length = length

def createGraph(filename):
    n = 0
    with open(filename, 'r') as file:
        for line in file:
            n += 1
        file.seek(0)
        V = [Vertex(x+1) for x in range(n)]
        for line in file:
            items = line.split()
            v = V[int(items[0])-1]
            for item in items[1:]:
                head, length = item.split(',')
                v.outgoing.append(Edge(V[int(head)-1], int(length)))
    return V

def printGraph(V):
    for v in V:
        for e in v.outgoing:
            print('Node', v.name, 'points to node', e.head.name)
    return


filename = "small_input.txt"
V = createGraph(filename)
printGraph(V)
