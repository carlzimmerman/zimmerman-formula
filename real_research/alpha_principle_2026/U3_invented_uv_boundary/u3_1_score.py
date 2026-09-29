#!/usr/bin/env python3
"""u3_1 -- scores the 34 pre-registered variants of the 13 invented UV boundary principles (U3_PREREGISTRATION.md): T-JOINT, T-DOMAIN, T-MONO, T-BRIDGE, J2, T-ABS implied alpha.
Writes u3_1_results.json (the input of u3_2_verdicts.py).  The real run exits 0 iff the machinery controls K0-K5 pass (the VERDICTS are data, not exit codes).
Run:    python3 u3_1_score.py            (real run, exit 0)
MUTATE: python3 u3_1_score.py --mutate   (control: the positive-control synthetic rule K1 (the central run's own values, which must PASS) is perturbed by 8%; exactly K1 must FAIL -> exit 1; anything else -> exit 3)
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np
import u3_lib as L

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag.split()[0])
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 110)
print("U3-1 scorer -- mode: " + ("MUTATE CONTROL (K1 synthetic rule perturbed by 8%)" if MUT else "REAL RUN"))
print("=" * 110)

VAR = L.make_variants()
print(f"\nK0  registered variants: {len(VAR)}; principles: {len(set(v['pid'] for v in VAR))}")
chk("K0 34 variants of 13 principles, ids unique", len(VAR) == L.N_TRIALS and len({v['id'] for v in VAR}) == 34 and len({v['pid'] for v in VAR}) == 13)

# ---------------------------------------------------------------- controls
cen_t = L.get_traj("2L-T")
Aref = cen_t.A(L.XP)
def syn(pred):
    return L.mkv("SYN", "synthetic", ("fixed", L.XP), dict(pred=list(pred)), kind="abs")
ev1 = L.evaluate_bands(syn(Aref * (1.08 if MUT else 1.0)))
lam1, P1 = L.look_elsewhere(1, ev1["tol"])
print(f"\nK1  positive control: synthetic rule = the central run's own values at X_P{' x 1.08 (MUTATED)' if MUT else ''}: residuals {np.round(ev1['cen_r'], 4)}, tol {np.round(ev1['tol'], 4)}, family 1: lambda = {lam1:.2e}, P = {P1:.2e}")
chk("K1 positive control (the run's own values) passes T-JOINT and J2 with family size 1", ev1["pass"] and P1 < 1e-3)
ev2 = L.evaluate_bands(syn(Aref * 1.08))
print(f"K2  negative control: same values x 1.08: residuals {np.round(ev2['cen_r'], 4)}, tol {np.round(ev2['tol'], 4)}")
chk("K2 negative control (+8%) fails T-JOINT", not ev2["pass"])
Ntrue = np.array([1.3, 0.7, 2.1])
predN = L.Shifted(cen_t, Ntrue).A(L.XP)
vN = syn(predN)
bN = L.bridge(vN)
print(f"K3  bridge solver on a synthetic rule generated with N = {Ntrue.tolist()}: recovered N = {None if bN['N'] is None else np.round(bN['N'], 4).tolist()}, max residual {bN['maxres']}")
chk("K3 T-BRIDGE recovers a known N to 1e-3", bN["feasible"] and np.allclose(bN["N"], Ntrue, atol=1e-3))
lam, Pp = L.look_elsewhere(1, [0.01, 0.01, 0.01])
chk("K4 J2 formula: lambda = prod(2 tol / ln 100) for tol = 1% x3, family 1", abs(lam - (0.02 / math.log(100)) ** 3) < 1e-18)
class Fake:
    lnmax = math.log(1e30)
    def A(self, mu):
        l = math.log(mu / 100.0)
        return np.array([50.0 - 1.0 * l, 20.0 + 0.5 * l, 10.0 + 2.0 * l])
xc = L.solve_cross(Fake(), "a2", "a3")
xexp = 100.0 * math.exp(10.0 / 1.5)
chk("K5 crossing solver on a synthetic trajectory (a_2 = a_3 at 100 exp(10/1.5))", xc is not None and abs(xc / xexp - 1) < 1e-8, f"({xc:.6e} vs {xexp:.6e})")

# ---------------------------------------------------------------- the 34 variants
rows = []
for v in VAR:
    ev = L.evaluate_bands(v)
    rec = dict(id=v["id"], pid=v["pid"], label=v["label"], kind=v["kind"], fixes_alpha=v["fixes_alpha"], param_scale=v["param_scale"], phi=v["phi"])
    rec["exists"] = ev["exists"]
    if not ev["exists"]:
        rec.update(X=None, status="DEAD", reason="the required crossing / self-consistent scale does not exist below 1e40 GeV" if ev["X"] is None else "scale beyond the integrated range")
        rows.append(rec)
        print(f"{v['id']} {v['pid']} {v['label']:<70s} NO SCALE -> DEAD")
        continue
    X = ev["X"]
    rec.update(X=X, names=ev["names"], cen_r=ev["cen_r"].tolist(), band=ev["band"].tolist(), tol=ev["tol"].tolist(), pass_k=[bool(b) for b in ev["pass_k"]], jpass=ev["pass"],
               A_at_X=(None if ev["A"] is None else ev["A"].tolist()), runs=ev["runs"])
    rec["domain_violation"] = bool(v["xspec"][0] in ("cross", "hetero") and X > 1.001 * L.XP)
    lam, P = L.look_elsewhere(L.N_TRIALS, ev["tol"])
    rec.update(lam=lam, P=P, J2=bool(P < 1e-3))
    mk, hits = L.mono_kill(v, ev)
    rec.update(mono_kill=mk, mono_hits=hits)
    # T-ABS implied alpha
    if v["fixes_alpha"]:
        imp = {}
        for name in L.VARIANTS_RUN:
            r_ = L.residuals(v, L.Shifted(L.get_traj(name), None))
            imp[name] = ALPHA = L.ALPHA_INV0 + (r_["pred"][0] - r_["A"][0]) + (r_["pred"][1] - r_["A"][1])
        if v["param_scale"]:
            for xf in (0.5, 2.0):
                r_ = L.residuals(v, L.Shifted(cen_t, None), xfac=xf)
                imp[f"X x{xf}"] = L.ALPHA_INV0 + (r_["pred"][0] - r_["A"][0]) + (r_["pred"][1] - r_["A"][1])
        c = imp["2L-T"]
        spread = max(abs(x - c) for x in imp.values())
        rec.update(implied_inv_alpha=c, implied_spread=spread, implied_delta=abs(c / L.ALPHA_INV0 - 1), implied_tol=max(2 * spread / L.ALPHA_INV0, 0.01), implied_runs=imp)
    # verdict stage 1
    if rec["domain_violation"]:
        rec.update(status="DEAD", reason=f"T-DOMAIN: scale {X:.3e} GeV is {X / L.XP:.3g} x M_P (above the programme's cutoff)")
    elif ev["pass"]:
        rec.update(status="PASS", reason="T-JOINT passed for all constraints")
    elif mk:
        rec.update(status="DEAD", reason="T-MONO: predicts " + ", ".join(hits) + " ABOVE the SM-desert run beyond tolerance; no added matter can repair it")
    else:
        rec.update(status="FAIL", reason="T-JOINT failed; T-BRIDGE decides")
    if rec["status"] in ("FAIL",) or (rec["status"] == "DEAD" and not rec["domain_violation"]):
        br = L.bridge(v)
        rec["bridge"] = br
        if rec["status"] == "FAIL":
            if not br["feasible"]:
                rec.update(status="DEAD", reason="T-BRIDGE infeasible: " + br.get("reason", ""))
            elif max(br["N"]) <= 1.0:
                rec.update(status="UNDECIDED_BRIDGE", reason=f"T-JOINT failed, but <= 1 unforced multiplet of each type at 1 TeV rescues it: N = {np.round(br['N'], 3).tolist()}")
            else:
                rec.update(status="DEAD", reason=f"T-BRIDGE needs more than 1 unforced multiplet: N = {np.round(br['N'], 3).tolist()}")
    rows.append(rec)
    rs = " ".join(f"{n}:{r:+.3f}(tol {t:.3f})" for n, r, t in zip(ev["names"], ev["cen_r"], ev["tol"]))
    print(f"{v['id']} {v['pid']} {v['label']:<70s} X={X:.3e}  {rs}  -> {rec['status']}")

with open(os.path.join(HERE, "u3_1_results" + ("_MUTATE" if MUT else "") + ".json"), "w") as f:
    json.dump(dict(n_trials=L.N_TRIALS, rows=rows), f, indent=1, default=float)

print("\nFAILED controls:", FAILED if FAILED else "none")
if MUT:
    works = sorted(FAILED) == ["K1"]
    print("MUTATE CONTROL:", "works (exactly K1 failed) -> exit 1" if works else "CONTROL BROKEN (exit 3): exactly K1 must fail")
    sys.exit(1 if works else 3)
sys.exit(0 if not FAILED else 1)
