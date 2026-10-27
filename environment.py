class InformationalCommons:
    def __init__(self, initial_state: float = 1.0, recovery_rate: float = 0.01):
        self.state = initial_state  # I_t in [0.0, 1.0]
        self.recovery_rate = recovery_rate

    def update(self, period_damage: float, num_purchasers: int):
        depletion_rate = 0.05 * (period_damage / max(1, num_purchasers))
        self.state = max(0.0, min(1.0, self.state - depletion_rate + self.recovery_rate))

    def get_state(self) -> float:
        return self.state
