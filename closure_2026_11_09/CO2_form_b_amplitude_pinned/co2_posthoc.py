#!/usr/bin/env python3
"""CO2 POST HOC (written after row P4 was graded; reported only, changes no label): the reference run's own large-scale
realisation noise, and what P4 reads when it is taken out.

Found after grading: CFG596's S0 run (one L = 100 Mpc/h box) starts with r(k) = P(z_i) / (D_i^2 P_lin) far from 1 in its
lowest bins (0.80, 1.03, 1.48 at k = 0.08, 0.14, 0.20 h/Mpc), and the pattern is still there at z = 0. A difference of two
models on the same run (CO1's d_cold) cancels it; an absolute fit (P4) does not.

Two corrections, each applied to the S0 nodes before the amplitude move (the response alpha(k) is a ratio of snapshots, so
a k-only factor leaves it unchanged):
  R1  the run's own initial spectrum: P(k, z) / r(k)^w(k), w = 1 for k <= 0.3, falling linearly in ln k to 0 at k = 1
      (variant R1b: w = 1 for k <= 0.2, 0 at k = 0.5).
  R2  an independent realisation at low k: CFG411's S0 run with L = 200 Mpc/h, N 512 (eight times the modes per bin) spliced
      in below k = 0.5, the L = 100 run above, in the manner of CFG596's pre-flight (R2b: CFG424's S0 run, seed 360, the same).

  nice -n 10 python3 co2_posthoc.py     -> co2_posthoc.json, co2_posthoc.out      (after co2_shear.py)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, glob, time, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "co2_shear.py")).read(); cut = src.index("# ------------------------------------------------------------------ the response and KA5")
NS = {"__file__": os.path.join(HERE, "co2_shear.py"), "__name__": "co2_shear_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "co2_shear.py", "exec"), NS)       # CFG592 library, S0 nodes, response, run_of, fitp, lab
import numpy as np
G, K, SN, HM, ROWS, FOOTS, fitp, lab, ONE, BASE = (NS[k] for k in ("G", "K", "SN", "HM", "ROWS", "FOOTS", "fitp", "lab", "ONE", "BASE"))
PZ0 = {z: p.copy() for z, p in NS["PZ"].items()}
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
r = np.array(SN["zi"]["P"]) / (SN["zi"]["D"] ** 2 * G["P_lin0"](K))
def weight(k1, k2): return np.clip(1 - np.log(np.maximum(K, k1) / k1) / math.log(k2 / k1), 0, 1)
CORR = {"R1": r ** weight(0.3, 1.0), "R1b": r ** weight(0.2, 0.5)}
# R2 / R2b: two independent L = 200 Mpc/h S0 runs (N 512) below k = 0.5
def load200(rel):
    J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"])
    r2 = np.array(S2["zi"]["P"]) / (S2["zi"]["D"] ** 2 * G["P_lin0"](np.array(S2["zi"]["k"])))
    def splice(z, key):
        p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"])))); out = PZ0[z].copy(); m = K < 0.5; out[m] = p2[m]; return out
    return k2, r2, {0.0: splice(0.0, "z0"), 0.5: splice(0.5, "z0.5"), 1.0: splice(1.0, "z1")}, [S2[x]["D"] / SN[x]["D"] for x in ("z1", "z0.5")]
k2, r2, PZ_R2, dchk = load200(("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))
k2b, r2b, PZ_R2b, dchkb = load200(("cfg424_work", "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json"))
RES = dict(lane="CO2", part="POST HOC realisation check (reported; changes no label)", criteria="2bd776c60d", note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           r_L100=dict(k=K[:12].tolist(), r=r[:12].tolist()), r_L200=dict(run="CFG411 S0 L200 N512", k=k2[:12].tolist(), r=r2[:12].tolist(), D_ratio_check=dchk), r_L200b=dict(run="CFG424 S0 L200 N512 seed 360", k=k2b[:12].tolist(), r=r2b[:12].tolist(), D_ratio_check=dchkb),
           rows={})
P("CO2 POST HOC (reported, changes no label): the reference run's large-scale realisation noise and P4 without it.")
P("  L = 100 run, P(z_i) / (D_i^2 P_lin) in its first bins: " + ", ".join(f"k {a:.3f}: {b:.3f}" for a, b in zip(K[:8], r[:8])))
P("  L = 200 run (CFG411 S0, N 512), the same: " + ", ".join(f"k {a:.3f}: {b:.3f}" for a, b in zip(k2[:10], r2[:10])))
P("  L = 200 run (CFG424 S0, N 512, seed 360), the same: " + ", ".join(f"k {a:.3f}: {b:.3f}" for a, b in zip(k2b[:10], r2b[:10])))
P(f"  splice check: L = 200 over L = 100 at z = 0 for the bins below k 0.5: " + ", ".join(f"{a:.3f}: {b:.3f}" for a, b in zip(K[K < 0.5], (PZ_R2[0.0] / PZ0[0.0])[K < 0.5])))
def setP(pz): NS["PZ"].update(pz)
def rows_for(tag, pz):
    setP(pz); out = {}
    for ft in FOOTS:
        Rt = HM["primary"][ft]["R_tot"]; s8 = ROWS["P2"][ft]["sigma8"]; s8n = ROWS["brackets"][ft]["one_0p06eV_neutrino"]["sigma8"]
        main = fitp("KiDS", Rt, s8); eng = fitp("KiDS", Rt, 0.811); nu = fitp("KiDS", Rt, s8n); s0 = fitp("KiDS", ONE, 0.811)
        grid = np.arange(0.70, 0.9001, 0.0125); c2 = np.array([fitp("KiDS", Rt, float(s))["chi2"] for s in grid]); i = int(np.argmin(c2))
        lo_, hi_ = max(i - 2, 0), min(i + 3, len(grid)); co = np.polyfit(grid[lo_:hi_], c2[lo_:hi_], 2); sb = float(-co[1] / (2 * co[0])); wid = 1 / math.sqrt(co[0]); best = fitp("KiDS", Rt, sb)
        des = fitp("DES", Rt, s8)
        out[ft] = dict(pinned=main, label_if_it_were_graded=lab(main["p"]), engine_sigma8=eng, S0_alone_engine=s0, one_0p06eV_neutrino=nu, best_sigma8=sb, width=wid, best=best,
                       pinned_minus_best_in_widths=(s8 - sb) / wid, dchi2_pinned_vs_best=main["chi2"] - best["chi2"], nu_minus_best_in_widths=(s8n - sb) / wid, DES_pinned=des)
        P(f"  [{tag}] {ft}: pinned sigma8 {s8:.4f}: chi2 {main['chi2']:.2f}, p {main['p']:.2e} (would read {lab(main['p'])}); at 0.811: {eng['chi2']:.2f}, p {eng['p']:.3f}; "
          f"with a 0.06 eV neutrino ({s8n:.4f}): {nu['chi2']:.2f}, p {nu['p']:.3f}; KiDS best sigma8 {sb:.4f} +- {wid:.4f} (chi2 {best['chi2']:.2f}, p {best['p']:.3f}); "
          f"pinned is {(s8 - sb) / wid:+.2f} widths away (Delta chi2 {main['chi2'] - best['chi2']:+.2f}), neutrino bracket {(s8n - sb) / wid:+.2f};  DES pinned p {des['p']:.3f}   [{time.time() - T0:.0f} s]")
    return out
RES["rows"]["as_graded"] = rows_for("as graded (no correction)", PZ0)
for tag in ("R1", "R1b"):
    RES["rows"][tag] = rows_for(tag, {z: PZ0[z] / CORR[tag] for z in PZ0})
RES["rows"]["R2"] = rows_for("R2 (CFG411 L = 200 below k 0.5)", PZ_R2)
RES["rows"]["R2b"] = rows_for("R2b (CFG424 seed 360 L = 200 below k 0.5)", PZ_R2b)
setP(PZ0)
json.dump(RES, open(os.path.join(HERE, "co2_posthoc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "co2_posthoc.out"), "w").write("\n".join(OUT) + "\n")
