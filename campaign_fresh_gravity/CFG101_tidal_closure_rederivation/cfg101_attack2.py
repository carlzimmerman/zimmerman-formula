#!/usr/bin/env python3
"""
CFG101 ATTACK-2 (POST-HOC addendum; declared after cfg101_attack.py had run).  Frozen before this script's first run.
Reason: in cfg101_attack.py the (a,b,c) LP with ghost-freedom alone (1 + h >= 0) was UNBOUNDED (a_f/g_tot ~ 1e3 at the +-1e4 box wall): ghost-freedom does not bound the force once the coupling is not restricted to the tidal line,
because directions with h >= 0 everywhere can be scaled without limit.  Such large positive h is not a ghost but is far outside the regime where 'Pi fixed and force = energy gradient' is a dynamics (metric factors O(h) dropped).
So the meaningful question is: ghost-free AND bounded, |h_rr|, |h_perp| <= H at every r (H = 0.3, 1, 3), using the same conventions/functions as cfg101_attack.py (imported, unchanged).
For each H and each fluid-side definition (D_c4, D_full):
   O1 (0.3h,1h,3h), O2 (uniform support on [0.3,3]h) for the tidal line and the full (a,b,c) family;
   O3: minimal reaction  rho_min(t0) = min max_{[0.3,3]h}|a_react|/g_tot  s.t. a_f/g_tot >= t0 on [0.3,3]h, at eps = 2.741 / 0.6141 / 0.01717 (M_b = 1e9 / 1e10 / 1e12 with CFG50's h = 2/3/5 kpc,
   recovered in the main run), t0 in {0.05, 0.1, 0.3}; the diagnostic is rho_min/t0 (dimensionless reaction cost of a unit of support).  ghost + |h|<=H are affine so rho_min/t0 is t0-independent while the H bound is slack; a change with t0 shows the bound biting.
Controls: (1) tidal line with H = 1 reproduces cfg101_main's D_c4 values 0.337 / 0.494 / 0.143 at 0.3h / 1h / 3h to 3e-3; (2) the full family >= tidal line (superset); (3) O1 finite (below box) for every H.
MUTATE=1: tidal line replaced by b = +a; control (1) must FAIL.  Exit 0 iff controls pass.  No pass line is claimed for the physics values; they are reported.
"""
import os, sys, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("atk", HERE / "cfg101_attack.py")
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
MUT = os.environ.get("MUTATE", "0")
OUT = HERE / f"cfg101_attack2_results{'' if MUT=='0' else '_MUTATE_'+MUT}.json"
CH = []; NUM = {}
def check(n, ok, d=""):
    CH.append((n, bool(ok), d)); print(f"[{'PASS' if ok else 'FAIL'}] {n} :: {d}")

def box_rows(H):
    hrr, hp, _, _ = A.rows(A.SGL)
    Ag = np.vstack([-hrr, -hp, hrr, hp]); bg = np.concatenate([np.ones(2 * len(A.SGL)), H * np.ones(2 * len(A.SGL))])
    # ghost 1+h>=0 -> -h<=1 ; boundedness h<=H
    Ag2 = np.vstack([-hrr, -hp]); bg2 = np.concatenate([np.minimum(1.0, H) * np.ones(len(A.SGL)), np.minimum(1.0, H) * np.ones(len(A.SGL))])
    # |h|<=H : -h<=H ; if H<1 the ghost condition is implied.  Use the tighter of (1, H) on the negative side.
    return Ag, bg, Ag2, bg2

def constraints(H):
    hrr, hp, _, _ = A.rows(A.SGL)
    neg = min(1.0, H)
    Aub = np.vstack([-hrr, -hp, hrr, hp]); bub = np.concatenate([neg * np.ones(2 * len(A.SGL)), H * np.ones(2 * len(A.SGL))])
    return Aub, bub

def tidal_eq(nvar):
    a = 1.0 if MUT == "0" else -1.0
    Aeq = np.zeros((2, nvar)); Aeq[0, 0] = a; Aeq[0, 1] = 1.0; Aeq[1, 2] = 1.0
    return Aeq, np.zeros(2)

def solve(cost, Aub, bub, nvar, tidal, bounds=None):
    Aeq, beq = (tidal_eq(nvar) if tidal else (None, None))
    if bounds is None: bounds = [(-1e4, 1e4)] * nvar
    return linprog(cost, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")

def O1(row, H, tidal):
    Aub, bub = constraints(H)
    r = solve(-row, Aub, bub, 3, tidal)
    return (-r.fun if r.status == 0 else float('nan')), r

def O2(Arows, H, tidal):
    Aub, bub = constraints(H)
    A1 = np.vstack([np.hstack([Aub, np.zeros((Aub.shape[0], 1))]), np.hstack([-Arows, np.ones((Arows.shape[0], 1))])])
    b1 = np.concatenate([bub, np.zeros(Arows.shape[0])])
    r = solve(np.array([0, 0, 0, -1.0]), A1, b1, 4, tidal, bounds=[(-1e4, 1e4)] * 4)
    return (r.x[3] if r.status == 0 else float('nan')), r

def O3(Aaf, Ar, t0, H, tidal):
    Aub, bub = constraints(H)
    n = Ar.shape[0]
    A1 = np.vstack([np.hstack([Aub, np.zeros((Aub.shape[0], 1))]), np.hstack([Ar, -np.ones((n, 1))]), np.hstack([-Ar, -np.ones((n, 1))]), np.hstack([-Aaf, np.zeros((Aaf.shape[0], 1))])])
    b1 = np.concatenate([bub, np.zeros(2 * n), -t0 * np.ones(Aaf.shape[0])])
    r = solve(np.array([0, 0, 0, 1.0]), A1, b1, 4, tidal, bounds=[(-1e4, 1e4)] * 3 + [(0, 1e6)])
    return (r.x[3] if r.status == 0 else float('nan')), r

def main():
    SW = A.SW
    defs = {"c4": A.af_rows_c4, "full": A.af_rows_full}
    eps_list = {"1e9": 2.741, "1e10": 0.6141, "1e12": 0.01717}
    gts = {k: A.gtot(e, SW) for k, e in eps_list.items()}
    ctrl1 = None
    for H in (0.3, 1.0, 3.0):
        print(f"\n=========== |h| <= {H} (ghost side 1+h>=0 too) ===========")
        for dn, fn in defs.items():
            Aw = fn(SW)
            for lab, tid in (("tidal", True), ("full(a,b,c)", False)):
                o1 = [O1(fn(np.array([s0]))[0], H, tid)[0] for s0 in (0.3, 1.0, 3.0)]
                o2, r2 = O2(Aw, H, tid)
                NUM[f"H{H}|{dn}|{lab}|O1"] = o1; NUM[f"H{H}|{dn}|{lab}|O2"] = float(o2)
                print(f" D_{dn:4s} {lab:12s}: O1 (0.3h,1h,3h) = {o1[0]:9.4f} {o1[1]:9.4f} {o1[2]:9.4f};  O2 = {o2:9.4f}" + (f"  (a,b,c)={np.round(r2.x[:3],3)}" if r2.status == 0 else ""))
                if dn == "c4" and lab == "tidal" and H == 1.0: ctrl1 = o1
                # O3
                for k, e in eps_list.items():
                    Ar = A.react_rows(SW, e, gts[k])
                    vals = []
                    for t0 in (0.05, 0.1, 0.3):
                        v, _ = O3(Aw, Ar, t0, H, tid)
                        vals.append(v)
                    NUM[f"H{H}|{dn}|{lab}|O3|{k}"] = [float(v) for v in vals]
                    print(f"      O3 M_b={k}: rho_min at t0=0.05,0.1,0.3 = " + ", ".join(f"{v:8.4f}" for v in vals) + "   rho_min/t0 = " + ", ".join(f"{v/t:7.3f}" for v, t in zip(vals, (0.05, 0.1, 0.3))))
    ok1 = ctrl1 is not None and all(abs(a - b) < 3e-3 for a, b in zip(ctrl1, (0.337, 0.494, 0.143)))
    check("control 1: tidal line, D_c4, |h|<=1 reproduces main-run 0.337/0.494/0.143 at 0.3h/1h/3h", ok1, str(ctrl1))
    # superset + finiteness
    ok2 = True; ok3 = True
    for H in (0.3, 1.0, 3.0):
        for dn, fn in defs.items():
            for s0 in (0.3, 1.0, 3.0):
                row = fn(np.array([s0]))[0]
                a1 = O1(row, H, True)[0]; a2 = O1(row, H, False)[0]
                ok2 &= (a2 >= a1 - 1e-6); ok3 &= (abs(a2) < 5e3)
    check("control 2: full family >= tidal line for every H, definition, radius", ok2, "")
    check("control 3: O1 finite (< box) once |h| <= H is imposed", ok3, "")
    nf = sum(1 for c in CH if not c[1])
    NUM["checks"] = CH
    OUT.write_text(json.dumps(NUM, indent=1, default=float))
    print(f"\nMUTATE={MUT}: {len(CH)-nf}/{len(CH)} controls pass")
    sys.exit(0 if nf == 0 else 1)

if __name__ == "__main__":
    main()
