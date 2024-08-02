import copy
import queue
import heapq
from sortedcontainers import SortedDict

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.NodeCnt = 0  # 노드의 카운트
        self.EdgeCnt = 0  # 연결된 하이퍼에지 ID를 저장하는 set
        self.Edge = set()  # 연결된 하이퍼에지를 저장하는 set

class Hypergraph:
    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}

    def add_hyperedge(self, edge_nodes):
        hyperedge_id = len(self.hyperedges) + 1
        self.hyperedges[hyperedge_id] = edge_nodes #각 hyperedge에 노드id set저장됨.

        for node in edge_nodes:
            if node not in self.nodes:
                self.nodes[node] = Node(node)
            self.nodes[node].Edge.add(hyperedge_id)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:

                current_nodes = {int(node.strip()) for node in line.strip().split(',')}

                self.add_hyperedge(current_nodes) #노드 id들을 set으로 추가.

    def del_node(self, node):
        if node in self.nodes:
            for hyperedge in self.nodes[node].Edge:
                self.hyperedges[hyperedge].remove(node)
            del self.nodes[node]

    def del_edge(self, edge):
        if edge in self.hyperedges:
            for node in self.hyperedges[edge]:
                self.nodes[node].Edge.remove(edge)
            del self.hyperedges[edge]   


class PriorityQueue:
    def __init__(self):
        self.data = SortedDict()
        self.node_to_priority = {}  # 노드를 키로, 해당 노드의 우선순위를 값으로 하는 dict

    # @profile
    def push(self, node, priority):
        # 우선순위를 키로 사용하여 노드를 추가
        if priority not in self.data:
            self.data[priority] = set()
        self.data[priority].add(node)
        self.node_to_priority[node] = priority
        # self.show()

    # @profile
    def pop(self):
        # 가장 높은 우선순위의 노드를 반환하고 제거
        if not self.data:
            raise IndexError("pop from empty priority queue")
        highest_priority = self.data.peekitem(-1)[0] #tuple 반환하니까 그 앞에 key
        node = self.data[highest_priority].pop()
        del self.node_to_priority[node]
        if not self.data[highest_priority]:
            del self.data[highest_priority]
        return node

    # @profile
    def remove(self, node):
        # 특정 노드의 우선순위를 찾아서 노드를 제거 contain을 확인 한 후에 사용함.
        priority = self.node_to_priority[node]
        nodes = self.data[priority]
        nodes.remove(node)
        if not nodes:
            del self.data[priority]
        del self.node_to_priority[node]

    # @profile
    def empty(self):
        # 큐가 비어있는지 확인
        return len(self.data) == 0

    # @profile
    def contains(self, node):
        # 특정 노드가 큐에 있는지 확인
        return node in self.node_to_priority

# @profile
def getNbrMap(G, node, g):
    cnt = {}
    tot_len = 0
    for hyperedge in G.nodes[node].Edge:
        for neighbor in G.hyperedges[hyperedge]:
            if neighbor != node:
                tot_len += 1
                if neighbor not in cnt:
                    cnt[neighbor] = 0
                cnt[neighbor] += 1
    nb_len = len(cnt.keys())
    ng = {node: count for node, count in cnt.items() if count >= g}
    ng_len = len(ng.keys())
    return ng, ng_len, nb_len, tot_len
# @profile
def updatesuptable(ng): #M은 M[v]를 받고 v의 ng임.
    M = {}
    for node in ng:
        occurence = ng[node]
        if occurence not in M:
            M[occurence] = 0
        M[occurence] += 1
    return M

# @profile
def getK(M):
    if len(M) == 0:
        return 0
    sum = 0
    for occurence in M:
        sum += M[occurence]
    return sum
# @profile
def getEdgeLB(v, M, g):
    c = v.EdgeCnt
    # print(f"before M: {M}")
    T = {}
    for s in M:
        if s - c >= g:
            T[s - c] = M[s]
    v.EdgeCnt = 0
    # print(f"after T: {T}, M: {M}")
    return getK(T), T
# @profile
def getNodeLB(v, M): #이것도 v의 object랑 M[v]임.
    c = v.NodeCnt
    keys = list(M.keys())
    keys.sort()#그래서 그냥 sort가 맞음.
    # print(f"nodeLB : v: {v.id}, c: {c}, M : {M}, keys : {keys}")
    while c != 0:
        if len(M) == 0:
            return 0
        mk = keys.pop() #reverse로 하고 pop하면 뒤에서 함. 그
        if c > M[mk]:
            c -= M[mk]
            del M[mk]
        else:
            M[mk] -= c
            if M[mk] == 0:
                del M[mk]
            break
    v.NodeCnt = 0
    # print(f"M: {M}, result : {getK(M)}")
    return getK(M)

def ASAP_kgcore(G, k, g):
    G1 = copy.deepcopy(G)
    S = {}
    VQ = queue.Queue()
    VQ1 = set()
    for node in G1.nodes:
        ng, _, _, _ = getNbrMap(G1, node, g)
        S[node] = len(ng)
        if S[node] < k:
            VQ.put(node)
            VQ1.add(node)
    while not VQ.empty():
        v = VQ.get()
        VQ1.remove(v)
        ng, _, _, _ = getNbrMap(G1, v, g)
        G1.del_node(v)
        del S[v]
        for w in ng:
            if w not in VQ1:
                S[w] -= 1
                if S[w] < k:
                    VQ.put(w)
                    VQ1.add(w)
    return G1, S
