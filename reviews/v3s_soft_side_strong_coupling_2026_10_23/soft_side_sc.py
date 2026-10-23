#!/usr/bin/env python3
"""v3s soft side (D.P < 0): non-relativistic strong-coupling analysis (FROZEN_CRITERIA.md, a7649df81b).

N1 structure identities (sympy); N2 z = 0 power counting vs P3's formula with c_pi(k) = omega/k; N3 H4's regions, both
footings; N4 approach to the null / interface; N5 other soft-side vertices.  --mutate: X3's reading, c_pi = 0 inserted
into P3's relativistic formula.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
checks, out = [], {"mutate": MUTATE}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


# ---------------------------------------------------------------- P3's scales(), verbatim (hash-checked)
P3DIR = REPO / "rebuild_2026_10_22" / "P3_v3_strong_field"
src = (P3DIR / "p3_v3_strong_field.py").read_text()
assert hashlib.sha256((P3DIR / "p3_v3_strong_field.py").read_bytes()).hexdigest().startswith("1aaf59addcc38ae6")
p3res = json.loads((P3DIR / "p3_v3_strong_field_results.json").read_text())
c_SI, G_SI, LPLANCK = 2.99792458e8, 6.67430e-11, 1.616255e-35
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MU_K = 1.0 / (100 * KPC)
c_tt, c_zz, c_tilt = p3res["E3"]["c_tt"], p3res["E3"]["c_zz"], p3res["E3"]["c_tilt"]
SQK = math.sqrt(4 * math.pi) * LPLANCK
i0 = src.index("def scales(zh, zPh, gh")
exec(src[i0:src.index("sysres = {}", i0)])
K_NAT = 4 * math.pi * LPLANCK ** 2            # K = 4 pi G in hbar = c = 1, in m^2
H0 = 67.5e3 / (1e3 * KPC)                      # s^-1

# ================================================================ N1 structure
t, x, y, z = sp.symbols("t x y z", real=True)
sig = sp.Function("sigma")(t, x, y, z)
X3 = (x, y, z)
v = [-sp.diff(sig, c) for c in X3]
Xi = -sp.diff(sig, t) + sp.Rational(1, 2) * sum(sp.diff(sig, c) ** 2 for c in X3)
res1 = [sp.simplify(sp.diff(Xi, X3[i]) - (sp.diff(v[i], t) + sum(v[j] * sp.diff(v[i], X3[j]) for j in range(3))))
        for i in range(3)]
a, a0, Kk, Lam, p = sp.symbols("a a0 K Lambda p", positive=True)
W = (a0 ** 2 / Kk) * (-(Kk * p) / a0 - sp.log(1 - Kk * p / a0))
pstar = sp.solve(sp.Eq(sp.diff(p * a - W, p), 0), p)
pstar = [s_ for s_ in pstar if sp.simplify(s_ - a0 * a / (Kk * (a0 + a))) == 0][0]
leg = sp.simplify((p * a - W).subs(p, pstar))
yv = a / a0
Jx = Lam - 2 * a0 ** 2 * (yv - sp.log(1 + yv))
res2 = sp.simplify(leg + (Jx - Lam) / (2 * Kk))
vd = sp.Matrix(sp.symbols("vd1:4"))
cv = sp.Matrix(sp.symbols("cv1:4"))
Mi = sp.symbols("M", positive=True)
quad_cub = sp.expand(((vd + cv).T * (vd + cv))[0] / (2 * Kk * Mi))
res3 = sp.simplify(quad_cub - ((vd.T * vd)[0] / (2 * Kk * Mi) + (vd.T * cv)[0] / (Kk * Mi) + (cv.T * cv)[0] / (2 * Kk * Mi)))
record("N1", all(r_ == 0 for r_ in res1) and res2 == 0 and res3 == 0,
       f"grad Xi = Dv/Dt (v = -grad sigma): {res1}; Legendre of P.a - W = -(J_x - Lambda)/(2K): {res2}; "
       f"(1/2KM)|vdot + (v.grad)v|^2 = quadratic + cubic (1/KM) vdot.(v.grad)v + quartic: {res3}")

# ================================================================ N2 power counting
kk, om, Mm, ell = sp.symbols("k omega M ell", positive=True)
eps_NR = Kk * Mm * kk ** 5 / om ** 3
dimless = sp.simplify(eps_NR.subs({Kk: Kk * ell ** 2, kk: kk / ell, om: om / ell}) - eps_NR) == 0
Z = kk ** 2 / (Kk * Mm)
cpi = om / kk
lam1 = Z * sp.Rational(c_zz) / 2
Lam2 = Z ** sp.Rational(3, 2) * cpi ** sp.Rational(7, 2) / lam1          # P3: Lambda^2 = Z^(3/2) c^(3/2 + 2)/lam
eps_P3 = sp.simplify((cpi * kk) ** 4 / Lam2 ** 2)
ratio = sp.simplify(eps_P3 / eps_NR)
# numeric route: P3's own scales() at a dispersionless point with G > 0 (gamma_L off: zP = k^2/M, L* -> 0 in V6 only)
kt, Mt, rho_t = 0.05, 1.04, 1e-25                       # m^-1, -, kg/m^3 (test point)
gh = 4 * math.pi * G_SI * rho_t / c_SI ** 2            # K rho in m^-2 (SI hatted, as P3)
zPh = kt ** 2 / Mt
s_ = scales(zPh, zPh, gh, kt, 0.0, 1e-27, 1e-27, Mt, 0.0, 1.0)
om0 = math.sqrt(gh * Mt)                                # decoupled omega/c, m^-1
eps_num = s_["vertices"]["V1 pidot (grad pi)^2 [clock]"]["eps"]
eps_formula = K_NAT * Mt * kt ** 5 / (4 * om0 ** 3)
record("N2", dimless and ratio == sp.Rational(1, 4) and abs(eps_num / eps_formula - 1) < 1e-9,
       f"eps_NR = K M k^5/omega^3 dimensionless: {dimless}; eps_P3(c_pi = omega/k)/eps_NR = {ratio}; P3's scales() at a "
       f"dispersionless test point: V1 eps {eps_num:.6e} vs K M k^5/(4 omega^3) {eps_formula:.6e}")
out["N2"] = {"eps_P3": str(eps_P3), "ratio": str(ratio), "numeric": [eps_num, eps_formula]}

# ================================================================ N3 H4's regions
h4 = json.loads((REPO / "rebuild_2026_10_22" / "H4_v3_saddle_stability" / "h4_v3_saddle_stability_results.json").read_text())


def lsc(rho, xx, mode="full", wfloor=False):
    """strong-coupling length (m) for |rho_tau| (kg/m^3) at x, P3 convention eps = K M k^5/(4 omega^3) = 1."""
    M = 1 + xx
    G2 = 4 * math.pi * G_SI * abs(rho) * (xx if mode == "full" else M)      # M - 1 = x exactly (run 1: (1+x)-1 underflowed)
    w = math.sqrt(G2) / c_SI                                 # m^-1
    if wfloor:
        w = max(w, H0 / c_SI)
    if MUTATE:
        return math.inf                                       # X3: c_pi = 0 -> Lambda = 0 at every k
    ksc = (4 * w ** 3 / (K_NAT * M)) ** 0.2
    return 2 * math.pi / ksc


rows = []
for key, rec in h4["regions"].items():
    foot = key.split("|")[1]
    for fkey, fv in rec.items():
        for res_, rv in fv.items():
            for part, d in rv.items():
                if d.get("empty"):
                    continue
                for stat, xk in (("median_abs_rho", "x_median"), ("max_abs_rho_excl_null", "x_at_max")):
                    rho, xx = d[stat], d[xk]
                    rows.append({"region": key, "footing": foot, "dust": fkey, "res": res_, "part": part, "stat": stat,
                                 "rho": rho, "x": xx, "l_full_m": lsc(rho, xx), "l_dec_m": lsc(rho, xx, "dec"),
                                 "l_full_H0_m": lsc(rho, xx, wfloor=True), "ell_region_m": d["ell_m"]})
lmax = max(r_["l_full_m"] for r_ in rows)
lmin = min(r_["l_full_m"] for r_ in rows)
worst = max(rows, key=lambda r_: r_["l_full_m"])
n3_ok = lmax <= PC
per_foot = {f: (min(r_["l_full_m"] for r_ in rows if r_["footing"] == f), max(r_["l_full_m"] for r_ in rows if r_["footing"] == f))
            for f in ("canonical", "alt")}
record("N3", n3_ok, f"{len(rows)} region values: l_sc (self-gravity Gamma, M = 1 + x) from {lmin:.3g} m to {lmax:.3g} m "
                    f"(canonical {per_foot['canonical'][0]:.3g}-{per_foot['canonical'][1]:.3g} m, alt "
                    f"{per_foot['alt'][0]:.3g}-{per_foot['alt'][1]:.3g} m); worst {worst['region']} {worst['stat']} "
                    f"|rho| {worst['rho']:.2e} kg/m^3, x {worst['x']:.4f}; decoupled bracket max "
                    f"{max(r_['l_dec_m'] for r_ in rows):.3g} m; with omega >= H0 max {max(r_['l_full_H0_m'] for r_ in rows):.3g} m; "
                    f"benign line 1 pc = {PC:.3g} m")
out["N3"] = {"rows": rows, "l_min_m": lmin, "l_max_m": lmax, "per_footing": per_foot}

# ================================================================ N4 approach to the null / interface
rho_ref = float(np.median([r_["rho"] for r_ in rows if r_["stat"] == "median_abs_rho"]))
x_ref = float(np.median([r_["x"] for r_ in rows if r_["stat"] == "median_abs_rho"]))
if not MUTATE:
    # l ~ (rho (M-1))^(-3/10) M^(1/5) -> solve l = target in x at rho_ref, and in rho at x_ref
    def solve_x(target):
        lo, hi = 1e-40, 10.0
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            (lo, hi) = (mid, hi) if lsc(rho_ref, mid) > target else (lo, mid)
        return hi

    def solve_rho(target):
        lo, hi = 1e-80, 1e-20
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            (lo, hi) = (mid, hi) if lsc(mid, x_ref) > target else (lo, mid)
        return hi

    n4 = {"rho_ref": rho_ref, "x_ref": x_ref, "l_at_ref_m": lsc(rho_ref, x_ref),
          "x_for_1pc": solve_x(PC), "x_for_1kpc": solve_x(KPC),
          "rho_for_1pc": solve_rho(PC), "rho_for_1kpc": solve_rho(KPC),
          "l_at_rho_1e-9_depth_m": lsc(1e-9 * rho_ref, x_ref)}
    record("N4", True, f"at the median region (|rho| {rho_ref:.2e} kg/m^3, x {x_ref:.4f}) l_sc = {n4['l_at_ref_m']:.3g} m; "
                       f"l_sc reaches 1 pc only for x < {n4['x_for_1pc']:.2e} (1 kpc: x < {n4['x_for_1kpc']:.2e}) or "
                       f"|rho| < {n4['rho_for_1pc']:.2e} ({n4['rho_for_1kpc']:.2e}) kg/m^3; at 1e-9 x depth "
                       f"{n4['l_at_rho_1e-9_depth_m']:.3g} m (X3 stiff-side interface layer: 7 m - 1.1 km)")
    out["N4"] = n4

# ================================================================ N5 other soft-side vertices
if not MUTATE:
    worst_J, worst_V5 = 0.0, 0.0
    for r_ in rows:
        M = 1 + r_["x"]
        w = math.sqrt(4 * math.pi * G_SI * abs(r_["rho"]) * r_["x"]) / c_SI
        ksc = 2 * math.pi / r_["l_full_m"]
        a0m = (9.36e-11 if r_["footing"] == "canonical" else 1.13e-10) / c_SI ** 2
        eps_conv = K_NAT * M * ksc ** 5 / (4 * w ** 3)
        eps_J = (4 / 9) * K_NAT * M * ksc ** 3 * w / (a0m ** 2 * M ** 2)       # J''' cubic: (2/3) w v/(a0 (1+x)), squared
        eps_V5 = eps_conv * (MU_K ** 2 * M / ksc ** 2) ** 2                     # coupling ratio mu^2 M/k^2, squared
        worst_J = max(worst_J, eps_J / eps_conv)
        worst_V5 = max(worst_V5, eps_V5 / eps_conv)
    record("N5", worst_J <= 1 and worst_V5 <= 1, f"at k_sc in every region: J''' cubic / convective <= {worst_J:.1e}; "
                                                 f"K(Q) dust cubic (V5) / convective <= {worst_V5:.1e}")
    out["N5"] = {"J3_over_conv": worst_J, "V5_over_conv": worst_V5}

npass = sum(c["pass"] for c in checks)
out["checks"] = checks
out["summary"] = f"{npass}/{len(checks)} PASS"
print(out["summary"])
(HERE / ("soft_side_sc_results_MUTATE.json" if MUTATE else "soft_side_sc_results.json")).write_text(json.dumps(out, indent=1, default=str))
sys.exit(0 if npass == len(checks) else 1)
