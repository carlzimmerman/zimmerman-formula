"""CFG559 helper: the kinetic redistribution Delta m(x), x = r / r_e, from cfg559_toy_results[_MUTATE].json (FROZEN_CRITERIA.md section 1).
Delta m at an object's census log M_ta: linear in log M_ta between the toy nodes (clamped at the end nodes), footing- and variant-matched.
Beyond each cell's x_ta, Delta m = its value at x_ta (= 0: all mass counted inside r_ta, R3); below x = 1e-3, Delta m = 0."""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = {}
FMAP = {"can": "canonical", "canonical": "canonical", "alt": "alt"}


def table(sigma2x=False):
    k = "MUT" if sigma2x else "MAIN"
    if k not in _CACHE:
        _CACHE[k] = json.load(open(os.path.join(HERE, "cfg559_toy_results_MUTATE.json" if sigma2x else "cfg559_toy_results.json")))
    return _CACHE[k]


class DM:
    """callable Delta m(x) for one object; kind: 'sharp' (Delta m = 0, kinetic support off), 'kin' (sigma x 1), 'kin2' (sigma x 2)."""

    def __init__(self, log10_Mta_h, foot, variant="primary", kind="kin"):
        self.kind = kind
        if kind == "sharp":
            return
        T = table(kind == "kin2")
        ft = FMAP[foot]
        nodes = T["settings"]["nodes"]
        lt = min(max(log10_Mta_h, nodes[0]), nodes[-1])
        j = int(np.clip(np.searchsorted(nodes, lt) - 1, 0, len(nodes) - 2))
        w = (lt - nodes[j]) / (nodes[j + 1] - nodes[j])
        self.parts = []
        for jj, ww in ((j, 1 - w), (j + 1, w)):
            c = T["cells"][f"{variant}|{ft}|{nodes[jj]:.1f}"]
            self.parts.append((ww, np.array(c["x"]), np.array(c["dm"]), np.array(c["m_kin"]), c["q_kin"]["r99"], c["q_sharp"]["r99"]))
        self.w = w; self.j = j

    def __call__(self, x):
        x = np.asarray(x, float)
        if self.kind == "sharp":
            return np.zeros_like(x)
        out = np.zeros_like(x)
        for ww, xg, dm, _, _, _ in self.parts:
            out = out + ww * np.interp(x, xg, dm, left=0.0, right=dm[-1])
        return out

    def m_kin(self, x):
        x = np.asarray(x, float); out = np.zeros_like(x)
        for ww, xg, _, mk, _, _ in self.parts:
            out = out + ww * np.interp(x, xg, mk, left=0.0, right=1.0)
        return out

    def r99(self):
        """r_99 of the kinetic settled mass in units of r_e (sharp: the sharp r_99)."""
        if self.kind == "sharp":
            return None
        return float(sum(ww * q for ww, _, _, _, q, _ in self.parts))
