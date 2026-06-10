import re

file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''    def monte_carlo_resonance(self, num_trials=100000):
        """Extended Monte Carlo Simulation for P-value refinement"""
        hits = 0
        for _ in range(num_trials):
            random_sample = np.random.uniform(0.5, 2.0, len(self.data_pool))
            current_harmony = np.mean([1 - abs(1 - x) for x in random_sample])
            real_harmony = np.mean(
                [
                    1
                    - (
                        abs(item["real"] - item["sim"])
                        / (item["sim"] if item["sim"] != 0 else 1)
                    )
                    for item in self.data_pool
                ]
            )
            if current_harmony >= real_harmony:
                hits += 1
        return hits / num_trials'''

new_func = '''    def monte_carlo_resonance(self, num_trials=10000):
        """Extended Monte Carlo Simulation for P-value refinement"""
        hits = 0
        # OUTSIDE LOOP AND VECTORIZED!
        real_harmony = np.mean(
            [
                1
                - (
                    abs(item["real"] - item["sim"])
                    / (item["sim"] if item["sim"] != 0 else 1)
                )
                for item in self.data_pool
            ]
        )
        for _ in range(num_trials):
            random_sample = np.random.uniform(0.5, 2.0, len(self.data_pool))
            current_harmony = np.mean(1 - np.abs(1 - random_sample))
            if current_harmony >= real_harmony:
                hits += 1
        return hits / num_trials'''

content = content.replace(old_func, new_func)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
