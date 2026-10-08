#!/usr/bin/env python3
"""CFG429 (door 4 of the 10-07 list): a settling rate keyed to the local dynamical time with ZERO constants.
The record's settling law (CFG382, used by T15/T16) is already f = 1 - exp(-lambda sqrt(4 pi G rho) tau), i.e. Gamma = lambda / t_dyn;
"zero constants" means lambda = 1.  Score it on T15's own ledger rows (numbers copied from t15_cold_budget.py's docstring, not refitted):
M_cold/M_b = x - f S(<R)/M_b; feasible iff >= 0.  MUTATE (CFG429_MUTATE=1): lambda = 0.0073 (T15's cluster ceiling) -> clusters_b0 must be ~0."""
import math, os, json
MUT = os.environ.get("CFG429_MUTATE", "0") == "1"; LAM = 0.0073 if MUT else 1.0
G, A0, GYR = 6.674e-11, 1.2e-10, 3.156e16; TAU = 10.3 * GYR
def S(Mb, Rk): return 1 / (math.exp(math.sqrt(G * Mb * 1.989e30 / A0) / 3.086e19 / Rk) - 1)
def f(rho): return 1 - math.exp(-LAM * math.sqrt(4 * math.pi * G * rho) * TAU)
rho500 = 1.55e-24; rho30 = 200e3 ** 2 / (4 * math.pi * G * (30 * 3.086e19) ** 2)
rows = {"MW30_V200": (1.8, f(rho30), S(7e10, 30)), "groups_b0": (0.79, f(rho500), S(6e12, 554)), "groups_b03": (1.76, f(rho500), S(6e12, 554)),
        "clusters_b0": (0.41, f(rho500), S(2.8e13, 985)), "clusters_b03": (0.91, f(rho500), S(2.8e13, 985))}
L = [f"lambda = {LAM}  (Gamma = lambda/t_dyn; 1 = zero constants)"]
out = {}
for k, (x, ff, s) in rows.items():
    mc = x - ff * s; out[k] = dict(x=x, f=ff, S=s, Mcold=mc); L.append(f"  {k:13s}: f {ff:.3f}  S/M_b {s:.2f}  deficit {x:.2f}  M_cold/M_b {mc:+.2f}  {'FEASIBLE' if mc >= 0 else 'NEGATIVE'}")
v = "ZERO-CONSTANT t_dyn RATE EXCLUDED" if all(r["Mcold"] < 0 for r in out.values()) else "NOT EXCLUDED"
L.append(f"VERDICT: {v}  (at lambda = 1 settling completes everywhere, f -> 1, so the full kernel supply S exceeds every measured deficit)")
print("\n".join(L)); suf = "_MUTATE" if MUT else ""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"cfg429_tdyn{suf}.out"), "w").write("\n".join(L) + "\n")
