import numpy as np

class ChaosEngine:

    def __init__(self, seed):
        self.seed = seed

    def _get_rng(self):
        return np.random.default_rng(self.seed)

    # 🔀 Permutation
    def permute(self, data):
        flat = data.flatten()
        rng = self._get_rng()
        indices = rng.permutation(len(flat))
        return flat[indices].reshape(data.shape)

    # 🔁 Reverse permutation
    def inverse_permute(self, data):
        flat = data.flatten()
        rng = self._get_rng()
        indices = rng.permutation(len(flat))

        original = np.empty_like(flat)
        original[indices] = flat

        return original.reshape(data.shape)

    # 🧬 Diffusion (XOR)
    def diffuse(self, data):
        flat = data.flatten()
        rng = self._get_rng()
        chaos = rng.integers(0, 256, size=len(flat), dtype=np.uint8)

        flat = flat ^ chaos
        return flat.reshape(data.shape)

    # 🔁 Reverse diffusion (same operation)
    def inverse_diffuse(self, data):
        return self.diffuse(data)