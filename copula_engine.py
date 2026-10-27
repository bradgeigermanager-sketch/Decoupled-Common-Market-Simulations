
import numpy as np
from scipy import stats

class CopulaEngine:
    """
    Copula引擎，用于生成具有特定依赖结构的均匀分布随机变量。
    支持高斯Copula和t-Copula。
    """
    def __init__(self, corr_matrix, copula_type='gaussian', df=4):
        """
        :param corr_matrix: 相关系数矩阵
        :param copula_type: 'gaussian' 或 't'
        :param df: t-Copula的自由度，仅当copula_type='t'时有效
        """
        self.corr_matrix = np.asarray(corr_matrix)
        self.copula_type = copula_type
        self.df = df
        self.dim = self.corr_matrix.shape[0]
        
        # 预计算分解矩阵以提高采样效率
        if self.copula_type == 'gaussian':
            self.L = np.linalg.cholesky(self.corr_matrix)
        elif self.copula_type == 't':
            # t-Copula采样需要更复杂的步骤，此处简化为使用多元t分布生成后转换
            pass
        else:
            raise ValueError("Unsupported copula type")

    def sample_uniform(self, n_samples):
        """
        从Copula分布中采样，返回[0,1]之间的均匀分布变量
        """
        if self.copula_type == 'gaussian':
            # 1. 生成标准正态分布随机数
            Z = np.random.standard_normal((n_samples, self.dim))
            # 2. 引入相关性
            correlated_Z = Z @ self.L.T
            # 3. 通过正态CDF转换为均匀分布 U ~ Uniform(0,1)
            U = stats.norm.cdf(correlated_Z)
            return U
        
        elif self.copula_type == 't':
            # 1. 生成多元t分布随机数
            # scipy没有直接的多维t采样，这里使用简化方法：
            # 生成标准正态，除以卡方分布的平方根
            Z = np.random.standard_normal((n_samples, self.dim))
            chi2 = np.random.chisquare(self.df, n_samples)
            # 广播机制调整维度
            scale = np.sqrt(self.df / chi2).reshape(-1, 1)
            T_vars = Z @ np.linalg.cholesky(self.corr_matrix).T * scale
            
            # 2. 通过t分布CDF转换为均匀分布
            U = stats.t.cdf(T_vars, df=self.df)
            return U

    def calculate_kendall_tau(self):
        """计算理论Kendall's Tau，用于验证依赖结构"""
        if self.copula_type == 'gaussian':
            return 2 * np.arcsin(self.corr_matrix) / np.pi
        elif self.copula_type == 't':
            return 2 * np.arcsin(self.corr_matrix) / np.pi # 近似
        return None
