#!/usr/bin/env python3
"""SC2 AMENDMENT A1 (post-result, reported only): the rule against catalogue noise. Reads the frozen runs' JSON from this lane and A1's from the scratch root. Writes sc2_a1.out and sc2_a1.json.
    python3 sc2_a1_table.py <scratch_root>     kappa = 1/2 FITTED; footings never pooled."""
import json, math, os, sys
from collections import Counter
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); RT = sys.argv[1]; OUT = []
def Q(s=""): print(s); OUT.append(str(s))
def load(t): return json.load(open(os.path.join(H if t in ("old", "new", "k20") else RT, f"sc2_results_{t}.json")))
GR = dict(old_k=["old"] + [f"oldS{i}" for i in range(1, 6)], new_k=["new"] + [f"newS{i}" for i in range(1, 6)], old_20=["old20a", "old20b"], new_20=["k20", "new20b"]); RUN = {t: load(t) for g in GR.values() for t in g}
SHORT = {"NOT POWERED": "NP", "LAW PREFERRED": "LAW", "ROUTE E PREFERRED": "RE", "NEITHER": "N"}
Q("SC2 AMENDMENT A1, post-result, reported only. The frozen table stands. kappa = 1/2 FITTED; footings never pooled"); Q("Frozen counts: old rule 6 catalogues, new rule 6 (the frozen ones and 5 more seeds). 20 per lens: 2 per rule. NP = NOT POWERED, LAW = LAW PREFERRED, RE = ROUTE E PREFERRED, N = NEITHER")
bad = {t: [k for k in ("K3_only_I_changed", "K4_nulls_on_new_I") if not RUN[t]["checks"].get(k, True)] for t in RUN}; Q("K3 and K4 failures by catalogue: " + (str({t: v for t, v in bad.items() if v}) or "none") + ("" if any(bad.values()) else " none"))
Q("\nWeight per centre, lens/I, O2 (O1), per catalogue:")
WT = {}
for g, ts in GR.items():
    Q(f"  {g:6s} S3 " + ", ".join(f"{RUN[t]['weight_ratios']['S3_L_over_I']['O2']:.3f} ({RUN[t]['weight_ratios']['S3_L_over_I']['O1']:.3f})" for t in ts) + "; S1 " + ", ".join(f"{RUN[t]['weight_ratios']['S1_L_over_I']['O2']:.3f} ({RUN[t]['weight_ratios']['S1_L_over_I']['O1']:.3f})" for t in ts))
    WT[g] = {s: dict(O2=float(np.mean([RUN[t]['weight_ratios'][f'{s}_L_over_I']['O2'] for t in ts])), O1=float(np.mean([RUN[t]['weight_ratios'][f'{s}_L_over_I']['O1'] for t in ts])), inn=float(np.mean([RUN[t]['weight_ratios'][f'{s}_L_over_I']['in'] for t in ts]))) for s in ("S3", "S1")}
def stat(ts, foot, s, ln):
    x = []; dg = []; cl = []; pH = []; pL = []; Ds = []
    for t in ts:
        o = RUN[t]["si2"]["foot"][foot][s][ln]; d, sg, mL, mH = (np.array(o[k]) for k in ("d", "sig", "m_L", "m_H")); x.append(o["all"]["dchi2"]); dg.append(float(np.sum(((d - mH) / sg) ** 2 - ((d - mL) / sg) ** 2))); cl.append(SHORT[o["cls"]]); pH.append(o["all"]["pH"]); pL.append(o["all"]["pL"]); Ds.append(o["all"]["D"])
    return dict(x=x, m=float(np.mean(x)), s=float(np.std(x, ddof=1)), dg=dg, mg=float(np.mean(dg)), sg=float(np.std(dg, ddof=1)), cl=cl, tally=dict(Counter(cl)), pH=pH, pL=pL, D=float(np.mean(Ds)))
TAB = {}
for foot in ("canonical", "alt"):
    Q(f"\n=== [{foot}]")
    for s in ("S3", "S1"):
        for ln in ("all_R0", "blue_R0", "red_R0", "red_R2", "all_R2"):
            a, b, c, e = (stat(GR[g], foot, s, ln) for g in ("old_k", "new_k", "old_20", "new_20")); ef = b["m"] - a["m"]; se = math.sqrt(a["s"] ** 2 / 6 + b["s"] ** 2 / 6); ef2 = e["m"] - c["m"]; ed = b["mg"] - a["mg"]; sd = math.sqrt(a["sg"] ** 2 / 6 + b["sg"] ** 2 / 6)
            TAB[f"{foot}|{s}|{ln}"] = dict(old=a, new=b, old20=c, new20=e, rule_effect=ef, rule_effect_se=se, rule_effect_20=ef2, rule_effect_diag=ed, rule_effect_diag_se=sd)
            Q(f"  {s} {ln:7s} old {a['m']:+6.1f} sd {a['s']:4.1f} {str(a['tally']):32s} new {b['m']:+6.1f} sd {b['s']:4.1f} {str(b['tally']):32s} rule {ef:+5.1f} +- {se:3.1f} | diag {ed:+5.1f} +- {sd:3.1f} | 20 per lens: old {c['x'][0]:+6.1f}, {c['x'][1]:+6.1f} {c['cl']}; new {e['x'][0]:+6.1f}, {e['x'][1]:+6.1f} {e['cl']}; rule {ef2:+5.1f}")
Q("\nSI2's combined reading [canonical, all at R2], tally:"); CB = {}
for g, ts in GR.items():
    CB[g] = dict(Counter(RUN[t]["si2"]["combined"] for t in ts)); Q(f"  {g:6s} {CB[g]}")
    Q("         S1 route E p " + ", ".join(f"{RUN[t]['si2']['foot']['canonical']['S1']['all_R2']['all']['pH']:.3f}" for t in ts) + "; S3 route E p " + ", ".join(f"{RUN[t]['si2']['foot']['canonical']['S3']['all_R2']['all']['pH']:.3f}" for t in ts))
# reported: the same fits against Hotelling's T^2, which a 15-bin covariance from 36 patches actually follows, where the frozen classes use chi2(15)
from scipy import stats
def pt2(c, np_=36, p=15): return float(stats.f.sf(c / ((np_ - p - 2) / (np_ - 1)) * (np_ - p) / (p * (np_ - 1)), p, np_ - p))
Q("\nall at R2, canonical, route E and law p against T^2 (frozen classes use chi2(15), reported only):"); T2 = {}
for g, ts in GR.items():
    T2[g] = {s_: dict(H=[pt2(RUN[t]["si2"]["foot"]["canonical"][s_]["all_R2"]["all"]["chi2_H"]) for t in ts], L=[pt2(RUN[t]["si2"]["foot"]["canonical"][s_]["all_R2"]["all"]["chi2_L"]) for t in ts]) for s_ in ("S3", "S1")}
    Q(f"  {g:6s} " + "; ".join(f"{s_} route E " + ", ".join(f"{x:.3f}" for x in T2[g][s_]["H"]) + " law " + ", ".join(f"{x:.3f}" for x in T2[g][s_]["L"]) for s_ in ("S3", "S1")))
Q("\nP2's lane line, tally:"); P2 = {}
for g, ts in GR.items():
    P2[g] = dict(Counter(RUN[t]["P2"]["lane"] for t in ts)); Q(f"  {g:6s} {P2[g]}; canonical (a) A_O1 " + ", ".join(f"{RUN[t]['P2']['verdict']['canonical']['amps']['a']['A_O1']:.2f}" for t in ts) + "; A_O2 " + ", ".join(f"{RUN[t]['P2']['verdict']['canonical']['amps']['a']['A_O2']:.2f}" for t in ts))
cpu = {t: RUN[t]["cpu_s"] for t in RUN}; Q(f"\ngrade CPU over all catalogues: {sum(cpu.values()):.0f} s")
json.dump(dict(table=TAB, combined=CB, P2=P2, weights=WT, groups=GR, p_T2_all_R2=T2), open(os.path.join(H, "sc2_a1.json"), "w"), indent=1, default=float); open(os.path.join(H, "sc2_a1.out"), "w").write("\n".join(OUT) + "\n")
