from decoupled_commons.simulation import MarketSimulationEngine
from decoupled_commons.visualization import plot_simulation_results

if __name__ == '__main__':
    print("Initializing Decoupled Market Simulation...")
    sim = MarketSimulationEngine(num_brokers=100, num_purchasers=100, periods=150)
    results = sim.run()
    print("Simulation complete. Rendering analytical plots...")
    plot_simulation_results(results)
