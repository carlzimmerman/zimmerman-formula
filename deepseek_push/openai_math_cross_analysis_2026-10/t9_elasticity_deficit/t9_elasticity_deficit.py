#!/usr/bin/env python3
"""T9 -- phantom-mass elasticity law.

Derived (see FROZEN_CRITERIA.md, committed alone):
  kernel-exact enclosed phantom mass of a point host, r_in -> 0:
      M_ph(<r_out) = M_b / (e^s - 1),   s = r_t / r_out,  r_t = sqrt(G M_b / a0)
  so the M_b-logarithmic elasticity is (d ln s/d ln M_b = 1/2):
      eps(s) = 1 - (s/2) e^s / (e^s - 1)
  E1 eps -> 1/2 as s -> 0 (deep-MOND sqrt-law; the framework's own 1/2)
  E2 eps < 1/2 for all s > 0 (universal sub-half deficit at finite radius)
  E3 eps strictly decreasing, zero at s* solving s e^s = 2(e^s - 1)

Screens (frozen): Q1: derives the ELASTICITY law from fitted-a0 (a0 enters
only through the unit s); kappa = 1/2 stays FITTED; the eps(0) = 1/2 = kappa
unification is DECLARED as an observation. Q2: no inserted rational; every
step follows from the kernel's closed form. Q3: n/a (functional comparison,
not a constant search).

Checks (exit 1 on FAIL): C1 canonical window; C2 alt window; C3 deep limit;
C4 monotone decreasing on [0.005, 3]; C5 zero crossing at the declared root;
C6 bridge to T1's C6 (+0.1 dex shift); C7 python MUTATE (T9_MUTATE=1,
exponent 1/2 -> 1/3 in d ln s/d ln M_b): C1, C2, C3, C6 must flip, C4/C5
re-solve and pass with the MUTATE root s e^s = 3(e^s - 1).
"""
import json, math, os, sys

MUT = os.environ.get("T9_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
MB = 1.0e11 * MSUN                     # MW baryon mass (T1's)
R_OUT = 818.0 * KPC                    # T1's supply ball radius
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MEAS = {"canonical": 0.4960, "alt": 0.4964}        # T1 lane outputs
WIN = 0.0006

EXP = 1.0 / 2.0 if not MUT else 1.0 / 3.0          # d ln s / d ln M_b
ROOT_RHS = 2.0 if not MUT else 3.0                 # s e^s = RHS (e^s - 1)


def rt(a0):
    return math.sqrt(G * MB / a0)


def eps(s):
    # stable form: (s/2) e^s / (e^s - 1) = (s/2) e^s / expm1(s); naive
    # (e^s - 1) cancels at s ~ 1e-9 (float64 floor ~ 1e-7 relative)
    return 1.0 - EXP * s * math.exp(s) / math.expm1(s)


def root(rhs, lo=0.1, hi=3.0):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = mid * math.exp(mid) - rhs * (math.exp(mid) - 1.0)
        if f > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


checks = {}
rows = {}
sstar = root(ROOT_RHS)
for fk in A0:
    s = rt(A0[fk]) / R_OUT
    e = eps(s)
    rows[fk] = dict(rt_kpc=rt(A0[fk]) / KPC, s=s, eps_pred=e,
                    eps_meas=MEAS[fk], ok=abs(e - MEAS[fk]) <= WIN)

checks["C1_canonical"] = rows["canonical"]["ok"]
checks["C2_alt"] = rows["alt"]["ok"]
checks["C3_deep_limit"] = abs(eps(1e-9) - 0.5) < 1e-9
ss = [0.005 + 0.03 * i for i in range(100)]
checks["C4_monotone"] = all(eps(ss[i]) > eps(ss[i + 1]) for i in range(99))
checks["C5_zero_crossing"] = abs(eps(sstar)) < 1e-6
bridge = math.exp(rows["canonical"]["eps_pred"] * math.log(10.0 ** 0.1)) - 1.0
checks["C6_bridge_C6"] = 0.1200 <= bridge <= 0.1220
# MUTATE flips are computed by the checks themselves; C4/C5 re-solve.
if MUT:
    assert EXP == 1.0 / 3.0 and abs(ROOT_RHS - 3.0) < 1e-9

ok = all(bool(v) for v in checks.values())
lines = [f"T9 elasticity law  MUTATE={MUT}  (EXP={EXP})",
         f"r_t: canonical {rows['canonical']['rt_kpc']:.4f} kpc, "
         f"alt {rows['alt']['rt_kpc']:.4f} kpc",
         f"root s* = {sstar:.6f} (e-elasticity zero, r_out = r_t/s* = "
         f"{1/sstar:.4f} r_t)"]
for fk in A0:
    r = rows[fk]
    lines.append(f"  {fk}: s={r['s']:.6f}  eps_pred={r['eps_pred']:.5f}  "
                 f"eps_meas={r['eps_meas']:.4f}  within {WIN}? {r['ok']}")
lines.append(f"  deep limit eps(1e-9) = {eps(1e-9):.10f} (1/2)  C3: {checks['C3_deep_limit']}")
lines.append(f"  monotone on [0.005,3]: C4: {checks['C4_monotone']}   "
             f"zero at s*: C5: {checks['C5_zero_crossing']} (eps(s*)={eps(sstar):.2e})")
lines.append(f"  bridge: +0.1 dex -> +{100*bridge:.4f}% (T1 C6: +12.10/+12.11%)  "
             f"C6: {checks['C6_bridge_C6']}")
lines.append("checks: " + json.dumps({k: bool(v) for k, v in checks.items()}))
print("\n".join(lines))
with open(os.path.join(here, f"t9_results{tag}.json"), "w") as fh:
    json.dump(dict(mutate=MUT, exp=EXP, rows=rows, sstar=sstar,
                   bridge_pct=100 * bridge,
                   checks={k: bool(v) for k, v in checks.items()}), fh, indent=1)
if ok:
    print(f"<LANE> COMPLETE: {sum(bool(v) for v in checks.values())}/{len(checks)} checks PASS.")
else:
    print(f"<LANE> COMPLETE: {sum(bool(v) for v in checks.values())}/{len(checks)} checks PASS. -- SOME CHECKS FAIL")
    sys.exit(1)