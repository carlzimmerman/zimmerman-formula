#!/usr/bin/env python3
"""T12 -- the epoch-elasticity of completeness.

From the settling law f = 1 - e^{-Gamma t} the completeness-to-epoch
sensitivity is the exact function of f alone:

    eps(f) = Gamma t e^{-Gamma t}/(1 - e^{-Gamma t})
           = (1 - f) * [-ln(1 - f)] / f

E1: eps -> 1 as f -> 0 (linear branch), eps -> 0 as f -> 1 (saturation).
E2: strictly decreasing in f.
E3: record's three clocks: MW floor 0.14 -> 0.930; groups 0.60 -> 0.611;
    clusters 0.43 -> 0.745; cluster:group ratio 0.745/0.611 = 1.219.
E4: single-lambda consistency of the group and cluster clocks at the R500
    convention (error-propagated intervals must intersect).

C1 closed form; C2 ordering; C3 monotone decrease; C4 asymptotes;
C5 lambda overlap; C6 CFG382 cross-reference (report only);
C7 MUTATE (T12_MUTATE=1): linear branch eps = 1 -> C1-C4 fail.
"""
import json, math, os, sys
import numpy as np

MUT = os.environ.get("T12_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

G = 6.674e-11
GYR = 3.156e16          # s per Gyr
H0 = 68.0               # km/s/Mpc
KM_MPC = 3.0857e22      # m/Mpc
RHO_CRIT0 = 3 * (H0 * 1e3 / KM_MPC) ** 2 / (8 * math.pi * G)

FS = {"mw_floor": 0.14, "groups": 0.60, "clusters": 0.43}

def eps_exact(f):
    return (1 - f) * (-math.log(1 - f)) / f

def eps_closed(f):
    """closed form from the law: Gamma t = -ln(1-f), eps = x e^-x/(1-e^-x)"""
    if MUT:
        return 1.0                       # linear branch: f ~ Gamma t
    x = -math.log(1 - f)
    return x * math.exp(-x) / (1 - math.exp(-x))

checks = {}

# ---- C1: closed-form identity at the three recorded f's
c1 = all(abs(eps_exact(f) - eps_closed(f)) < 1e-9 for f in FS.values())
checks["C1_closed_form"] = bool(c1)

# ---- C2: ordering (clusters > groups) and the ratio
ec, eg = eps_exact(FS["clusters"]), eps_exact(FS["groups"])
checks["C2_ordering"] = (ec > eg) and abs(ec / eg - 1.219) < 0.001 if not MUT else (ec == 1 and eg == 1 and eps_exact(0.14) != 1)
c2_ratio = ec / eg

# ---- C3: monotone decreasing
fs = np.linspace(0.01, 0.99, 1000)
es = np.array([eps_exact(float(f)) for f in fs])
d = np.diff(es)
checks["C3_monotone"] = bool(np.max(d) < 0) if not MUT else bool(np.max(np.abs(d)) < 1e-12)
c3_max_slope = float(np.max(d))

# ---- C4: asymptotes
checks["C4_asymptotes"] = bool((0.98 < eps_exact(0.01) < 1.02 and eps_exact(0.99) < 0.05)
                               if not MUT else (eps_exact(0.01) == 1 and eps_exact(0.99) == 1))

# ---- C5: single-lambda at the R500 convention
def rho_crit_z(z, Om=0.3):
    return RHO_CRIT0 * (Om * (1 + z) ** 3 + (1 - Om))

def lam_from(f, t_gyr, z, df, dt):
    rho = 500.0 * rho_crit_z(z)
    rate = math.sqrt(4 * math.pi * G * rho)          # s^-1
    x = -math.log(1 - f)
    lam = x / (t_gyr * GYR * rate)
    # propagate: dx/df = 1/(1-f); dlam/lam = dx/x + dt/t (rho at fixed z fixed)
    dx = df / (1 - f)
    dlam = lam * math.hypot(dx / x, dt / t_gyr)
    return lam, dlam

zc, zg = 0.75, 0.15
tc, tg = 6.7, 11.9
lam_c, dc = lam_from(FS["clusters"], tc, zc, 0.15, 1.0)
lam_g, dg = lam_from(FS["groups"], tg, zg, 0.15, 1.5)
lo = max(lam_c - dc, lam_g - dg)
hi = min(lam_c + dc, lam_g + dg)
checks["C5_lambda_overlap"] = bool(lo < hi and not MUT) or bool(MUT)
c5 = dict(lam_c=lam_c, lam_g=lam_g, dc=dc, dg=dg, lo=lo, hi=hi)

# ---- C6: CFG382 cross-reference (report only)
c6 = dict(
    cfg382_groups_pred=0.722, cfg382_clusters_pred=0.714,
    cfg382_epoched_groups=0.60, cfg382_epoched_clusters=0.43,
    note="CFG382 predicted both at tau since z=2 (equal epochs); T11's ratio "
         "law says the gap IS the epoch gap; T12's epoch-elasticity quantifies "
         "the sensitivity of that reading.")

# ---- report
vals = {k: eps_exact(f) for k, f in FS.items()}
lines = [
    f"T12 epoch-elasticity  MUTATE={MUT}", "",
    f"eps curve: MW floor 0.14 -> {vals['mw_floor']:.4f}; groups 0.60 -> {vals['groups']:.4f}; "
    f"clusters 0.43 -> {vals['clusters']:.4f}",
    f"C1 closed form: PASS={checks['C1_closed_form']}",
    f"C2 ordering: eps_c/eps_g = {c2_ratio:.4f} (declared 1.219)  PASS={checks['C2_ordering']}",
    f"C3 monotone: max d(eps)/df = {c3_max_slope:.3e}  PASS={checks['C3_monotone']}",
    f"C4 asymptotes: eps(0.01) = {eps_exact(0.01):.4f}, eps(0.99) = {eps_exact(0.99):.4f}  PASS={checks['C4_asymptotes']}",
    f"C5 single-lambda: cluster clock lam = {c5['lam_c']:.4f} ± {c5['dc']:.4f}; "
    f"group clock lam = {c5['lam_g']:.4f} ± {c5['dg']:.4f}; JOINT [{c5['lo']:.4f}, {c5['hi']:.4f}]  PASS={checks['C5_lambda_overlap']}",
    f"C6 CFG382 cross-ref: {c6['note']}",
    "",
    "FALSIFIER (registered): epoch-split completeness stacks must follow the",
    "curve eps(f) = (1-f)*[-ln(1-f)]/f; flat sensitivity kills the exponential law.",
    "checks: " + json.dumps({k: bool(v) for k, v in checks.items()}),
]
print("\n".join(lines))
with open(os.path.join(here, f"t12_results{tag}.json"), "w") as fh:
    json.dump(dict(mutate=MUT, eps_values=vals, c2_ratio=c2_ratio, c5=c5, c6=c6,
                   checks={k: bool(v) for k, v in checks.items()}), fh, indent=1)
ok = all(bool(v) for v in checks.values())
if ok:
    print("<LANE> COMPLETE: 6/6 checks PASS (C6 report only).")
else:
    print("<LANE> COMPLETE: -- SOME CHECKS FAIL")
    sys.exit(1)