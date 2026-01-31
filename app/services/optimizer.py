class AIResourceOptimizer:
    def __init__(self):
        self.kwh_per_1k_tokens = 0.0008
        self.liters_per_1k_tokens = 0.42

    def calculate_metrics(self, token_usage):
        energy = (token_usage / 1000) * self.kwh_per_1k_tokens
        water = (token_usage / 1000) * self.liters_per_1k_tokens
        return round(energy, 6), round(water, 4)

    def self_optimize_check(self, prompt):
        if len(prompt) > 750:
            return True, "⚠️ High input volume was detected. A summary was made to improve energy efficiency."
        return False, "✅ The input is optimized."