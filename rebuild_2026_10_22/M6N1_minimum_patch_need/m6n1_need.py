#!/usr/bin/env python3
"""M6N1_minimum_patch_need: minimum cosmic baryon fraction M6's depleted patches must hold for the galaxies that need
M6, against X57's provisional patch budget. FROZEN_CRITERIA.md committed alone first (3a2f5ca3a0).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I m6n1_need.py      (M6N1_MUTATE=1 twin)
"""
import os, sys, json, hashlib, resource, time
import numpy as np

MUT = os.environ.get("M6N1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
T0 = time.time()
OUT = open(os.path.join(HERE, f"m6n1_need{TAG}.out"), "w")
RES = {"lane": "M6N1_minimum_patch_need", "criteria": "3a2f5ca3a0", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def dump():
    RES["elapsed_s"] = time.time() - T0
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    json.dump(RES, open(os.path.join(HERE, f"m6n1_need_results{TAG}.json"), "w"), indent=1, default=float)


FOOTS = ("canonical", "alt")
P("M6N1_minimum_patch_need" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria 3a2f5ca3a0; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
POP = os.path.join(REPO, "closure_program_2026_10_27", "population", "run", "results.json")
SHA = "0131d5da47e442c92dfd716fda8b5d036b0808940079fc8e0dd62d2445746323"
if MUT:
    SHA = SHA[:-1] + "0"                                                       # m2
sha_ok = hashlib.sha256(open(POP, "rb").read()).hexdigest() == SHA
pop = json.load(open(POP))
p1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json")))
x22 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")))
FINV = {"stellar": pop["census"]["F_star"], "stars+cold gas": pop["census"]["F_cold_baseline"]}
Q = {"q_lo (ungrouped 0.30)": 0.30, "q_hi (1e9-1e11)": pop["gsmf"]["mass_ranges"]["1e9_to_1e11"]["fraction_of_fitted_stellar_mass"]}
FALLOW = {f: p1["backgrounds"]["native"]["m6"][f]["Fb_max_z3"] for f in FOOTS}
DBI = {f: p1["backgrounds"]["native"]["m6"][f]["delta_b_in"] for f in FOOTS}
FMAX = {f: x22["step2"]["per_footing"][f]["f_max"] for f in FOOTS}
tgt = [(FINV["stellar"], 0.046987), (FINV["stars+cold gas"], 0.059787), (Q["q_hi (1e9-1e11)"], 0.69145),
       (FALLOW["canonical"], 0.06132), (FALLOW["alt"], 0.04895)]
rep_ok = all(round(a, 4) == round(b, 4) for a, b in tgt)
s0 = sha_ok and rep_ok
P(f"  sha256 {'OK' if sha_ok else 'MISMATCH'}; inputs reproduced (4 dp) {rep_ok}: F_star {FINV['stellar']:.6f}, F_cold {FINV['stars+cold gas']:.6f}, "
  f"q_hi {Q['q_hi (1e9-1e11)']:.5f}, F_allowed {FALLOW['canonical']:.5f}/{FALLOW['alt']:.5f}")
P("  " + "; ".join(f"{f}: f_max {FMAX[f]:.5f}, delta_b,in {DBI[f]:.5f}" for f in FOOTS))
check("S0", s0, f"sha {sha_ok}, reproduce {rep_ok}", "all")
RES["inputs"] = {"F_inv": FINV, "q": Q, "F_allowed": FALLOW, "delta_b_in": DBI, "f_max": FMAX}
if not s0 and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"; dump(); sys.exit(1)


def r_of_x(x, fm, dbi):
    return (1 - x) + x * fm / (1 + dbi)


def xmin_closed(fm, dbi):
    if MUT:
        return 0.0                                                             # m1: wrong cap r <= 1
    return (1 - fm) / (1 - fm / (1 + dbi))


# K1 brute force on the frozen cap r <= f_max
k1 = 0.0
grid = np.arange(0, 1 + 1e-12, 1e-7)
for f in FOOTS:
    ok = grid[r_of_x(grid, FMAX[f], DBI[f]) <= FMAX[f] + 1e-15]
    k1 = max(k1, abs(ok.min() - xmin_closed(FMAX[f], DBI[f])))
check("K1", k1 <= 1e-6, f"closed-form x_min vs brute force: max |diff| {k1:.1e}", "<= 1e-6")
# K2 identity
d = DBI["canonical"]; epsr = 1 / (1 + d)
k2 = abs(1.0 * 1.0 * (1 / (1 + d)) / epsr - 1.0)
check("K2", k2 <= 1e-12, f"x=1, q=1, F_inv=1/(1+delta), eps=eps_ref -> F_need = {1 + k2:.12f}", "== 1")
# K3 limits (use the frozen closed form, not the twin's)
true_x = lambda fm, dbi: (1 - fm) / (1 - fm / (1 + dbi))
k3 = abs(true_x(1 - 1e-12, 4.0)) < 1e-9 and abs(true_x(1e-12, 4.0) - 1) < 1e-9
check("K3", k3, "f_max -> 1 gives x_min -> 0; f_max -> 0 gives x_min -> 1", "limits")

# ============================================================== requirement
RES["footings"] = {}
for f in FOOTS:
    xm = xmin_closed(FMAX[f], DBI[f])
    eref = 1 / (1 + DBI[f])
    Fa = FALLOW[f]
    P(f"\n== {f.upper()}: f_max {FMAX[f]:.4f}, delta_b,in {DBI[f]:.4f} -> x_min {xm:.4f}; eps_ref = 1/(1+delta_b) {eref:.4f}; F_allowed {Fa:.5f} (provisional)")
    corners = {}
    for qn, q in Q.items():
        for fn, Fi in FINV.items():
            Fmin = xm * q * Fi
            Fref = Fmin / eref
            corners[f"{qn} | {fn}"] = {"q": q, "F_inv": Fi, "F_need_min": Fmin, "F_need_eps_ref": Fref, "eps_crit": Fmin / Fa,
                                       "min_ok": Fmin <= Fa, "ref_ok": Fref <= Fa, "q_at_budget_full_retention": Fa / (xm * Fi) if xm > 0 else float("inf")}
            c = corners[f"{qn} | {fn}"]
            P(f"  {qn:24s} {fn:15s}: F_need,min {Fmin:.4f} ({Fmin / Fa:.2f} x budget); at eps_ref {Fref:.4f} ({Fref / Fa:.2f} x); "
              f"eps_crit {c['eps_crit']:.3f} vs eps_ref {eref:.3f}; q at budget (eps=1) {c['q_at_budget_full_retention']:.3f}")
    mins = [c["min_ok"] for c in corners.values()]; refs = [c["ref_ok"] for c in corners.values()]
    if not any(mins):
        v = "M6 OVER BUDGET EVEN AT FULL RETENTION"
    elif all(mins) and not any(refs):
        v = "BUDGET BINDS AT RECORD RETENTION"
    elif all(refs):
        v = "BUDGET DOES NOT BIND"
    else:
        flips = [k for k, c in corners.items() if not (c["min_ok"] and not c["ref_ok"])]
        v = "MIXED (corners not in the BINDS pattern: " + "; ".join(flips) + ")"
    P(f"  ==> {f}: {v}")
    RES["footings"][f] = {"x_min": xm, "eps_ref": eref, "F_allowed": Fa, "corners": corners, "verdict": v}

peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("K4", peak < 1.0, f"peak RSS {peak:.3f} GB", "< 1 GB")
P(f"\n== VERDICT: " + "; ".join(f"{f}: {RES['footings'][f]['verdict']}" for f in FOOTS))
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
dump()
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
