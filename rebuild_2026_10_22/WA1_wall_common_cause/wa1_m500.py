"""eRASS1 M500 per cluster, from X7's measured per-cluster file, read only. Mass axis of the tilt nuisance only. Returns log10 M500/Msun."""
import os, numpy as np
_d = np.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "X7_cluster_core_significance", "x7_measure_percluster.npz"), allow_pickle=True)
_m = {str(n): float(x) for n, x in zip(_d["name"], _d["M500"])}
def lg(name):
    v = _m[str(name)]; return np.log10(v) + 13.0  # column in 1e13 Msun: median near 2e14, GS4 tercile edges 1.36e14, 2.39e14
