#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG167 POST-COMPARISON diagnostics (written AFTER CFG161's script/out/json were opened; NOT part of any frozen result).
1. exact per-row comparison with CFG161's committed json; 2. KROSS-selection systematic; 3. joint gas profile at pinned KROSS gas values.
ZF_REPO=<repo> python3 CFG167_diag_post.py > CFG167_diag_post.out (rc 0)"""
import os, sys, json, math, copy
sys.dont_write_bytecode = True
import numpy as np
import CFG167_referee_diff_p4 as D67
M = D67.M
P = lambda *a: print(*a, flush=True)
SK, SR, AS = D67.load_all("inc_star_deg")
P4 = D67.P4
R = D67.rows(SK, SR)
j = json.load(open(os.path.join(D67.REPO, "campaign_fresh_gravity", "CFG161_kross_differential_p4_results.json")))["numbers"]
P("repo=<repo>\n== 1. per-row comparison with CFG161's committed json (D, sigma_D, D_H; exact differences)")
mp = {"P0": ("R1", "P0 (none)"), "P1": ("R1", "P1 (sigma0 on KURVS)"), "P2": ("R1", "P2 (sigma_out on KURVS)"), "P3": ("R1", "P3 (fixed height)"), "P4": ("R1", "P4 (Kretschmer, primary)"),
      "P4 a0.6": ("R2", "P4 alpha x 0.6"), "P4 a1.4": ("R2", "P4 alpha x 1.4"), "P4 KU s0": ("R2", "P4, KURVS sigma0")}
mx = 0
for k, (sec, nm) in mp.items():
    t = j[sec][nm]
    dd = (R[k]["D"] - t["D"], R[k]["sD"] - t["sigma_D"], R[k]["DH"] - t["D_H"])
    mx = max(mx, max(abs(v) for v in dd))
    P(f"   {k:9s}: dD {dd[0]:+.2e}  dsigma {dd[1]:+.2e}  dD_H {dd[2]:+.2e}")
o = j["P4"]["own"]
c = R["P4"]
P(f"   KURVS/KROSS raw pooled P4: dKf {c['kf']-o['KURVS_flat']:+.2e} dKh {c['kh']-o['KURVS_H']:+.2e} dRf {c['rf']-o['KROSS_flat']:+.2e} dRh {c['rh']-o['KROSS_H']:+.2e}  errors dK {c['ke']-o['eKURVS']:+.2e} dR {c['re']-o['eKROSS']:+.2e}")
P(f"   max |difference| over the eight rows: {mx:.2e}")
P("   (my run and CFG161's use different code paths for the pooling and the KROSS loader; agreement at this level is the check)")

P("\n== 2. KROSS-selection systematic (EXTRA, not frozen): spread of the KROSS mean Delta_flat across the deterministic (c) variants")
kd, ke = c["rpo"]["d_flat"], c["rpo"]["e_flat"]
rows_ = {r["name"]: r for r in M.read_csv("data_assembly/high_z_tf_tables/kross_v2.csv")}
kin = np.array([rows_[n]["kin_type"] for n in SR.name])
vs = SR.V / SR.sig0
ba = np.cos(SR.inc)
masks = {"RT": kin == "RT", "RT+": kin == "RT+", "v/s>=2": vs >= 2, "v/s>=3": vs >= 3, "b/a>0.5": ba > 0.5, "logM<med": SR.logM < np.median(SR.logM), "logM>=med": SR.logM >= np.median(SR.logM),
         "z<0.85": SR.z < 0.85, "z>=0.85": SR.z >= 0.85}
vals = {}
for nm, mk in masks.items():
    m, e, _ = M.pool(kd[mk], ke[mk])
    vals[nm] = (m, e)
    P(f"   {nm:10s} n={mk.sum():3d}  KROSS Delta_flat {m:+.3f} +- {e:.3f}")
mm = np.array([v[0] for v in vals.values()])
P(f"   all: {c['rf']:+.3f} +- {c['re']:.3f};  sd of the sub-sample means {mm.std():.3f}; range {mm.min():+.3f}..{mm.max():+.3f}")
a, b = vals["RT"], vals["RT+"]
P(f"   RT minus RT+ : {a[0]-b[0]:+.3f} +- {math.hypot(a[1], b[1]):.3f} ({(a[0]-b[0])/math.hypot(a[1], b[1]):+.1f} sigma of the pooled statistical error)")
a, b = vals["v/s>=3"], vals["b/a>0.5"]
sys_sel = float(mm.std())
tot = math.hypot(c["sD"], sys_sel)
P(f"   selection-systematic sd {sys_sel:.3f} added in quadrature to sigma_D: total {tot:.3f}; z_flat {c['D']/tot:+.2f}; z_rival {(c['D']-c['DH'])/tot:+.2f}")
res_ = {"sys_sel": sys_sel, "tot": tot, "z_flat": c["D"] / tot, "z_riv": (c["D"] - c["DH"]) / tot}

P("\n== 3. joint gas profile at pinned KROSS gas (EXTRA, not frozen): each law's best KURVS gas, anchored joint chi2 with covariance")
ap = M.anchor_pool(P4, 0.0, D67.FOOT, AS)["flat"]
AP, AE = ap[0], ap[1]
muk = np.exp(np.linspace(math.log(0.1), math.log(12), 80))
KP = {m_: D67.pooled(SK, P4, m_) for m_ in muk}
for mr in (0.10, 0.17, 0.25, 0.27, 0.46, 0.67, 1.5, 4.0):
    rr = D67.pooled(SR, P4, mr)
    line = f"   mu_R = {mr:4.2f}:"
    for law in ("f", "h"):
        best = (1e9, None)
        for mk in muk:
            if mk < mr:
                continue
            kk = KP[mk]
            v = np.array([kk[law] - AP, rr[law] - AP])
            C = np.diag([kk["fe"] ** 2, rr["fe"] ** 2]) + AE ** 2
            c2 = float(v @ np.linalg.solve(C, v))
            if c2 < best[0]:
                best = (c2, mk, v)
        line += f"  {'flat' if law=='f' else 'rival'}: chi2 {best[0]:6.2f} at mu_K = {best[1]:.2f} (Dprime_R {best[2][1]:+.3f})"
    P(line)
P("   (mu_R = 0.27 with 16-84% 0.17-0.46 is the Sharma+2024 molecular median quoted in CFG165's README; total mu about 4.0 there; not re-derived here)")
json.dump(res_, open(os.path.join(D67.HERE, "CFG167_diag_post_results.json"), "w"), indent=1)
P("exit 0")
