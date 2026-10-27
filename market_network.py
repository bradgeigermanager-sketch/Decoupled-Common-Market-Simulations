
import networkx as nx
import numpy as np

class MarketNetwork:
    """
    基于图论的市场参与者网络建模。
    节点代表经纪人(Brokers)和采购方(Purchasers)，边代表交易关系。
    """
    def __init__(self, n_brokers=10, n_purchasers=50, connection_prob=0.1):
        self.n_brokers = n_brokers
        self.n_purchasers = n_purchasers
        self.connection_prob = connection_prob
        self.graph = nx.Graph()
        self._build_network()

    def _build_network(self):
        """构建二分图或复杂网络结构"""
        # 添加经纪人节点
        brokers = [f"Broker_{i}" for i in range(self.n_brokers)]
        purchasers = [f"Purchaser_{i}" for i in range(self.n_purchasers)]
        
        self.graph.add_nodes_from(brokers, bipartite=0, type='broker')
        self.graph.add_nodes_from(purchasers, bipartite=1, type='purchaser')
        
        # 随机建立连接，模拟市场交互
        for b in brokers:
            for p in purchasers:
                if np.random.rand() < self.connection_prob:
                    weight = np.random.exponential(scale=1.0) # 交易强度权重
                    self.graph.add_edge(b, p, weight=weight)

    def get_adjacency_matrix(self):
        """获取邻接矩阵，用于后续数值计算"""
        nodes = list(self.graph.nodes())
        return nx.to_numpy_array(self.graph, nodelist=nodes)

    def get_node_degrees(self):
        """获取节点度分布，分析中心性"""
        return dict(self.graph.degree())

    def visualize_structure(self):
        """返回网络结构摘要，实际项目中可集成matplotlib可视化"""
        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph)
        }
