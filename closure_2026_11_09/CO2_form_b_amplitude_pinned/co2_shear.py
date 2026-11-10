#!/usr/bin/env python3
"""CO2 (FROZEN_CRITERIA.md 2bd776c60d, AMENDMENT_A1 b6dd6d0641) part 3: row P4, raw KiDS-1000 at the pinned amplitude.
CFG592's native machinery, library part executed UNCHANGED, on CFG596's S0 run (the same 104 points as CO1's C5).
Model: S0 x R_tot (form B's layout, CO1's co1_hm.json) moved from the engine's sigma8 0.811 to the pinned fit's sigma8.
  primary  the run's own response: alpha(k) = d ln P / d ln D^2 between neighbouring snapshots (node z 0: 0.2562 -> 0;
           node 0.5: 0.7548 -> 0.2562; node 1: 1 -> 0.7548), running median over five k bins, clipped to [1, 3];
           P'(k, node) = P(k, node) x f^alpha(k), f = (sigma8 / 0.811)^2.
  bracket  the constant factor f (alpha = 1).
Lines on p (chi2_data survival at N, as CFG596 prints it): >= 0.05 CONSISTENT; >= 0.0027 TENSION; else EXCLUDED AT 3 SIGMA.

  nice -n 10 python3 co2_shear.py     -> co2_shear.json, co2_shear.out      (after co2_rows.py)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list in R (CO1's criteria)."""
import os, sys, json, math, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
from scipy.stats import chi2 as CH
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
Pmat, fit, support_mask, subset, SURV = (G[k] for k in ("Pmat", "fit", "support_mask", "subset", "SURV"))
FOOTS = ("canonical", "alt"); S8E = 0.811
HM = json.load(open(os.path.join(HERE, "..", "CO1_form_b_cosmology_computed", "co1_hm.json"))); KH = np.array(HM["k"])
CO1S = json.load(open(os.path.join(HERE, "..", "CO1_form_b_cosmology_computed", "co1_shear.json")))
ROWS = json.load(open(os.path.join(HERE, "co2_rows.json")))
S0J = json.load(open(glob.glob(os.path.join(G["EXT"], "cfg596_work", "P0", "cfg596_*.json"))[0])); SN = S0J["snap"]
K = np.array(SN["z0"]["k"]); NP_, LBOX = int(S0J["np"]), float(S0J["L"])
PZ = {0.0: np.array(SN["z0"]["P"]), 0.5: np.array(SN["z0.5"]["P"]), 1.0: np.array(SN["z1"]["P"])}
BASE = dict(N=NP_, L=LBOX, k=K, k_lo=float(K[0]), k_hi=float(math.pi * NP_ / (4 * LBOX)))
def a_raw(early, late): return np.log(np.array(SN[late]["P"]) / np.array(SN[early]["P"])) / (2 * math.log(SN[late]["D"] / SN[early]["D"]))
ARAW = {0.0: a_raw("x0.2562", "z0"), 0.5: a_raw("x0.7548", "x0.2562"), 1.0: a_raw("z1", "x0.7548")}
def runmed5(a):
    n = len(a); return np.array([np.median(a[max(0, i - 2):min(n, i + 3)]) for i in range(n)])
ALPHA = {z: np.clip(runmed5(a), 1.0, 3.0) for z, a in ARAW.items()}
def onk(R): return np.interp(np.log(np.clip(K, KH[0], KH[-1])), np.log(KH), np.asarray(R, float))
def run_of(R, f=1.0, mode="resp"):
    nodes = {z: ((PZ[z] * (f ** ALPHA[z] if mode == "resp" else f),) * 2) for z in PZ}
    return dict(BASE, name="x", foot="-", B=onk(R), nodes=nodes)
ONE = np.ones_like(KH)
RUN1 = run_of(ONE); PS0 = Pmat(RUN1, "S0")
DS = {}
for sn, S in SURV.items():
    fm = support_mask(S, RUN1, PS0); DS[sn] = subset(S, S["pubkeep"] & (fm >= 0.9))
def fitp(sn, R, s8, mode="resp"):
    f = (s8 / S8E) ** 2; r = fit(SURV[sn], DS[sn], Pmat(run_of(R, f, mode), "F"))
    return dict(sigma8=s8, factor=f, chi2=r["chi2"], chi2_data=r["chi2_data"], p=float(CH.sf(r["chi2_data"], DS[sn]["N"])), A_IA=r["A_IA"])
def lab(p): return "CONSISTENT" if p >= 0.05 else ("TENSION" if p >= 0.0027 else "EXCLUDED AT 3 SIGMA")
RES = dict(lane="CO2", part="P4 raw KiDS-1000 at the pinned amplitude", criteria="2bd776c60d", amendment_A1="b6dd6d0641", S0=S0J["tag"], N=DS["KiDS"]["N"],
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0; inherited halo list in R", KA={}, alpha={}, P4={}, brackets={}, scan={}, DES_reported={}, MUTATE={})
P(f"CO2 part 3: raw KiDS-1000 at the pinned amplitude. S0 run {S0J['tag']}; {DS['KiDS']['N']} KiDS points, {DS['DES']['N']} DES points.")

# ------------------------------------------------------------------ the response and KA5
KSEL = (0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0); ka5 = {}
for z in (0.0, 0.5, 1.0):
    m = K < 0.12; med = float(np.median(ARAW[z][m])) if m.any() else float("nan")
    ka5[str(z)] = dict(n_bins=int(m.sum()), median_alpha=med, pass_=bool(m.any() and abs(med - 1) <= 0.15))
    RES["alpha"][str(z)] = dict(at={str(kk): float(np.interp(kk, K, ALPHA[z])) for kk in KSEL}, raw_at={str(kk): float(np.interp(kk, K, ARAW[z])) for kk in KSEL},
                                clipped_low=int(np.sum(runmed5(ARAW[z])[K <= BASE["k_hi"]] < 1.0)), clipped_high=int(np.sum(runmed5(ARAW[z])[K <= BASE["k_hi"]] > 3.0)))
    P(f"response alpha(k) at node z {z}: " + ", ".join(f"k {kk:g}: {np.interp(kk, K, ALPHA[z]):.2f}" for kk in KSEL) + f"; raw median below k 0.12 ({int(m.sum())} bins) {med:.3f}; "
      f"bins clipped up to 1: {RES['alpha'][str(z)]['clipped_low']}, down to 3: {RES['alpha'][str(z)]['clipped_high']}")
RES["KA"]["KA5"] = ka5
_m = K <= BASE["k_hi"]; _d = float(np.max(np.abs(ALPHA[0.0][_m] - ALPHA[0.5][_m]))); RES["alpha"]["max_abs_node0_minus_node0.5"] = _d
P(f"reported: the response changes between nodes 0 and 0.5 by at most {_d:.2f} over the run's k range (the move at node 0 extrapolates the last interval)")
P(f"KA5 the response is 1 on linear scales (within 0.15): {'PASS' if all(v['pass_'] for v in ka5.values()) else 'FAIL'}")

for ft in FOOTS:
    pri = HM["primary"][ft]; Rt, Rb = pri["R_tot"], pri["R_bar"]; s8 = ROWS["P2"][ft]["sigma8"]; s8u = ROWS["P2"][ft]["CO1_unpinned"]["sigma8"]
    # KA4
    k_a = fitp("KiDS", Rt, s8u, "const"); k_b = fitp("KiDS", Rt, S8E, "resp"); k_c = fitp("KiDS", Rt, S8E, "const")
    ref_a = CO1S["brackets"][ft]["amplitude_sigma8_of_C3"]["chi2_tot"]; ref_b = CO1S["C5"][ft]["chi2_tot"]
    ka4 = dict(const_at_CO1_sigma8=k_a["chi2"], ref=ref_a, f1_resp=k_b["chi2"], f1_const=k_c["chi2"], ref_f1=ref_b,
               pass_=bool(abs(k_a["chi2"] - ref_a) <= 0.01 and abs(k_b["chi2"] - ref_b) <= 0.01 and abs(k_c["chi2"] - ref_b) <= 0.01))
    RES["KA"].setdefault("KA4", {})[ft] = ka4
    P(f"\n[{ft}] KA4: constant factor at CO1's sigma8 {s8u:.4f}: chi2 {k_a['chi2']:.2f} (CO1 {ref_a:.2f}); f = 1: {k_b['chi2']:.2f} / {k_c['chi2']:.2f} (CO1 {ref_b:.2f}) -> {'PASS' if ka4['pass_'] else 'FAIL'}")
    main = fitp("KiDS", Rt, s8); cst = fitp("KiDS", Rt, s8, "const"); s0 = fitp("KiDS", ONE, s8); bar = fitp("KiDS", Rb, s8)
    RES["P4"][ft] = dict(**main, label=lab(main["p"]), constant_factor=cst, S0_alone=s0, S0_x_R_bar=bar)
    P(f"  P4 raw KiDS at the pinned sigma8 {s8:.4f} (factor {main['factor']:.4f}), S0 x R_tot, the run's own response: chi2 {main['chi2']:.2f}, p {main['p']:.2e} -> {lab(main['p'])}")
    P(f"     constant factor (bracket): chi2 {cst['chi2']:.2f}, p {cst['p']:.2e} ({lab(cst['p'])});  S0 alone {s0['chi2']:.2f} (p {s0['p']:.2e});  S0 x R_bar {bar['chi2']:.2f} (p {bar['p']:.2e});  A_IA {main['A_IA']:.2f}")
    s8n = ROWS["brackets"][ft]["one_0p06eV_neutrino"]["sigma8"]
    br = dict(one_0p06eV_neutrino=fitp("KiDS", Rt, s8n), prefactor_0_layout=fitp("KiDS", HM["brackets"][ft]["pre_0"]["R_tot"], s8),
              unpinned_sigma8_response=fitp("KiDS", Rt, s8u), unpinned_sigma8_constant=k_a, engine_sigma8=k_b)
    RES["brackets"][ft] = br
    P("     brackets: " + "; ".join(f"{n} (sigma8 {v['sigma8']:.4f}) chi2 {v['chi2']:.2f}, p {v['p']:.2e}" for n, v in br.items()))
    # scan in sigma8 (response scaling)
    grid = np.arange(0.70, 0.9001, 0.0125); sc = [fitp("KiDS", Rt, float(s)) for s in grid]; c2 = np.array([v["chi2"] for v in sc]); i = int(np.argmin(c2))
    lo_, hi_ = max(i - 2, 0), min(i + 3, len(grid)); co = np.polyfit(grid[lo_:hi_], c2[lo_:hi_], 2); sb = -co[1] / (2 * co[0]); cmin = float(np.polyval(co, sb)); wid = 1 / math.sqrt(co[0])
    best = fitp("KiDS", Rt, float(sb))
    RES["scan"][ft] = dict(sigma8=grid.tolist(), chi2=c2.tolist(), p=[v["p"] for v in sc], best_sigma8=float(sb), width_dchi2_1=wid, chi2_min_parabola=cmin, best_fit=best,
                           pinned_minus_best_in_widths=(s8 - sb) / wid, dchi2_pinned_vs_best=main["chi2"] - best["chi2"])
    m2 = sc[-1]; RES["MUTATE"].setdefault("M2", {})[ft] = dict(sigma8=float(grid[-1]), chi2=m2["chi2"], p=m2["p"], bites=bool(abs(grid[-1] - 0.90) < 1e-9 and m2["p"] < 0.0027))
    RES["MUTATE"].setdefault("M3", {})[ft] = dict(chi2_response=main["chi2"], chi2_constant=cst["chi2"], applies=bool(s8 > S8E), bites=bool(s8 <= S8E or main["chi2"] > cst["chi2"]))
    P(f"     scan: raw KiDS is best at sigma8 {sb:.4f} +- {wid:.4f} for form B's spectrum (chi2 {best['chi2']:.2f}, p {best['p']:.3f}); the pinned value sits {(s8 - sb) / wid:+.2f} widths away "
      f"(Delta chi2 {main['chi2'] - best['chi2']:+.2f})")
    P(f"     M2 sigma8 0.90: chi2 {m2['chi2']:.2f}, p {m2['p']:.1e} -> {'bites' if RES['MUTATE']['M2'][ft]['bites'] else 'DOES NOT BITE'};  M3 response against constant: "
      f"{main['chi2']:.2f} against {cst['chi2']:.2f} -> {'bites' if RES['MUTATE']['M3'][ft]['bites'] else 'DOES NOT BITE'}")
    d = fitp("DES", Rt, s8); d0 = fitp("DES", Rt, S8E); RES["DES_reported"][ft] = dict(pinned=d, engine=d0)
    P(f"     DES Y3 (reported; {DS['DES']['N']} points): pinned chi2 {d['chi2']:.2f}, p {d['p']:.3f}; at 0.811 {d0['chi2']:.2f}, p {d0['p']:.3f}   [{time.time() - T0:.0f} s]")
RES["KA_ok"] = bool(all(v["pass_"] for v in ka5.values()) and all(v["pass_"] for v in RES["KA"]["KA4"].values()))
P(f"\nKnown answers of this part all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "co2_shear.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "co2_shear.out"), "w").write("\n".join(OUT) + "\n")
