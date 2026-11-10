#!/usr/bin/env python3
"""MK2 row i (amendment A4 9754a17af7): is the exponential clock static out to the law's range around galaxies?
(a) the capped static state (A1 Hernquist x_a 0.2, A2 global cap, the dust's self-gravity) exists on the branch at each c_s;
(b) a cold shell's infall speed from FLD1's R_ta(z 0) in the static law potential (and in the baryons' Newtonian potential) at
10 / 100 / 300 / 1000 kpc against c_s; (c) sound-crossing times of 300 kpc, 1 Mpc and R_need = max(r_c, 1 Mpc) against the age t0
(F1A's B2 background per footing); (d) the law's range r_c beside FLD1's R_fold, ONE1's window edges and PD1's cap.
    python3 mk2_static.py -> mk2_static.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
import numpy as np
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk2_lib as L
G, MS, KPC, MPC, C = L.G, L.MSUN, L.KPC, L.MPC, L.C_SI
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
ONE = json.load(open(os.path.join(REPO, "fable52_push", "ONE1_counted_once", "one1.json"))); XP = {f: float(ONE["foot"][f]["X"]) for f in L.FOOT}
KD1 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
RHO = {f: KD1["footings"][f]["setting"]["I0_Mpc-2"] * C ** 2 / (8 * math.pi * G) / MPC ** 2 for f in L.FOOT}
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit"); OMR = 2.4728e-5 * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
CS = 10 ** (4.0 - 0.025 * np.arange(121))
# FLD1's inputs (A4 table; canonical physical kpc): log M_b -> (R_ta, R_fold0, inner edge, middle edge, R_cap)
FLD1 = {8.0: (40, 21, None, None, 23), 9.4: (120, 62, 81, 190, 116), 10.45: (268, 139, 272, 637, 389), 10.7: (325, 169, 362, 849, 518), 10.9: (378, 197, 456, 1069, 653)}
RADII = (10.0, 100.0, 300.0, 1000.0)
GYR = 3.15576e16
RES = dict(lane="MK2", row="i static to the law's range (A4)", note=L.NOTE, footings={})
P(f"MK2 row i (A4): masses {list(FLD1)}; radii {RADII} kpc. {L.NOTE}")
XA = 0.2; BH = L.hernquist(XA); GRID = L.Grid(BH, 1e-5, 1e5, h=0.01)
for f in L.FOOT:
    fit = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{f}_cold.json")))["pars"]; h = fit["h"]; Om = (fit["ob"] + fit["oc"]) / h ** 2; Or = OMR / h ** 2; OL = 1 - Om - Or
    H0 = 100 * h * 1e3 / MPC; t0 = quad(lambda a: 1 / (a * H0 * math.sqrt(Om / a ** 3 + Or / a ** 4 + OL)), 1e-12, 1.0, limit=200)[0] / GYR
    P(f"\n=== {f}: t0 = {t0:.3f} Gyr (F1A B2: h {h:.4f}, Omega_m {Om:.4f})")
    a0 = L.A0[f]; st0 = L.shoot_fast(GRID, 0, 0, 1, 0, XP[f], 1.0, 1.0, -10.0, first=True)
    def phi0(x):     # no-dust capped law potential (units s) at x = r / r_M
        if x <= st0["rc"]: return float(np.interp(math.log(x), st0["u"][:len(st0["Phi"])], st0["Phi"]))
        return -(st0["C"] / x + BH.tail(x))
    mass = {}
    for lm, (Rta, Rf, ein, emid, Rcap) in FLD1.items():
        M = 10 ** lm * MS; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0); alpha = 4 * math.pi * RHO[f] * rM ** 3 / M
        xta = Rta * KPC / rM
        vin = {}; vN = {}
        for r in RADII:
            x = r * KPC / rM
            if r >= Rta: vin[r] = 0.0; vN[r] = 0.0; continue
            vin[r] = math.sqrt(max(2 * s * (phi0(xta) - phi0(x)), 0.0)) / 1e3
            aa = XA * rM; vN[r] = math.sqrt(max(2 * G * M * (1 / (r * KPC + aa) - 1 / (Rta * KPC + aa)), 0.0)) / 1e3
        # (a) the capped static state along decreasing c_s
        Pv = st0["Phi0"]; alive = True; ex = []; rc = []
        for cs in CS:
            if alive:
                st = L.shoot_fast(GRID, 1, alpha, (cs * 1e3) ** 2 / s, 0, XP[f], 1.0, 1.0, Pv)
                if st["ok"]: Pv = st["Phi0"]; ex.append(True); rc.append(st["rc"] * rM / KPC); continue
                alive = False
            ex.append(False); rc.append(None)
        mass[lm] = dict(rM_kpc=rM / KPC, v_flat_kms=s ** 0.5 / 1e3, v_inf_law=vin, v_inf_newton=vN, exists=ex, r_c_kpc=rc,
                        fold_cs=(float(CS[ex.index(False)]) if False in ex else None), FLD1=dict(R_ta=Rta, R_fold0=Rf, inner=ein, middle=emid, R_cap=Rcap))
        P(f"  log M_b {lm}: v_flat {s ** 0.5 / 1e3:.0f} km/s; cold-shell infall from R_ta {Rta} kpc in the law potential at 10/100/300/1000 kpc: "
          + " / ".join(f"{vin[r]:.0f}" for r in RADII) + " km/s (Newtonian only: " + " / ".join(f"{vN[r]:.0f}" for r in RADII) + "); "
          f"static capped state folds below c_s {mass[lm]['fold_cs']}")
    per = []
    for j, cs in enumerate(CS):
        ok_a = all(mass[lm]["exists"][j] for lm in FLD1)
        sup = {lm: [r for r in RADII if mass[lm]["v_inf_law"][r] > cs] for lm in FLD1}; ok_b = all(not v for v in sup.values())
        rneed = max([1000.0] + [mass[lm]["r_c_kpc"][j] or 0.0 for lm in FLD1]); ts = {R: R * KPC / (cs * 1e3) / GYR for R in (300.0, 1000.0, rneed)}
        ok_c = ts[rneed] <= t0
        Rlaw = {lm: (mass[lm]["r_c_kpc"][j] if (mass[lm]["exists"][j] and not sup[lm] and ok_c) else None) for lm in FLD1}
        per.append(dict(cs=float(cs), a=ok_a, b=ok_b, c=ok_c, PASS=bool(ok_a and ok_b and ok_c), supersonic={str(k): v for k, v in sup.items()},
                        t_sound_Gyr={str(k): v for k, v in ts.items()}, R_law_kpc={str(k): v for k, v in Rlaw.items()}))
    ps = [p["cs"] for p in per if p["PASS"]]
    lab = (f"STATIC TO THE LAW'S RANGE [{min(ps):.4g}, {max(ps):.4g}] km/s" if ps else "NOT")
    contiguous = bool(ps) and all(any(abs(p["cs"] - c) < 1e-9 and p["PASS"] for p in per) for c in CS if min(ps) <= c <= max(ps))
    RES["footings"][f] = dict(t0_Gyr=t0, masses={str(k): v for k, v in mass.items()}, per_cs=per, label=lab, contiguous=contiguous)
    P(f"  [{f}] row i: {lab} (contiguous {contiguous})")
    for cs_ in (3000, 1000, 600, 500, 400, 300, 200, 100, 50):
        p = min(per, key=lambda q: abs(math.log(q['cs'] / cs_)))
        P(f"     c_s {p['cs']:7.1f}: (a) states {'all' if p['a'] else 'NOT all'}; (b) supersonic at " + ("nowhere" if p["b"] else "; ".join(f"{k}: {v}" for k, v in p["supersonic"].items() if v))
          + f"; (c) t_sound 300 kpc {p['t_sound_Gyr']['300.0']:.2f}, 1 Mpc {p['t_sound_Gyr']['1000.0']:.2f} Gyr (t0 {t0:.2f}) -> {'PASS' if p['PASS'] else 'FAIL'}; R_law " +
          ", ".join(f"{k}: {('%.0f' % v) if v else '-'}" for k, v in p["R_law_kpc"].items()))
P("\nBeside (FLD1, canonical kpc): log M_b: R_fold(0) / ONE1 inner / middle window edge / PD1 R_cap = " + "; ".join(f"{k}: {v[1]} / {v[2]} / {v[3]} / {v[4]}" for k, v in FLD1.items()))
P("What this does not show: a static and timescale argument, not an evolution run (A4).")
json.dump(RES, open(os.path.join(HERE, "mk2_static.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "mk2_static.out"), "w").write("\n".join(OUT + [L.NOTE]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
