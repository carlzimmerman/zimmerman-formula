#!/usr/bin/env python3
"""OE1 reported cross-check, not in the label: BL1's route E halo inside R200; beyond it the cut at r_ta (baseline) against the 1e12 stack's own M(<r) to the sphere's edge (ZN1 ng 64, snapshot z 0.25). S2's forward model; BL1 read only. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HH_ = os.path.dirname(os.path.abspath(__file__)); BD = os.path.join(os.path.dirname(HH_), "BL1_blue_lens_halo_mass"); src = open(os.path.join(BD, "bl1_blue.py")).read(); cut = "for foot in FOOTS:\n    F = {}\n"; assert src.count(cut) == 1
__file__ = os.path.join(BD, "bl1_blue.py"); exec(compile(src[:src.index(cut)], "bl1_head", "exec"))
data_nat, gls, wmask, W = N["data_nat"], N["gls"], N["wmask"], N["W"]; ZS = json.load(open(os.path.join(REB, "ZN1_zooms_to_z0", "zn1_shapes.json"))); LX = np.log(np.array(ZS["x"])); LN = np.array(ZS["1e12"]["0.25"]["lnm"]); _h0 = halo
def halo(foot, Ms, Mc, Mb_tot, dlm, prof):
    if prof != "Z": return _h0(foot, Ms, Mc, Mb_tot, dlm, prof)
    Mh, q = _h0(foot, Ms, Mc, Mb_tot, dlm, "E"); x = RG / q["R200"]; M2 = q["M200"]; Mx = M2 * np.exp(np.interp(np.log(np.maximum(x, 1e-9)), LX, LN)) / float(np.exp(np.interp(0.0, LX, LN))); return np.where(x <= 1, Mh, Mx), q
RES = {}
for foot in FOOTS:
    RES[foot] = {}
    for k in ("blue", "all"):
        gb, go, C = data_nat(k, CFG["h"], CFG["pz"]); e = np.sqrt(np.diag(C)); Ci = np.linalg.inv(C); m = wmask(gb, W); Cw = np.linalg.inv(C[np.ix_(m, m)]); rr = {}
        for nm, mode, prof in (("E_cut_rta", "E", "E"), ("Z_particles", "E", "Z"), ("law", "law", "E")):
            STATE.update(mode=mode, prof=prof, dlm=0.0); g = model_g(foot, k, CFG); a = gls(go, C, g, m); rr[nm] = dict(A=a["A"], sA=a["sA"], chi2=float((go - g) @ Ci @ (go - g)), chi2_win=float((go - g)[m] @ Cw @ (go - g)[m]), ratio=(go / g).tolist())
            P(f"{foot} {k} {nm}: window A {a['A']:.3f} +- {a['sA']:.3f}; chi2 15 {rr[nm]['chi2']:.1f}; window chi2 {rr[nm]['chi2_win']:.1f}")
        RK = np.sqrt(4.30091e-6 * 10 ** 10.7 / (gb * 3.2408e-20 ** -1 * 0 + 1) * 0 + 1) if False else None; R_ = np.sqrt(6.674e-11 * 10 ** 10.7 * 1.989e30 / gb) / 3.0857e19; RES[foot][k] = dict(R_kpc_at_lgMs_10p7=R_.tolist(), window=m.tolist(), runs=rr); s = (R_ >= 150) & (R_ <= 300)
        P(f"  bins with R 150-300 kpc at lg M* 10.7 (indicative): R " + " ".join(f"{x:.0f}" for x in R_[s]))
        for nm in rr: P(f"    data/{nm} " + " ".join(f"{x:.2f}" for x, y in zip(rr[nm]['ratio'], s) if y))
json.dump(RES, open(os.path.join(HH_, "oe1_bl1.json"), "w"), default=float); open(os.path.join(HH_, "oe1_bl1.out"), "w").write("\n".join(map(str, OUT)) + "\n")
