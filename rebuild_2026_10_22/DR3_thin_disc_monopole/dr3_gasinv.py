import warnings; warnings.filterwarnings("ignore", message=".*matmul.*")
"""DR3 stress, AFTER the primary result: gas monopole from SPARC's measured V_gas by a nonnegative ring inversion, no assumed shape. Soft thin-ring kernel; total pinned to 1.33 M_HI. kpc, Msun, km/s."""
import math
import numpy as np
from scipy.optimize import nnls
from scipy.special import ellipk, ellipe
G = 4.30091e-6
def _gr(R, a, z):
    """v^2/dm at R from a ring a, height z (km/s)^2 per Msun."""
    D2 = (R + a) ** 2 + z * z; m = 4 * a * R / D2
    return G / (math.pi * np.sqrt(D2)) * (ellipk(m) + ellipe(m) * (R * R - a * a - z * z) / ((R - a) ** 2 + z * z))
def invert(R, Vg2, Mtot, nsub=3000, nout=5):
    """R ascending, Vg2 signed. Returns gas mass inside each R, fit rms of V^2 over its max."""
    nodes = np.r_[0.0, R, R[-1] * np.geomspace(1.25, 3.0, nout)]; dr = max(float(np.median(np.diff(R))) if len(R) > 1 else R[0], 1e-3); z = 0.1 * dr
    a = np.linspace(nodes[0], nodes[-1], nsub + 1); a = 0.5 * (a[1:] + a[:-1]); da = a[1] - a[0]; nn = len(nodes); H = np.empty((len(a), nn))
    for j in range(nn):
        e = np.zeros(nn); e[j] = 1.0; H[:, j] = np.interp(a, nodes, e)
    dm = 2 * math.pi * a[:, None] * da * H * 1e6                                # Msun per unit Sigma (Msun/pc^2) at each node
    A = np.array([(_gr(Ri, a, z)[:, None] * dm).sum(0) for Ri in R]); s = max(float(np.max(np.abs(Vg2))), 1e-6); tot = dm.sum(0)
    if Mtot > 0: Mx = np.vstack([A / s, tot / Mtot]); y = np.r_[Vg2 / s, 1.0]
    else: Mx, y = A / s, Vg2 / s
    S, _ = nnls(Mx, y); Sa = H @ S; cum = np.cumsum(2 * math.pi * a * da * Sa * 1e6); return np.interp(R, a + 0.5 * da, cum), float(np.sqrt(np.mean(((A @ S - Vg2) / s) ** 2)))
if __name__ == "__main__":
    from scipy.special import i0, i1, k0, k1
    # K6: recover an exponential's monopole at SPARC-like sampling. Truth from Freeman's formula, h = 2 kpc, M 1e9.
    for Rmax, n in ((10.0, 12), (16.0, 25), (6.0, 8)):
        R = np.linspace(Rmax / n, Rmax, n); y = R / 4; V2 = 4 * math.pi * G * (1e9 / (2 * math.pi * 4)) * 2 * y * y * (i0(y) * k0(y) - i1(y) * k1(y)); M, e = invert(R, V2, 1e9); T = 1e9 * (1 - (1 + R / 2) * np.exp(-R / 2)); print(f"Rmax {Rmax}, n {n}: max |M/T - 1| beyond the first point {np.max(np.abs(M[1:] / T[1:] - 1)):.3f}; fit rms {e:.3f}")
