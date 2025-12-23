class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, i):
            root = i
            while root != self.parent[root]:
                root = self.parent[root]
            
            curr = i
            while curr != root:
                next_node = self.parent[curr]
                self.parent[curr] = root
                curr = next_node
                
            return root

    def union(self, i, j):
        ri = self.find(i)
        rj = self.find(j)
        if ri == rj:
            return False
        if self.rank[ri] < self.rank[rj]:
            self.parent[ri] = rj
        elif self.rank[ri] > self.rank[rj]:
            self.parent[rj] = ri
        else:
            self.parent[rj] = ri
            self.rank[ri] += 1
        return True


class UnionFindSimples:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}

    def find(self, i):
        while self.parent[i] != i:
            i = self.parent[i]
        return i

    def union(self, i, j):
        ri = self.find(i)
        rj = self.find(j)
        if ri == rj:
            return False
        self.parent[rj] = ri
        return True
