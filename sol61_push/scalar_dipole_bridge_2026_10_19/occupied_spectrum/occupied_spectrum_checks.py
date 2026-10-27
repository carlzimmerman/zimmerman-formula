"""Bounded deterministic checks of occupied Friedrichs spectra, not decay counts.

Run only with contract.json through the pinned computation-audit runner.
The smooth-cutoff NR model is a declared mathematical control, not a fitted
cosmological population or a relativistic UV completion.
"""
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import scipy

BASE = Path(__file__).resolve().parent
PAR = json.loads((BASE / "parameters.json").read_text())
CHECKS = []
ROWS = {}


def check(name, condition, observed=None, tolerance=None):
    row = {"name": name, "passed": bool(condition)}
    if observed is not None:
        row["observed"] = observed
    if tolerance is not None:
        row["tolerance"] = tolerance
    CHECKS.append(row)


def slope(f, lo, hi):
    return math.log(f(hi) / f(lo)) / math.log(hi / lo)


def j_rel(E, m, M, g):
    # beta evaluated without subtraction of nearly equal squared energies.
    beta = math.sqrt((E - 2 * m) * (E + 2 * m)) / E
    return g * g * beta / (16 * math.pi**2 * M)


m = PAR["benchmark"]["m_eV"]
u = PAR["benchmark"]["u_star"]
g = m * PAR["benchmark"]["g_over_m"]
M = 2 * m * math.sqrt(1 + u * u)
delta = 2 * m * u * u / (math.sqrt(1 + u * u) + 1)
width = g * g * u / math.sqrt(1 + u * u) / (8 * math.pi * M)
A_benchmark = g * g / (16 * math.pi**2 * M * math.sqrt(m))
check("canonical J matches on-shell width", abs(2 * math.pi * j_rel(M, m, M, g) / width - 1) < 1e-11)
for ratio in [2.0004, 2.01, 3, 10]:
    E = ratio * m
    p = math.sqrt(E * E / 4 - m * m)
    omega = E / 2
    # Radial phase-space Jacobian, including the unordered-pair factor 1/2.
    radial = (g * g / (4 * M)) * (p * p / (2 * math.pi**2 * omega**2)) * (omega / (2 * p))
    check("vertex and phase-space normalization " + str(ratio), abs(radial / j_rel(E, m, M, g) - 1) < 1e-12)
gamma_off = lambda E: g * g * math.sqrt(1 - 4 * m * m / E**2) / (8 * math.pi * E)
for ratio in [2.1, 4, 20]:
    E = ratio * m
    check("offshell normalization factor " + str(ratio), abs((2 * math.pi * j_rel(E, m, M, g)) / gamma_off(E) - E / M) < 1e-12)
ROWS["benchmark"] = {"m_eV": m, "M_eV": M, "delta_eV": delta, "g_eV": g, "width_eV": width, "width_over_delta": width / delta, "NR_threshold_A_sqrt_eV": A_benchmark, "critical_energy_scale_eV": (math.pi * A_benchmark)**2}


def smooth_j(e, A, cutoff):
    return A * math.sqrt(e) / (1 + e / cutoff)**2


def smooth_re_sigma(e, A, cutoff):
    C = math.pi * A * math.sqrt(cutoff) / 2
    s = e / cutoff
    return -C * (1 - s) / (1 + s)**2


def smooth_spectrum(e, A, cutoff, nu):
    J = smooth_j(e, A, cutoff)
    C = math.pi * A * math.sqrt(cutoff) / 2
    D = e - nu - (smooth_re_sigma(e, A, cutoff) + C)
    return J / (D * D + (math.pi * J)**2)


for model in PAR["smooth_models"]:
    A, cutoff, nu = model["A"], model["cutoff"], model["nu"]
    C = math.pi * A * math.sqrt(cutoff) / 2
    bare = nu + C
    bound, Z = 0.0, 0.0
    if nu < 0:
        f = lambda k: -cutoff * k * k - nu - C + C / (1 + k)**2
        k = brentq(f, 1e-15, 10)
        bound = -cutoff * k * k
        Z = 1 / (1 + C / (cutoff * k * (1 + k)**3))
    # e=t^2 resolves the integrable critical threshold without a singular sample.
    moments = []
    errors = []
    for power in [0, 1, 2]:
        fun = lambda t: 2 * t * (t * t)**power * smooth_spectrum(t * t, A, cutoff, nu)
        val, err = quad(fun, 0, np.inf, epsabs=2e-10, epsrel=2e-10, limit=200)
        moments.append(val + Z * bound**power)
        errors.append(err)
    targets = [1, bare, bare * bare + C * cutoff]
    for power in [0, 1, 2]:
        check("smooth spectral moment " + model["name"] + " " + str(power), abs(moments[power] - targets[power]) < 2e-8, moments[power] - targets[power], 2e-8)
    # Independent quadrature of the self-energy below the continuum.
    for z in [-.02, -.3, -2]:
        numerical = quad(lambda t: 2 * t * smooth_j(t * t, A, cutoff) / (z - t * t), 0, np.inf, epsabs=1e-11, limit=200)[0]
        exact = -C / (1 + math.sqrt(-z / cutoff))**2
        check("smooth self-energy " + model["name"] + " " + str(z), abs(numerical - exact) < 1e-10, numerical - exact, 1e-10)
    threshold_slope = slope(lambda e: smooth_spectrum(e, A, cutoff, nu), 1e-10, 1e-8)
    expected = -.5 if nu == 0 else .5
    check("actual occupied threshold exponent " + model["name"], abs(threshold_slope - expected) < 2e-4, threshold_slope, 2e-4)
    ROWS[model["name"]] = {"bare_source_excess": bare, "bound_energy": bound, "bound_residue": Z, "continuum_probability": moments[0] - Z, "moments_with_bound": moments, "moment_targets": targets, "quad_errors": errors, "threshold_slope": threshold_slope}

# Distinguish the physical NR intermediate tail and formal relativistic star tail.
nr_tail = slope(lambda e: smooth_spectrum(e, 1e-6, 1, 1e-7), 1e-4, 1e-3)
rel_tail = slope(lambda E: j_rel(E, 1, 2.1, .01) / (E - 2.1)**2, 1e4, 1e5)
width_tail = slope(lambda E: (2.1 / E) * j_rel(E, 1, 2.1, .01) / (E - 2.1)**2, 1e4, 1e5)
check("NR intermediate occupation tail", abs(nr_tail + 1.5) < .004, nr_tail, .004)
check("formal canonical relativistic star tail", abs(rel_tail + 2) < .001, rel_tail, .001)
check("running-width matched star tail differs", abs(width_tail + 3) < .001, width_tail, .001)
ROWS["tail_slopes"] = {"NR_intermediate": nr_tail, "canonical_formal_relativistic": rel_tail, "running_width_star": width_tail}

# Occupied BE spectra: free particles vs Bogoliubov quasiparticles and atoms.
T, mc2 = 1., 1.
free = lambda e, mu: math.sqrt(e) / math.expm1((e - mu) / T)
for mu, exponent in [(-.5, .5), (0., -.5)]:
    sl = slope(lambda e: free(e, mu), 1e-9, 1e-6)
    check("free Bose occupied threshold mu=" + str(mu), abs(sl - exponent) < 1e-5, sl, 1e-5)


def bog(omega):
    # m=1, c=1; epsilon_k=sqrt(omega^2+mc2^2)-mc2, stabilized at small omega.
    r = math.sqrt(omega * omega + mc2 * mc2)
    eps = omega * omega / (r + mc2)
    k = math.sqrt(2 * eps)
    dos = k * omega / (2 * math.pi**2 * r)
    v2 = mc2 * mc2 / (2 * omega * (eps + mc2 + omega))
    bose = 1 / math.expm1(omega / T)
    return {"qp": dos * bose, "atom_quantum": dos * v2, "atom_thermal": dos * r / omega * bose}


for name, exponent in [("qp", 1), ("atom_quantum", 1), ("atom_thermal", 0)]:
    sl = slope(lambda om: bog(om)[name], 1e-9, 1e-6)
    check("Bogoliubov occupied IR " + name, abs(sl - exponent) < 1e-5, sl, 1e-5)
quantum_tail = slope(lambda om: bog(om)["atom_quantum"], 30, 300)
check("Bogoliubov atom depletion UV power", abs(quantum_tail + 1.5) < .03, quantum_tail, .03)
# The explicit thermal contribution is exponentially suppressed, independent of DOS.
check("thermal occupation UV suppression", bog(100)["qp"] / bog(30)["qp"] < 1e-28)

# Exact target moment divergence, shown at finite cutoffs using its antiderivative.
target_first = lambda L: math.asinh(L) - L / math.sqrt(1 + L * L)
target_rows = [{"L_over_a": L, "first_moment_over_psat_a": target_first(L)} for L in [10, 100, 1000, 10000]]
for r1, r2 in zip(target_rows[:-1], target_rows[1:]):
    check("target logarithmic energy-moment increment " + str(r2["L_over_a"]), abs((r2["first_moment_over_psat_a"] - r1["first_moment_over_psat_a"]) - math.log(10)) < .015)
ROWS["target_moment_cutoffs"] = target_rows

out = {"parameters": PAR, "rows": ROWS, "checks": CHECKS, "all_pass": all(c["passed"] for c in CHECKS), "software": {"Python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__}, "scope": "Occupied source spectral measures and explicit Bose populations; no repeated survival-probability production experiment", "non_claims": ["No physical dipole or mapping Omega/(2d) is supplied", "The smooth NR cutoff is an explicit control model", "No cosmological source state, abundance, thermal history or UV completion is inferred"]}
result = BASE / sys.argv[1] / "results.json"
result.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"checks": len(CHECKS), "all_pass": out["all_pass"], "benchmark": ROWS["benchmark"], "tail_slopes": ROWS["tail_slopes"]}, indent=2))
assert out["all_pass"]
