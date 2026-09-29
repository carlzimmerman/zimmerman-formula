#!/usr/bin/env python3
"""u3_2 -- final verdicts of lane U3: reads u3_1_results.json, applies lane D's bar (alpha_bar_checker.assess, log2size = log2 34, zero fitted reals) to the T-ABS variants,
applies the pre-registered verdict rules (DEAD / UNDECIDED / SURVIVES) to each of the 34 variants and the least-severe-variant headline to each of the 13 principles, prints the table.
Run:    python3 u3_2_verdicts.py            (real run, exit 0 iff the consistency checks C1-C4 pass)
MUTATE: python3 u3_2_verdicts.py --mutate   (control: the record of variant V01 is corrupted (status PASS although its T-JOINT failed); exactly check C1 must FAIL -> exit 1; anything else -> exit 3)
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np
import u3_lib as L
import alpha_bar_checker as BAR          # lane D, read only (located via u3_lib's sys.path insertion)

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag.split()[0])
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


D = json.load(open(os.path.join(HERE, "u3_1_results.json")))
rows = D["rows"]
if MUT:
    for r in rows:
        if r["id"] == "V01":
            r["status"] = "PASS"           # corrupt: V01 failed T-JOINT
LOG2N = math.log2(D["n_trials"])
print("=" * 130)
print("U3-2 verdicts -- mode: " + ("MUTATE CONTROL (V01 record corrupted)" if MUT else "REAL RUN") + f"   (family size {D['n_trials']}, log2 = {LOG2N:.2f})")
print("=" * 130)


def restate(r):
    """Recompute the stage-1 status of a row from its own recorded fields (the pre-registered rule)."""
    if not r.get("exists", True):
        return "DEAD"
    if r.get("domain_violation"):
        return "DEAD"
    if r["jpass"]:
        return "PASS"
    if r["mono_kill"]:
        return "DEAD"
    b = r.get("bridge")
    if b is None or not b["feasible"]:
        return "DEAD"
    return "UNDECIDED_BRIDGE" if max(b["N"]) <= 1.0 else "DEAD"


print()
chk("C0 34 records", len(rows) == 34)
bad = [r["id"] for r in rows if restate(r) != r["status"]]
chk("C1 every recorded status equals the status recomputed from its own fields by the pre-registered rule", not bad, f"(inconsistent: {bad})")
# bar sanity
r_pos = BAR.assess(delta=1e-12, log2size=LOG2N, predicted_precision=0.0, fitted_reals=0, verbose=False)
r_neg = BAR.assess(delta=0.01, log2size=LOG2N, predicted_precision=0.01, fitted_reals=0, verbose=False)
chk("C2 the bar clears a 1e-12 miss in a 34-member family and rejects a 1% miss even at predicted precision 1%", r_pos["clears"] and not r_neg["clears"], f"(P_neg = {r_neg['p']:.3g}, needs < 1e-3 and miss <= 5e-10 or 2x own precision: lambda = {r_neg['lam']:.3g})")
lam_min = L.N_TRIALS * 0.025 * 2 * 1e-3 / L.N_TRIALS
# the running-power statement: smallest delta_eff at which P < 1e-3 for a 34-member family with rho = RHO_DEFAULT
rho = BAR.RHO_DEFAULT
dmax = -math.log(1 - 1e-3) / (34 * rho * 2)
chk("C3 statement: with 34 trials the bar's P < 1e-3 needs delta_eff < %.2e, far below the 1%% floor of the running" % dmax, dmax < 1e-3)

# ---------------------------------------------------------------- bar on the T-ABS variants
print("\nLane D bar on the variants that fix alpha (both a_Y and a_2 absolute).  Implied Thomson value = 137.035999177 + (pred - run) for Y and 2 at the scale X; predicted precision = the variant's own tolerance:")
for r in rows:
    if r.get("fixes_alpha") and r.get("exists", True):
        b = BAR.assess(delta=r["implied_delta"], log2size=LOG2N, predicted_precision=r["implied_tol"], fitted_reals=0, n_targets=1, verbose=False)
        r["bar"] = dict(delta=b["delta"], p=b["p"], c1=b["c1_lookelsewhere"], c2=b["c2_precision"], clears=b["clears"], lam=b["lam"])
        print(f"  {r['id']} {r['label']:<52s} implied 1/alpha(0) = {r['implied_inv_alpha']:10.3f} (miss {r['implied_delta']:.3g}, spread over V {r['implied_spread']:.2f}, tol {r['implied_tol']:.3g}); bar: P = {b['p']:.3g}, c1 {b['c1_lookelsewhere']}, c2 {b['c2_precision']} -> {'CLEARS' if b['clears'] else 'does not clear'}")
chk("C4 no variant clears the bar unless it also passed T-JOINT (bar and joint test agree)", all((not r.get("bar", {}).get("clears")) or r["jpass"] for r in rows))

# ---------------------------------------------------------------- verdicts
def final_verdict(r):
    if r["status"] == "DEAD":
        return "DEAD"
    if r["status"] == "UNDECIDED_BRIDGE":
        return "UNDECIDED"
    # PASS of T-JOINT
    K = len(r["cen_r"])
    tind = r.get("fixes_alpha") and K >= 3 and r["J2"] and r.get("bar", {}).get("clears", False)
    return "SURVIVES" if tind else "UNDECIDED"


for r in rows:
    r["verdict"] = final_verdict(r)
rank = {"DEAD": 0, "UNDECIDED": 1, "SURVIVES": 2}

print("\nPER VARIANT")
print(f"{'id':4s} {'principle variant':<66s} {'scale X (GeV)':>11s}  {'worst |miss|/tol':>16s}  {'flag':4s} verdict / reason")
for r in rows:
    if r.get("exists", True):
        ratios = [abs(m) / t for m, t in zip(r["cen_r"], r["tol"])]
        w = max(ratios)
        xs = f"{r['X']:.2e}"
    else:
        w, xs = float("nan"), "none"
    flag = ("PHI" if r["phi"] else "") + ("*" if (r.get("exists", True) and not r["jpass"] and max(ratios) < 1.25) else "")
    print(f"{r['id']:4s} {r['label']:<66s} {xs:>11s}  {w:16.1f}  {flag:4s} {r['verdict']}: {r['reason'][:100]}")
print("  (worst |miss|/tol = the largest ratio of a constraint's miss to its own tolerance; * = fails by less than 25% of its tolerance, i.e. marginal; PHI = post-hoc informed)")

PRIN = {
    "P01": ("Dual-Coxeter coupling", "a_3 = 12 pi, a_2 = 8 pi, a_1 = 20 pi (a_Y = 100 pi/3) at X_P or X_S", "all three absolute (fixes alpha)"),
    "P02": ("GUT-group Coxeter at the crossing", "a_1 = a_2 at the SM crossing; a_3 = a_2; a_2 = 4 pi h, h in {5, 8, 12}", "a_3 (ratio), unified coupling"),
    "P03": ("Equal couplings at a Planckian scale", "a_1 = a_2 = a_3 (GUT) or a_Y = a_2 = a_3 (Y) at X_P, X_R, X_S", "two ratios"),
    "P04": ("Y-normalised universality at a pair crossing", "third coupling equals the pair at the a_Y=a_2, a_2=a_3, a_Y=a_3 crossing", "one ratio; scale is the crossing"),
    "P05": ("Fixed hypercharge-to-weak ratio", "a_Y/a_2 = n in {2, 3}, a_3 = a_2 at X_P, X_S", "two ratios"),
    "P06": ("Equal log-derivative magnitudes", "|b_i|/a_i equal for i = Y, 2, 3 at X_P, X_S", "two ratios"),
    "P07": ("Vanishing beta-weighted sum", "sum b_i a_i = 0 (Y or GUT norm) at X_P, X_S", "one relation"),
    "P08": ("RG invariant vanishes", "(b2-b3) a_1 + (b3-b1) a_2 + (b1-b2) a_3 = 0, scale-free", "one relation"),
    "P09": ("Species-scale emergence, all three", "a_Y = a_2 = a_3 = 0 at M_red/sqrt(N), N = 118, 126", "all three absolute (=0), fixes alpha"),
    "P10": ("Abelian emergence + Coxeter non-abelian", "a_Y = 0, a_2 = 8 pi, a_3 = 12 pi at X_S or X_R", "all three absolute, fixes alpha"),
    "P11": ("Anomaly-index coupling", "a_i = c I_i, (I_Y, I_2, I_3) = (10, 6, 6), c = 2 pi, 4 pi at X_P", "all three absolute, fixes alpha"),
    "P12": ("'t Hooft-coupling universality", "a_1 : a_2 : a_3 = 5 : 2 : 3 at X_P, X_S", "two ratios"),
    "P13": ("Heterotic string-scale locking", "a_1 = a_2 = a_3 at X = 0.216 g M_red, g^2 = 4 pi / a_2(X) (recalled)", "two ratios; scale self-consistent"),
}
print("\nPER PRINCIPLE (headline = least severe non-inapplicable variant)")
headline = {}
table = []
for pid, (name, eq, forces) in PRIN.items():
    vs = [r for r in rows if r["pid"] == pid]
    best = max(vs, key=lambda r: rank[r["verdict"]])
    hv = best["verdict"]
    headline[pid] = hv
    # smallest worst-ratio among variants (closest approach)
    closest = min(vs, key=lambda r: (min(9e9, max(abs(m) / t for m, t in zip(r["cen_r"], r["tol"]))) if r.get("exists", True) else 9e9))
    if closest.get("exists", True):
        cs = ", ".join(f"{n} {m:+.3f}/tol {t:.3f}" for n, m, t in zip(closest["names"], closest["cen_r"], closest["tol"]))
    else:
        cs = "no scale"
    nd = sum(1 for r in vs if r["verdict"] == "DEAD")
    nu = sum(1 for r in vs if r["verdict"] == "UNDECIDED")
    table.append(dict(pid=pid, name=name, eq=eq, forces=forces, headline=hv, n_variants=len(vs), n_dead=nd, n_undecided=nu, closest_variant=closest["id"], closest=cs, closest_reason=closest["reason"]))
    print(f"{pid} {name}: {hv}  ({len(vs)} variants: {nd} DEAD, {nu} UNDECIDED)  | closest {closest['id']}: {cs}")

tot = {k: sum(1 for r in rows if r["verdict"] == k) for k in rank}
print(f"\nSUMMARY: variants DEAD {tot['DEAD']}, UNDECIDED {tot['UNDECIDED']}, SURVIVES {tot['SURVIVES']} (of 34); principles by headline: " + ", ".join(f"{k} {sum(1 for h in headline.values() if h == k)}" for k in rank))
und = [r for r in rows if r["verdict"] == "UNDECIDED"]
for r in und:
    print(f"  UNDECIDED: {r['id']} {r['label']} -- {r['reason']}" + ("  [PHI: post-hoc informed, not a prediction]" if r["phi"] else ""))
print("\nFAILED checks:", FAILED if FAILED else "none")
if not MUT:
    json.dump(dict(rows=rows, principles=table, headline=headline, summary=tot), open(os.path.join(HERE, "u3_2_verdicts.json"), "w"), indent=1, default=float)
if MUT:
    works = sorted(FAILED) == ["C1"]
    print("MUTATE CONTROL:", "works (exactly C1 failed) -> exit 1" if works else "CONTROL BROKEN (exit 3): exactly C1 must fail")
    sys.exit(1 if works else 3)
sys.exit(0 if not FAILED else 1)
