#!/usr/bin/env python3
"""BL1 POST-RESULT, reported only: per-bin residuals for blue, red, all (law vs route E), and route E on S2's red stellar-mass ladder (R1 +0.123, R2 +0.123 + IMF 0.172).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
HERE_ = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE_, "bl1_blue.py")).read(); cut = "for foot in FOOTS:\n    F = {}\n"; assert src.count(cut) == 1
__file__ = os.path.join(HERE_, "bl1_blue.py"); exec(compile(src[:src.index(cut)], "bl1_head", "exec"))
data_nat, gls, wmask, W = N["data_nat"], N["gls"], N["wmask"], N["W"]
R = {}
def mg(foot, k, mode, cfg, prof="E", dlm=0.0):
    STATE.update(mode=mode, prof=prof, dlm=dlm); return model_g(foot, k, cfg)
for foot in FOOTS:
    R[foot] = {}
    for k in ("blue", "red", "all"):
        gb, go, C = data_nat(k, CFG["h"], CFG["pz"]); e = np.sqrt(np.diag(C)); gE = mg(foot, k, "E", CFG); gL = mg(foot, k, "law", CFG); gT = mg(foot, k, "E", CFG, "T")
        Ci = np.linalg.inv(C); c = lambda g: float((go - g) @ Ci @ (go - g)); m = wmask(gb, W)
        Cw = np.linalg.inv(C[np.ix_(m, m)]); cw = lambda g: float((go - g)[m] @ Cw @ (go - g)[m])
        R[foot][k] = dict(gb=gb.tolist(), go=go.tolist(), e=e.tolist(), route_E=gE.tolist(), route_T=gT.tolist(), law=gL.tolist(), chi2=dict(E=c(gE), T=c(gT), L=c(gL)), chi2_win=dict(E=cw(gE), T=cw(gT), L=cw(gL), n=int(m.sum())))
        P(f"\n[{foot} {k}] chi2 all 15: E {c(gE):.1f}, T {c(gT):.1f}, law {c(gL):.1f}; window ({int(m.sum())} pts, no amplitude): E {cw(gE):.1f}, T {cw(gT):.1f}, law {cw(gL):.1f}")
        if foot == "canonical":
            P("   lg g_bar  data/err     data/E  data/law  win")
            for i in range(15): P(f"   {np.log10(gb[i]):7.2f}  {go[i] / e[i]:7.1f}   {go[i] / gE[i]:7.2f} {go[i] / gL[i]:7.2f}   {'*' if m[i] else ''}")
    L = {}
    for nm, sh in (("R0", 0.0), ("R1 +0.123", 0.123), ("R2 +0.295", 0.295)):
        c_ = dict(CFG, red_shift=sh); STATE.update(mode="E", prof="E", dlm=0.0); a = cell(foot, "red", c_); al = cell(foot, "all", c_); STATE.update(mode="law"); b = cell(foot, "red", c_); bl = cell(foot, "all", c_)
        L[nm] = dict(E_red=dict(A=a["A"], s=a["sA"], cls=a["cls"], chi2=a["chi2_15_A1"]), E_all=dict(A=al["A"], s=al["sA"], cls=al["cls"], chi2=al["chi2_15_A1"]), law_red=dict(A=b["A"], s=b["sA"], cls=b["cls"], chi2=b["chi2_15_A1"]), law_all=dict(A=bl["A"], s=bl["sA"], cls=bl["cls"], chi2=bl["chi2_15_A1"]))
        P(f"  [{foot}] red ladder {nm}: route E red A {a['A']:.3f}+-{a['sA']:.3f} [{a['cls']}] chi2 {a['chi2_15_A1']:.1f}; all A {al['A']:.3f}+-{al['sA']:.3f} [{al['cls']}] chi2 {al['chi2_15_A1']:.1f} | law red A {b['A']:.3f}+-{b['sA']:.3f} [{b['cls']}] chi2 {b['chi2_15_A1']:.1f}; all A {bl['A']:.3f}+-{bl['sA']:.3f} [{bl['cls']}] chi2 {bl['chi2_15_A1']:.1f}")
    R[foot]["ladder"] = L
json.dump(R, open(os.path.join(HERE_, "bl1_posthoc.json"), "w"), indent=1, default=float); open(os.path.join(HERE_, "bl1_posthoc.out"), "w").write("\n".join(map(str, OUT)) + "\n")
