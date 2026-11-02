#!/usr/bin/env python3
"""AR1 reader for the live validation (FROZEN_CRITERIA.md): Q live against the action solver and Blumenthal. Seed 1 is the frozen run; seeds 2, 3 added for scatter. Centre: centre of mass inside r0, DR8's fallback. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path[:0] = [HERE, os.path.join(RB, "DR8_pressure_core_response"), os.path.join(RB, "ZK1_fast_force_kernel"), os.path.join(RB, "LC1_live_contraction")]; import ar1_solver as A, dr8_ic as IC, dr8_live as DL
_a = sys.argv; sys.argv = [_a[0]]; import lc1_read as LR; sys.argv = _a
SS = json.load(open(os.path.join(HERE, "ar1_setup.json"))); OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(str(s))
RD = np.array([1, 2, 3, 4, 6, 8, 10.0]); RX = np.array([0.25, 0.5, 1, 2, 4])
for T in ("1e10", "1e13"):
    S = SS[T]; Rd, r0, R2, Md = S["Rd"], S["r0"], S["R2"], S["Md"]; rr = np.r_[RD * Rd, RX * r0]; _, _, _, Msim, Mod = IC.build("core", S, 100, 1, 0.1); frac = 1 - Md / Msim; FF = Md / (Msim - Md); rg = np.geomspace(max(1e-4 * R2, Mod.r[0]), R2, 1200); M0 = np.interp(np.log(rg), np.log(Mod.r), Mod.M) * frac; Mb = Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2)); Ma = A.act_contract(rg, Mb, M0, FF); Mbl = LR.contract(rg, Mb, M0, FF)[0]; Qa, Qb = (np.interp(np.log(rr), np.log(rg), y) / np.interp(np.log(rr), np.log(rg), M0) for y in (Ma[0], Mbl)); rows = []; R_ = {}
    for s in (1, 2, 3):
        fd, fn = (os.path.join(HERE, "runs", f"{T}_s{s}{t}", "snap_t7.70.npz") for t in ("", "_nodisc"))
        if not (os.path.exists(fd) and os.path.exists(fn)): continue
        Z, Y = np.load(fd), np.load(fn); ma = json.loads(str(Z["meta"])); m0 = float(Y["m"]); m1 = m0 * (1 - ma["Md_now"] / ma["Msim"]); cA, cB = DL.centre_com(Z["x"], r0, Z["c"]), DL.centre_com(Y["x"], r0, Y["c"]); rA, rB = np.sort(np.linalg.norm(Z["x"] - cA, axis=1)), np.sort(np.linalg.norm(Y["x"] - cB, axis=1)); nA, nB = np.searchsorted(rA, rr), np.searchsorted(rB, rr); Q = nA / np.maximum(nB, 1); e = Q * np.sqrt(1 / np.maximum(nA, 1) + 1 / np.maximum(nB, 1)); fa = (Q - 1) / (Qa - 1); fb = (Q - 1) / (Qb - 1); idx = [1, 2, 3]; rows.append(dict(s=s, Q=Q.tolist(), e=e.tolist(), N0=nB.tolist(), fA=float(np.median(fa[idx])), fB=float(np.median(fb[idx])), jump=ma["jump_rms"], faall=fa.tolist(), fball=fb.tolist()))
        P(f"{T} s{s}: f_A (2,3,4 R_d) {rows[-1]['fA']:.3f}, f_B {rows[-1]['fB']:.3f}; N no disc at 2,3,4 R_d {nB[idx].tolist()}; centre jump rms {ma['jump_rms']*1e3:.3f} kpc, eps {S['eps']*1e3:.3f} kpc")
    P(f"{T}: r0 {r0*1e3:.2f} kpc R_d {Rd*1e3:.2f} kpc R200 {R2*1e3:.1f} kpc M_d/M2 {Md/S['M2']:.3f} solver change {Ma[1]:.1e}"); P("  r/R_d " + " ".join(f"{x:g}" for x in RD) + " then r/r0 " + " ".join(f"{x:g}" for x in RX)); P("  Q act  " + " ".join(f"{x:.3f}" for x in Qa)); P("  Q blum " + " ".join(f"{x:.3f}" for x in Qb))
    if rows:
        Qm = np.median([r["Q"] for r in rows], axis=0); P("  Q live median " + " ".join(f"{x:.3f}" for x in Qm)); P("  Q live s1 err " + " ".join(f"{x:.3f}" for x in rows[0]["e"])); P("  f_A by radius " + " ".join(f"{x:.2f}" for x in (Qm - 1) / (Qa - 1))); P("  f_B by radius " + " ".join(f"{x:.2f}" for x in (Qm - 1) / (Qb - 1))); fm = float(np.median([r["fA"] for r in rows])); ln = rows[0]["fA"]; g = 0.85 <= ln <= 1.15; P(f"  VALIDATION {T}: seed 1 f_A {ln:.3f}, median of seeds {fm:.3f}, seeds {[round(r['fA'],3) for r in rows]}, line 0.85-1.15: {'VALIDATED' if g else 'ACTION SOLVER NOT VALIDATED AT THAT MASS'}; f_B median {np.median([r['fB'] for r in rows]):.3f}")
        RES[T] = dict(rows=rows, Qa=Qa.tolist(), Qb=Qb.tolist(), f_A_s1=ln, f_A_med=fm, validated=g, setup=S)
json.dump(RES, open(os.path.join(HERE, "ar1_live.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ar1_live.out"), "w").write("\n".join(OUT) + "\n")
