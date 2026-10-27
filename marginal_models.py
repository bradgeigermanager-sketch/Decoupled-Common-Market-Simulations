
import numpy as np
from scipy import stats

class MarginalModel:
    """
    定义单个资产的边缘分布，并提供概率积分变换(PIT)和逆变换功能。
    """
    def __init__(self, dist_type='norm', params=None):
        """
        :param dist_type: 分布类型，如 'norm', 't', 'lognorm'
        :param params: 分布参数字典，例如 {'loc': 0, 'scale': 1}
        """
        self.dist_type = dist_type
        self.params = params if params else {}
        self.dist = self._get_distribution()

    def _get_distribution(self):
        if self.dist_type == 'norm':
            return stats.norm(**self.params)
        elif self.dist_type == 't':
            return stats.t(**self.params)
        elif self.dist_type == 'lognorm':
            return stats.lognorm(**self.params)
        else:
            raise ValueError(f"Unsupported distribution: {self.dist_type}")

    def inverse_cdf(self, u):
        """
        逆累积分布函数 (PPF)，将均匀分布变量U映射回实际收益值
        """
        return self.dist.ppf(u)

    def simulate_returns(self, u_values):
        """
        根据输入的均匀分布变量生成模拟收益
        """
        return self.inverse_cdf(u_values)
