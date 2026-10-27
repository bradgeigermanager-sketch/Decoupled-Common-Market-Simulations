import random

class Broker:
    def __init__(self, broker_id: int, initial_disclosure: float):
        self.id = broker_id
        self.disclosure = initial_disclosure  # d in [0, 1] (1 = honest, 0 = hidden defects)

    def update_strategy(self, successful_transaction: bool):
        # Adaptive adjustment: if misrepresentation secures transactions, lower disclosure (race to the bottom)
        if successful_transaction and self.disclosure > 0.0:
            self.disclosure = max(0.0, self.disclosure - 0.02)

class Purchaser:
    def __init__(self, purchaser_id: int, decoupling_level: float):
        self.id = purchaser_id
        self.decoupling = decoupling_level  # delta in [0, 1] (1 = fully insulated from failure)
