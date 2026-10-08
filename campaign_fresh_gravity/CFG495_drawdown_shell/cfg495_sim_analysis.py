#!/usr/bin/env python3
"""CFG495 Step 1 analysis: drawdown depth, radial range and Delta Sigma difference from the cfg495_sim.py stacks (+ the analytic engine rule
at the same masses, cfg495_lenslib.group_q, to show how far the mesh resolves the drawdown).  Writes cfg495_sim_analysis.out / _results.json.
CFG495_MUTATE=1 -> the shuffled-centre stacks (outputs *_MUTATE.*): the drawdown must vanish."""
import os, sys, json, math
import numpy as np, warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg495_lenslib as LL
W = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg495_work"))
MUTATE = os.environ.get("CFG495_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
FB = LL.FB
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))
np.set_printoptions(linewidth=220, precision=3, suppress=True)
KEYS = ["N512_s360_can", "N512_s359_can", "N512_s359_alt", "N256_s359_can", "N256_s359_alt"] if not MUTATE else ["N512_s360_can", "N256_s359_can"]
MBINS = [(13.2, 13.4), (13.4, 13.7), (13.7, 14.2), (14.2, 16.0)]
rng = np.random.default_rng(4951)
OUT = {}
def boot(a, nb=300):
    n = len(a)
    if n < 3: return np.full(a.shape[1:], np.nan)
    i = rng.integers(0, n, (nb, n))
    return np.nanstd(np.nanmean(a[i], axis=1), axis=0)

for KEY in KEYS:
    p = os.path.join(W, f"cfg495_sim_{KEY}{TAG}.npz")
    if not os.path.exists(p):
        P(f"{KEY}: MISSING"); continue
    d = np.load(p); j = json.load(open(os.path.join(W, f"cfg495_sim_{KEY}{TAG}.json")))
    fn = j["fnames"]; ix = {n: i for i, n in enumerate(fn)}
    XB = np.array(j["XB"]); xc = 0.5 * (XB[1:] + XB[:-1]); YB = np.array(j["YB"]); yc = 0.5 * (YB[1:] + YB[:-1])
    PX, PY, DS, hM, hR, hre, qh, OWN = d["PX"], d["PY"], d["DS"], d["hM"], d["hR"], d["hre"], d["qh"], d["OWN"]
    lM = np.log10(hM)
    info = j.get("info", {})
    P(f"\n================ {KEY}{TAG}: {j['nH']} resolved hosts; dx {j['dx']:.3f} Mpc/h; catchment q mass-weighted {info.get('q_massweighted', float('nan')):.3f}, "
      f"max {info.get('q_max', float('nan')):.3f}; shell-only variant overdraw (q_sh > 1) {info.get('qsh_overdraw_mass', float('nan')):.3f} of catchment mass")
    R = {}
    for lo, hi in MBINS:
        m = (lM >= lo) & (lM < hi)
        if m.sum() < 5: continue
        # 3D: cold fractional depletion = comp / s_c = dc / ((1 - f_b)(1 + delta_TA)), ratio of stacked means
        cold = (1 - FB) * (1 + PX[m, ix["dTA"]])
        dep = np.nanmean(PX[m, ix["dc"]], 0) / np.maximum(np.nanmean(cold, 0), 1e-9)
        dep_sh = np.nanmean(PX[m, ix["dcsh"]], 0) / np.maximum(np.nanmean(cold, 0), 1e-9)
        xe = np.median(hre[m] / hR[m])
        shell = (xc > xe) & (xc < 1.0)
        wv = np.nanmean(cold, 0) * xc ** 2
        def wavg(v, sel):
            k = sel & np.isfinite(v) & np.isfinite(wv)
            return float(np.average(v[k], weights=wv[k])) if k.any() else float("nan")
        depth = wavg(dep, shell); depth_sh = wavg(dep_sh, shell)
        out_ = (xc > 1.0) & (xc < 2.0)
        depth_out = wavg(dep, out_)
        # effective density difference vs the matched S0 control (3D): TA particles + e - comp - S0
        eff = PX[m, ix["dTA"]] + PX[m, ix["de"]] - PX[m, ix["dc"]] - PX[m, ix["dS0"]]
        eff_m = np.nanmean(eff, 0); eff_s = boot(eff)
        dS0 = np.nanmean(PX[m, ix["dS0"]], 0)
        # projected
        DSS0 = np.nanmean(DS[m, ix["dS0"]], 0)
        dd = -DS[m, ix["dc"]]; dd_m = np.nanmean(dd, 0); dd_s = boot(dd)
        ddsh = -DS[m, ix["dcsh"]]; ddsh_m = np.nanmean(ddsh, 0)
        tot = DS[m, ix["dTA"]] + DS[m, ix["de"]] - DS[m, ix["dc"]] - DS[m, ix["dS0"]]; tot_m = np.nanmean(tot, 0); tot_s = boot(tot)
        part = DS[m, ix["dTA"]] - DS[m, ix["dS0"]]; part_m = np.nanmean(part, 0); part_s = boot(part)
        nod = DS[m, ix["dTA"]] + DS[m, ix["de"]] - DS[m, ix["dS0"]]; nod_m = np.nanmean(nod, 0)
        sel = (xc > 0.3) & (xc < 1.0)
        amp = float(np.nanmean(dd_m[sel] / DSS0[sel]))
        # analytic engine rule at the bin's median mass (f_ret = 1, z = 0), both footings for reference
        Mmed = 10 ** np.median(lM[m]) / LL.H
        qa, xa, _ = LL.group_q(Mmed, 0.0, j["foot"])
        row = dict(n=int(m.sum()), lM_med=float(np.median(lM[m])), x_edge_med=float(xe), q_halo_med=float(np.median(qh[m])),
                   depth_shell=depth, depth_shell_outer_only_variant=depth_sh, depth_1to2_rta=depth_out, depletion_profile=dep.tolist(),
                   eff3d_minus_S0=eff_m.tolist(), eff3d_sig=eff_s.tolist(), dS0_3d=dS0.tolist(),
                   DS_S0=DSS0.tolist(), DS_drawdown=dd_m.tolist(), DS_drawdown_sig=dd_s.tolist(), DS_drawdown_shell_variant=ddsh_m.tolist(),
                   DS_total_minus_S0=tot_m.tolist(), DS_total_sig=tot_s.tolist(), DS_particles_minus_S0=part_m.tolist(), DS_particles_sig=part_s.tolist(),
                   DS_nodrawdown_minus_S0=nod_m.tolist(), drawdown_frac_0p3_1=amp, q_analytic=qa, x_edge_analytic=xa)
        if "dNC" in ix:
            row["DS_NOCOMPrun_particles_minus_S0"] = np.nanmean(DS[m, ix["dNC"]] - DS[m, ix["dS0"]], 0).tolist()
            row["DS_TA_minus_NOCOMPrun_particles"] = np.nanmean(DS[m, ix["dTA"]] - DS[m, ix["dNC"]], 0).tolist()
        R[f"{lo}-{hi}"] = row
        neg = np.where(eff_m < -2 * eff_s)[0]
        P(f"  log M_ta [{lo},{hi}) n {m.sum():4d} (median {row['lM_med']:.2f}); x_edge {xe:.3f} (analytic {xa:.3f}); q per host median {row['q_halo_med']:.3f}; "
          f"analytic engine rule q {qa:.3f}")
        P(f"     cold depletion depth in the shell r_edge..r_ta: {depth:.3f} (outer-shell-only variant {depth_sh:.3f}); at 1-2 r_ta (neighbour catchments) {depth_out:.3f}")
        P(f"     depletion profile vs r/r_ta {np.round(xc[::3], 2)}: {np.round(dep[::3], 3)}")
        P(f"     3D effective density TA(+e-comp) - S0 [units of mean]: {np.round(eff_m[::3], 3)} +- {np.round(eff_s[::3], 3)}; "
          f"bins below -2 sigma at r/r_ta = {np.round(xc[neg], 2).tolist()}")
        P(f"     Delta Sigma [h Msun/pc^2] vs R/r_ta {np.round(xc[1::3], 2)}")
        P(f"       S0 control          : {np.round(DSS0[1::3], 3)}")
        P(f"       drawdown (-comp)    : {np.round(dd_m[1::3], 3)} +- {np.round(dd_s[1::3], 3)}   (mean fraction of S0 over 0.3-1 r_ta: {amp:+.3f})")
        P(f"       shell-only variant  : {np.round(ddsh_m[1::3], 3)}")
        P(f"       TA total - S0       : {np.round(tot_m[1::3], 3)} +- {np.round(tot_s[1::3], 3)}")
        P(f"       no-drawdown - S0    : {np.round(nod_m[1::3], 3)}")
        P(f"       particles TA - S0   : {np.round(part_m[1::3], 3)} +- {np.round(part_s[1::3], 3)}")
        if "dNC" in ix:
            P(f"       particles TA - NOCOMP run: {np.round(np.array(row['DS_TA_minus_NOCOMPrun_particles'])[1::3], 3)}")
    OUT[KEY] = dict(info=info, xc=xc.tolist(), bins=R)

if MUTATE:
    ref = json.load(open(os.path.join(HERE, "cfg495_sim_analysis_results.json")))
    P("\n== MUTATE (shuffled centres): drawdown amplitude over 0.3-1 r_ta, random / halo-centred")
    ok_all = True
    for KEY in OUT:
        for b, row in OUT[KEY]["bins"].items():
            c = ref[KEY]["bins"].get(b)
            if c is None: continue
            xc = np.array(OUT[KEY]["xc"]); sel = (xc > 0.3) & (xc < 1.0)
            a_r = float(np.nanmean(np.array(row["DS_drawdown"], float)[sel])); a_c = float(np.nanmean(np.array(c["DS_drawdown"], float)[sel]))
            ratio = a_r / a_c if a_c != 0 else float("nan"); ok = abs(ratio) < 0.1
            ok_all &= ok
            P(f"  {KEY} {b}: centred {a_c:+.4f}, shuffled {a_r:+.4f} h Msun/pc^2 -> ratio {ratio:+.3f} {'(killed)' if ok else '(NOT killed)'}")
    OUT["mutate_killed"] = bool(ok_all)
    P(f"MUTATE: shuffled centres kill the drawdown signal (|ratio| < 0.1 in every bin): {'PASS' if ok_all else 'FAIL'}")
json.dump(OUT, open(os.path.join(HERE, f"cfg495_sim_analysis{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg495_sim_analysis{TAG}.out"), "w").write("\n".join(LOG) + "\n")
