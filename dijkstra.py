class Vertex:
    def __init__(self, name, dist=1000000) -> None:
        self.name = name
        self.dist = dist
        self.incoming = []
        self.outgoing = []

class Edge:
    def __init__(self, tail, head, length) -> None:
        self.tail = tail
        self.head = head
        self.length = length
        self.heapIndex = None

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
                h, length = item.split(',')
                e = Edge(v, V[int(h)-1], int(length))
                v.outgoing.append(e)
                e.head.incoming.append(e)
    return V

def dijkstra(V, s):
    s.dist = 0
    # initialize X with s
    X = {s}
    # initialize the heap 
    heap = []
    for e in s.outgoing:
        e.head.dist = s.dist + e.length
        heapInsert(heap, e)
    #print('initialized s, printing heap')
    #printHeap(heap)
    # repeat until X includes all vertices
    while heap:
        w = heapExtract(heap).head
        #print('after extraction in main loop, printing heap')
        #printHeap(heap)
        X.add(w)
        for e in w.outgoing:
            #print('e:', e.tail.name, '=>', e.head.name, 'e index:', e.heapIndex)
            v = e.head
            if v not in X and (w.dist + e.length) < v.dist: # got better path to v thru w
                # delete old edge to v from heap (if it exists)
                for f in v.incoming:
                    #print('f:', f.tail.name, '=>', f.head.name, 'f index:', f.heapIndex)
                    if f.heapIndex != None:
                        #print('heapIndex:', f.heapIndex)
                        #printHeap(heap)
                        heapDelete(heap, f.heapIndex)
                # insert the better edge into the heap and update v's dist
                heapInsert(heap, e)
                v.dist = w.dist + e.length
            #print('end of for loop, printing heap')
            #printHeap(heap)
    return

def sink(heap, p):
    parent = heap[p]
    while True:
        # find minimum child
        c1 = 2*p + 1
        c2 = 2*p + 2
        if c1 < len(heap) and (c2 >= len(heap) or \
                               heap[c1].head.dist < heap[c2].head.dist):
            c = c1
        elif c2 < len(heap):
            c = c2
        else:
            break
        # if parent is greater than the min child, swap with the min child
        if parent.head.dist > heap[c].head.dist:
            heapSwap(heap, p, c)
            p = c
            parent = heap[p]
        # else parent is already the min, leave as is
        else:
            break
    return

def swim(heap, c):
    while True:
        p = max((c-1) // 2, 0)
        if heap[c].head.dist < heap[p].head.dist:
            heapSwap(heap, p, c)
            c = p
        else:
            break
    return

def heapDelete(heap, i):
    heapSwap(heap, i, len(heap)-1)
    deleted = heap.pop()
    deleted.heapIndex = None
    if not heap:
        return
    p = max((i-1) // 2, 0)
    c1 = 2*i + 1
    c2 = 2*i + 2
    if heap[i].head.dist < heap[p].head.dist:
        swim(heap, i)
    elif (c1 < len(heap) and heap[i].head.dist > heap[c1].head.dist) or \
         (c2 < len(heap) and heap[i].head.dist > heap[c2].head.dist):
        sink(heap, i)
    return

def heapExtract(heap):
    heapSwap(heap, 0, len(heap)-1)
    extracted = heap.pop()
    extracted.heapIndex = None
    if not heap:
        return extracted
    sink(heap, 0)
    return extracted

def heapInsert(heap, child):
    heap.append(child)
    c = len(heap)-1
    child.heapIndex = c
    swim(heap, c)
    return

def heapSwap(heap, i, j):
    heap[i].heapIndex = j
    heap[j].heapIndex = i
    temp = heap[i]
    heap[i] = heap[j]
    heap[j] = temp
    return

def printGraph(V):
    for v in V:
        for e in v.outgoing:
            print('Node', v.name, 'Edge:', e.tail.name, '=>', e.head.name)
    return

def printHeap(heap):
    for edge in heap:
        print('Edge', edge.tail.name, "=>", edge.head.name, 'Dist =', edge.head.dist)
    print('\n')
    return

def printDists(V):
    for v in V:
        print('Node', v.name, '... Dist from s:', v.dist)
    return

filename = "small_input.txt"
V = createGraph(filename)
# printGraph(V)
dijkstra(V, V[0])
printDists(V)


# test = [Vertex(1), Vertex(2,423), Vertex(3,233), Vertex(4, 93), Vertex(5, 2)]