from collections import deque


class Vertex:
    """顶点类"""

    def __init__(self, val: int):
        self.val = val


def vals_to_vets(vals: list[int]) -> list["Vertex"]:
    """输入值列表 vals ，返回顶点列表 vets"""
    return [Vertex(val) for val in vals]


class GraphAdjList:
    """基于邻接表实现的无向图类"""

    def __init__(self, edges: list[list[Vertex]]):
        """构造方法"""
        self.adj_list = dict[Vertex, list[Vertex]]()
        for edge in edges:
            self.add_vertex(edge[0])
            self.add_vertex(edge[1])
            self.add_edge(edge[0], edge[1])

    def add_edge(self, vet1: Vertex, vet2: Vertex):
        """添加边"""
        if vet1 not in self.adj_list or vet2 not in self.adj_list or vet1 == vet2:
            raise ValueError()
        self.adj_list[vet1].append(vet2)
        self.adj_list[vet2].append(vet1)

    def add_vertex(self, vet: Vertex):
        """添加顶点"""
        if vet in self.adj_list:
            return
        self.adj_list[vet] = []


def graph_bfs(graph: GraphAdjList, start_vet: Vertex) -> list[Vertex]:
    """广度优先遍历"""
    # 顶点遍历序列
    res = []
    # 哈希表，用于记录已被访问过的顶点
    visited = set[Vertex]([start_vet])
    # 队列用于实现 BFS
    que = deque[Vertex]([start_vet])
    # 以顶点 vet 为起点，循环直至访问完所有顶点
    while len(que) > 0:
        vet = que.popleft()  # 队首顶点出队
        res.append(vet)  # 记录访问顶点
        # 遍历该顶点的所有邻接顶点
        for adj_vet in graph.adj_list[vet]:
            if adj_vet in visited:
                continue  # 跳过已被访问的顶点
            que.append(adj_vet)  # 只入队未访问的顶点
            visited.add(adj_vet)  # 标记该顶点已被访问
    # 返回顶点遍历序列
    return res


"""Driver Code"""
if __name__ == "__main__":
    # 初始化无向图
    v = vals_to_vets([0, 1, 2, 3, 4])
    edges = [
        [v[0], v[1]],
        [v[0], v[3]],
        [v[1], v[2]],
        [v[1], v[4]],
        [v[3], v[4]],
    ]
    graph = GraphAdjList(edges)
    del edges

    # 广度优先遍历
    res = graph_bfs(graph, v[0])
