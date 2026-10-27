
import numpy as np
import pandas as pd
from market_network import MarketNetwork
from copula_engine import CopulaEngine
from marginal_models import MarginalModel

class DecoupledMarketSimulator:
    """
    解耦共同市场模拟器：
    1. 构建市场网络
    2. 定义资产边缘分布
    3. 定义资产间依赖结构(Copula)
    4. 执行蒙特卡洛模拟
    """
    def __init__(self, n_assets=5, n_simulations=10000, copula_type='t'):
        self.n_assets = n_assets
        self.n_simulations = n_simulations
        self.copula_type = copula_type
        
        # 1. 初始化市场网络 (此处简化为资产间的关联，实际可扩展为网络拓扑影响相关性)
        self.network = MarketNetwork(n_brokers=5, n_purchasers=20)
        
        # 2. 定义相关系数矩阵 (假设资产间存在中等正相关)
        base_corr = 0.5
        self.corr_matrix = np.full((n_assets, n_assets), base_corr)
        np.fill_diagonal(self.corr_matrix, 1.0)
        
        # 3. 初始化Copula引擎
        self.copula = CopulaEngine(self.corr_matrix, copula_type=copula_type, df=4)
        
        # 4. 定义每个资产的边缘分布 (例如：正态分布，均值0，波动率不同)
        self.marginals = []
        volatilities = [0.02, 0.03, 0.015, 0.025, 0.04] # 不同资产的波动率
        for v in volatilities:
            self.marginals.append(MarginalModel(dist_type='norm', params={'loc': 0.0005, 'scale': v}))

    def run_simulation(self):
        """
        执行模拟并返回结果
        """
        print(f"Starting simulation with {self.n_simulations} paths for {self.n_assets} assets...")
        
        # 1. 从Copula生成均匀分布变量 (N_samples, N_assets)
        uniform_vars = self.copula.sample_uniform(self.n_simulations)
        
        # 2. 通过边缘分布逆变换生成实际收益
        simulated_returns = np.zeros((self.n_simulations, self.n_assets))
        for i, marginal in enumerate(self.marginals):
            simulated_returns[:, i] = marginal.simulate_returns(uniform_vars[:, i])
            
        # 3. 计算组合统计量 (例如等权重组合)
        weights = np.ones(self.n_assets) / self.n_assets
        portfolio_returns = simulated_returns @ weights
        
        results = {
            "asset_returns": simulated_returns,
            "portfolio_returns": portfolio_returns,
            "var_95": np.percentile(portfolio_returns, 5),
            "cvar_95": np.mean(portfolio_returns[portfolio_returns <= np.percentile(portfolio_returns, 5)])
        }
        
        return results

    def summary_report(self, results):
        """
        生成模拟结果摘要
        """
        df_assets = pd.DataFrame(results['asset_returns'], columns=[f"Asset_{i}" for i in range(self.n_assets)])
        print("\n--- Simulation Summary ---")
        print(f"95% VaR (Portfolio): {results['var_95']:.4f}")
        print(f"95% CVaR (Portfolio): {results['cvar_95']:.4f}")
        print("\nAsset Return Statistics:")
        print(df_assets.describe())
        
        return df_assets

if __name__ == "__main__":
    # 实例化模拟器
    simulator = DecoupledMarketSimulator(n_assets=5, n_simulations=5000, copula_type='t')
    
    # 运行模拟
    results = simulator.run_simulation()
    
    # 输出报告
    simulator.summary_report(results)
