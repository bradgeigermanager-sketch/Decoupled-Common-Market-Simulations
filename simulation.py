import random
from decoupled_commons.agents import Broker, Purchaser
from decoupled_commons.environment import InformationalCommons

class MarketSimulationEngine:
    def __init__(self, num_brokers: int = 100, num_purchasers: int = 100, periods: int = 150):
        self.periods = periods
        self.commons = InformationalCommons()
        self.brokers = [Broker(i, random.uniform(0.3, 0.8)) for i in range(num_brokers)]
        self.purchasers = [Purchaser(i, random.uniform(0.5, 1.0)) for i in range(num_purchasers)]
        
        self.history = {'commons': [], 'avg_disclosure': [], 'avg_acquisition': []}

    def run(self):
        for _ in range(self.periods):
            total_disclosure = 0
            total_acquisition = 0
            period_damage = 0

            for purchaser in self.purchasers:
                broker = random.choice(self.brokers)
                
                # Purchaser acquisition decision logic based on decoupling and perceived quality
                acquisition_incentive = 1.0 - (purchaser.decoupling * (1.0 - broker.disclosure))
                acquire = 1 if acquisition_incentive > 0.4 else 0

                if acquire:
                    total_acquisition += 1
                    period_damage += (1.0 - broker.disclosure)

                total_disclosure += broker.disclosure
                broker.update_strategy(successful_transaction=bool(acquire))

            # Update environment state
            self.commons.update(period_damage, len(self.purchasers))

            # Log metrics
            num_b = len(self.brokers)
            num_p = len(self.purchasers)
            self.history['commons'].append(self.commons.get_state())
            self.history['avg_disclosure'].append(total_disclosure / num_b)
            self.history['avg_acquisition'].append(total_acquisition / num_p)

        return self.history
