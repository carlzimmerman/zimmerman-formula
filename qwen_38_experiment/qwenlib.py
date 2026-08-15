#!/usr/bin/env python3
"""qwenlib -- the single source of framework constants, the kernel, and check().

Every runs/tNNN_*.py imports from here.  Do NOT re-hardcode constants in task scripts;
if a constant is missing, add it HERE with a provenance comment and note it in the ledger.
"""
import sys

import numpy as np

# ---- constants, with provenance -----------------------------------------------------
G = 6.67430e-11                 # CODATA
C = 2.99792458e8                # exact
KPC = 3.0856775814913673e19     # m
MPC = 1e3 * KPC
MSUN = 1.989e30
AU = 1.495978707e11
H0 = 67.4e3 / MPC               # 1/s (Planck-18 base)
T_H = 4.35e17                   # s, committed Hubble time (stage17)
RHO_CRIT = 3 * H0**2 / (8 * np.pi * G)
OM_DM, OM_B, OM_M, OM_L = 0.265, 0.0493, 0.315, 0.685
A0_CAN = 9.3619e-11             # canonical footing: kappa c sqrt(G rho_Lambda)
A0_ALT = 1.1279e-10             # alt footing: rho_total / cH0
KAPPA_MEAS, KAPPA_ERR = 0.551, 0.043   # distance-free measurement; 1/2 is ADOPTED
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4      # the committed nu0 window (stage17)
Q0_LO, Q0_HI = 0.0024, 0.0146          # Mpc^-1, operative pinned band (stage58+61)
X_CORE = (106.0, 453.0)                # pinned X, core (stage56/58)
GAMMA_BAND_CAN = (1.1614, 1.1814)      # frozen Amendment-10 DR4 band, canonical
GAMMA_BAND_ALT = (1.1917, 1.2267)      # frozen Amendment-10 DR4 band, alt
NOVERDICT_EDGE = 1.23
Z_BIND = 10.83                         # binding-epoch wall (stage52/53)
KB_MAX = 0.25                          # corpus BBN cap on K_B (stage50)

FOOTINGS = {"can": A0_CAN, "alt": A0_ALT}

# ---- the framework's own kernel (Milgrom & Sanders 2008 Eq 13, alpha=1/2) -----------
def nu(y):
    """nu(y) = 1/(1 - exp(-sqrt(y))): g_obs = nu(g_N/a0) * g_N."""
    y = np.asarray(y, dtype=float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def y_of_x(x, iters=200):
    """invert x = y nu(y): observed x = g_obs/a0 -> Newtonian y = g_N/a0."""
    x = np.asarray(x, dtype=float)
    y = x.copy()
    for _ in range(iters):
        y = x / nu(y)
    return y

def mu_of_x(x):
    """AQUAL-side mu(x) = y(x)/x = 1/nu."""
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    m = x > 1e-12
    out[m] = y_of_x(x[m]) / x[m]
    return out

def gobs_line(gn, a0):
    """the a0-line exact law g_obs^2 - g_N^2 = a0 g_N."""
    gn = np.asarray(gn, dtype=float)
    return 0.5 * (gn + np.sqrt(gn**2 + 4 * gn * a0))

def a0_local_ratio(overdensity, nu0):
    """S = a0_local/a0(0) at charge overdensity r (stage59's committed formula)."""
    return ((1.0 + nu0**2) / (1.0 + nu0**2 * np.asarray(overdensity, float) ** 2)) ** 0.25

def response_tensor(x_ext):
    """linearized AQUAL EFE response about external x: (nu0, L0, B_par, B_perp)."""
    ye = float(y_of_x(x_ext))
    n0 = float(nu(ye))
    h = 1e-6
    dxdy = ((ye + h) * float(nu(ye + h)) - (ye - h) * float(nu(ye - h))) / (2 * h)
    L0 = n0 / dxdy - 1.0
    return n0, L0, n0, n0 / np.sqrt(1.0 + L0)

def a0z_ratio_sq(z, nu0):
    """derived law: a0^2(z)/a0^2(0) = sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6)."""
    return np.sqrt(1 + nu0**2) / np.sqrt(1 + nu0**2 * (1.0 + np.asarray(z, float)) ** 6)

# ---- the check harness ---------------------------------------------------------------
FAIL, NCHK = [], [0]

def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok

def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))

def finish(stage_name):
    """print the tally and exit non-zero on any failure.  Call as the LAST line."""
    n_fail = len(FAIL)
    print("=" * 90)
    print(f"{stage_name}: {NCHK[0] - n_fail}/{NCHK[0]} checks passed"
          + ("" if not n_fail else f"; FAILED: {FAIL}"))
    sys.exit(1 if n_fail else 0)

# ---- dimensional-analysis helpers (T084) -------------------------------------------
# A dimensional quantity is (value, dims) with dims the [m, kg, s] exponent 3-vector.
# Arithmetic propagates exponents: * adds, / subtracts, **n multiplies, a bare scalar
# leaves dims unchanged.  T084 uses these to unit-test that the committed formulas are
# dimensionally consistent.  Purely ADDITIVE: no pinned number in the section above is
# touched, so the T085 canary is unaffected.
DIM_LABELS = ("m", "kg", "s")

class Qty:
    """(value, [m, kg, s] exponents); operators carry the dimensions through."""
    __slots__ = ("value", "dims")
    def __init__(self, value, dims=(0, 0, 0)):
        self.value = float(value)
        self.dims = tuple(dims)
    def __repr__(self):
        return f"Qty({self.value:.4g}, {self.dims})"
    def __mul__(self, o):
        if isinstance(o, Qty):
            return Qty(self.value * o.value,
                       tuple(a + b for a, b in zip(self.dims, o.dims)))
        return Qty(self.value * o, self.dims)
    __rmul__ = __mul__
    def __truediv__(self, o):
        if isinstance(o, Qty):
            return Qty(self.value / o.value,
                       tuple(a - b for a, b in zip(self.dims, o.dims)))
        return Qty(self.value / o, self.dims)
    def __rtruediv__(self, o):
        return Qty(o / self.value, tuple(-a for a in self.dims))
    def __pow__(self, n):
        return Qty(self.value ** n, tuple(d * n for d in self.dims))

# committed dimensional exponents [m, kg, s] for the corpus constants (qwenlib provenance)
DIM = {
    "G":        (3, -1, -2),
    "C":        (1, 0, -1),
    "KPC":      (1, 0, 0),
    "MPC":      (1, 0, 0),
    "MSUN":     (0, 1, 0),
    "AU":       (1, 0, 0),
    "H0":       (0, 0, -1),
    "T_H":      (0, 0, 1),
    "RHO_CRIT": (-3, 1, 0),
    "A0_CAN":   (1, 0, -2),
    "A0_ALT":   (1, 0, -2),
    "Q0":       (-1, 0, 0),
    "DIMLESS":  (0, 0, 0),
}

# named target dimensions, [m, kg, s]
DIMS = {
    "accel":       (1, 0, -2),
    "density":     (-3, 1, 0),
    "length":      (1, 0, 0),
    "time":        (0, 0, 1),
    "speed":       (1, 0, -1),
    "velocity_sq": (2, 0, -4),
    "dimless":     (0, 0, 0),
}

def D(name):
    """a unit-magnitude quantity carrying the named dimension (for building RHSes)."""
    return Qty(1.0, DIM[name])

def check_dims(expr, target, label):
    """check() wrapper: a built quantity's propagated dims must equal a named target."""
    return check(tuple(expr.dims) == DIMS[target],
                 f"{label}: dims {expr.dims} == {DIMS[target]} ({target})")
