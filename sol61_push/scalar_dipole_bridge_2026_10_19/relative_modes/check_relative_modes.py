#!/usr/bin/env python3
"""Bounded exact invariants and Gaussian form-factor checks; standard library only."""
import json
import math
from fractions import Fraction as Q
from pathlib import Path

OUT = Path("sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/run/results.json")


def derivative(p):
    return {n - 1: n * c for n, c in p.items() if n}


def add(p, q):
    r = dict(p)
    for n, c in q.items():
        r[n] = r.get(n, Q(0)) + c
    return {n: c for n, c in r.items() if c}


def value(p, x):
    return sum(c * x ** n for n, c in p.items())


# U/(G Md Mb/R), x=s/R, for coextensive equal-radius uniform spheres.
energy = {0: -Q(6, 5), 2: Q(1, 2), 3: -Q(3, 16), 5: Q(1, 160)}
force = derivative(energy)
radial_laplacian = add(derivative(force), {n - 1: 2 * c for n, c in force.items()})
assert radial_laplacian == {0: Q(3), 1: -Q(9, 4), 3: Q(3, 16)}
assert value(energy, Q(2)) == -Q(1, 2)
assert value(force, Q(2)) == Q(1, 4)
assert value(derivative(force), Q(0)) == Q(1)

mass_checks = []
for md, mb in [(Q(1), Q(1)), (Q(1, 3), Q(1)), (Q(2), Q(7)), (Q(100), Q(1))]:
    mt = md + mb
    mu = md * mb / mt
    a, b = mb / mt, md / mt
    assert md * a - mb * b == 0
    assert md * a * a + mb * b * b == mu
    # K=G Md Mb/R^3, so omega_rel^2=G Mt/R^3.
    assert md * mb / mu == mt
    mass_checks.append({"Md": str(md), "Mb": str(mb), "mu": str(mu),
                        "inertial_and_source_identities": "passed"})


def delta_f(k, sd, sb):
    if sd == sb:
        return 0.0
    if sb < sd:
        return -delta_f(k, sb, sd)
    return math.exp(-0.5 * (k * sd) ** 2) * (-math.expm1(-0.5 * k * k * (sb * sb - sd * sd)))


infrared = []
for k in [0.1, 0.03, 0.01, 0.003, 0.001]:
    df = delta_f(k, 1.0, 3.0)
    rho_source = k * df  # mu=s_parallel=1
    leading = 4.0 * k ** 3
    infrared.append({"k_sigma_d": k, "DeltaF": df, "density_source": rho_source,
                     "source_over_leading_k_cubed": rho_source / leading,
                     "density_susceptibility_over_leading_k_sixth": (k * df) ** 2 / (16 * k ** 6)})
    assert delta_f(k, 1.0, 1.0) == 0.0
assert abs(infrared[-1]["source_over_leading_k_cubed"] - 1.0) < 3e-6


def bisect(fn, lo, hi):
    flo = fn(lo)
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        fm = fn(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


bands = []
for q in [1.0, 2.0, 3.0, 10.0, 30.0, 100.0]:
    if q == 1:
        bands.append({"sigma_b_over_sigma_d": q, "maximum_DeltaF_squared": 0.0,
                      "band_DeltaF_squared_at_least_0p9": None})
        continue
    kp = math.sqrt(4 * math.log(q) / (q * q - 1))
    peak = delta_f(kp, 1.0, q) ** 2
    # Exact derivative condition for the peak, checked independently.
    assert abs(math.exp(-kp * kp / 2) - q * q * math.exp(-q * q * kp * kp / 2)) < 1e-12
    band = None
    if peak >= 0.9:
        fn = lambda k: delta_f(k, 1.0, q) ** 2 - 0.9
        lower = bisect(fn, 0, kp)
        upper = bisect(fn, kp, 20)
        assert abs(fn(lower)) < 1e-12 and abs(fn(upper)) < 1e-12
        band = {"k_sigma_d_min": lower, "k_sigma_d_max": upper, "wavenumber_ratio": upper / lower}
    bands.append({"sigma_b_over_sigma_d": q, "peak_k_sigma_d": kp,
                  "maximum_DeltaF_squared": peak, "band_DeltaF_squared_at_least_0p9": band})


# An independent central finite difference checks the Gaussian overlap Hessian.
def gaussian_energy(s, S):
    # G Md Mb = 1 in this check.
    return -math.sqrt(2 / math.pi) / S if s == 0 else -math.erf(s / (math.sqrt(2) * S)) / s


gaussian_curvatures = []
for sd, sb in [(1.0, 1.0), (1.0, 3.0), (1.0, 30.0)]:
    S = math.hypot(sd, sb)
    h = S * 1e-3
    fd = (gaussian_energy(h, S) - 2 * gaussian_energy(0, S) + gaussian_energy(-h, S)) / (h * h)
    overlap = (2 * math.pi * S * S) ** (-1.5)
    predicted = 4 * math.pi * overlap / 3
    relerr = abs(fd / predicted - 1)
    assert relerr < 1e-5
    gaussian_curvatures.append({"sigma_d": sd, "sigma_b": sb, "K_over_GMdMb_exact_formula": predicted,
                                "central_difference": fd, "relative_error": relerr})

results = {
    "status": "passed",
    "exact_uniform_sphere_polynomial_laplacian": {str(n): str(c) for n, c in radial_laplacian.items()},
    "exact_uniform_sphere_boundary_energy": str(value(energy, Q(2))),
    "exact_uniform_sphere_boundary_force": str(value(force, Q(2))),
    "mass_inertia_checks": mass_checks,
    "infrared_source_checks": infrared,
    "Gaussian_intermediate_bands": bands,
    "Gaussian_curvature_checks": gaussian_curvatures,
    "scope": "Exact finite rational invariants and floating Gaussian examples only; no GP-Poisson evolution or equilibrium-state construction."
}
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({"status": "passed", "output": str(OUT), "Gaussian_bands": bands}, indent=2))
