import random
import matplotlib.pyplot as plt

class MarketSimulation:
    def __init__(self, num_brokers=50, num_purchasers=50, periods=100):
        self.num_brokers = num_brokers
        self.num_purchasers = num_purchasers
        self.periods = periods
        
        # State variables
        self.informational_commons = 1.0  # Normalized from 0.0 to 1.0
        self.history = {'commons': [], 'avg_disclosure': [], 'avg_acquisition': []}
        
        # Initialize agents with behavioral traits (e.g., baseline honesty/decoupling)
        self.brokers = [{'id': i, 'disclosure': random.uniform(0.2, 0.8)} for i in range(num_brokers)]
        self.purchasers = [{'id': i, 'decoupling': random.uniform(0.5, 1.0)} for i in range(num_purchasers)]

    def run(self):
        for t in range(self.periods):
            total_disclosure = 0
            total_acquisition = 0
            period_damage = 0
            
            # Interaction loops
            for purchaser in self.purchasers:
                broker = random.choice(self.brokers)
                
                # Dynamic penalty based on current informational commons state
                reputational_penalty = broker['disclosure'] * self.informational_commons
                
                # Purchaser decision model: High decoupling (delta close to 1) ignores defects
                # If expected utility > 0, complete acquisition
                acquisition_incentive = 1.0 - (purchaser['decoupling'] * (1.0 - broker['disclosure']))
                acquire = 1 if acquisition_incentive > 0.4 else 0
                
                if acquire:
                    total_acquisition += 1
                    # Unrepresented defects degrade the commons
                    period_damage += (1.0 - broker['disclosure'])

                total_disclosure += broker['disclosure']
                
                # Adaptive broker behavior: if low disclosure wins transactions, mimic it
                if acquire and broker['disclosure'] > 0.1:
                    broker['disclosure'] = max(0.0, broker['disclosure'] - 0.02) # race to bottom
            
            # Update the shared informational commons
            depletion_rate = 0.05 * (period_damage / max(1, self.num_purchasers))
            recovery_rate = 0.01 # baseline institutional repair/audit
            self.informational_commons = max(0.0, min(1.0, self.informational_commons - depletion_rate + recovery_rate))
            
            # Record metrics
            self.history['commons'].append(self.informational_commons)
            self.history['avg_disclosure'].append(total_disclosure / self.num_brokers)
            self.history['avg_acquisition'].append(total_acquisition / self.num_purchasers)

# Execute simulation
sim = MarketSimulation(num_brokers=100, num_purchasers=100, periods=150)
sim.run()
