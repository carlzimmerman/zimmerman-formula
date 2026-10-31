#!/usr/bin/env python3
"""SC2_clone_rule_on_spec_lenses (criteria a664f7af34): old against new, from the runs' JSON. Writes sc2_classes.out and sc2_classes.json.
    python3 sc2_table.py     kappa = 1/2 FITTED; footings never pooled."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); RUN = {t: json.load(open(os.path.join(H, f"sc2_results_{t}.json"))) for t in ("old", "new", "k20")}; OUT = []
def Q(s=""): print(s); OUT.append(str(s))
def fp(p): return f"{p:.3f}" if p >= 0.001 else f"{p:.0e}"
LINES = (("all_R0", "all, R0 (SI1's grade)"), ("blue_R0", "blue, R0"), ("red_R0", "red, R0"), ("red_R2", "red, R2"), ("all_R2", "ALL, R2"), ("all_R2_raw", "all, R2, raw L-R (reported)"))
Q("SC2 old against new. Same counts: S3 4 per lens, S1 2 per lens. k20: 20 per lens, reported. dchi2 = chi2(route E) - chi2(law). kappa = 1/2 FITTED; footings never pooled")
Q("\nchecks: " + "; ".join(f"{t}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in RUN[t]["checks"].items()) for t in RUN))
Q("\nWeight per centre, K_H3-style, in / O1 / O2; clones' mean z and lg M* against the lenses'")
WR = {}
for t in RUN:
    W = RUN[t]["weight_ratios"]; SK = RUN[t]["skew"]; WR[t] = {k: {r: W[k][r] for r in ("in", "O1", "O2")} for k in W}
    for s in ("S3", "S1"):
        Q(f"  {t:4s} {s}: lens/I {W[s + '_L_over_I']['in']:.3f} / {W[s + '_L_over_I']['O1']:.3f} / {W[s + '_L_over_I']['O2']:.3f};  lens/R {W[s + '_L_over_R']['in']:.3f} / {W[s + '_L_over_R']['O1']:.3f} / {W[s + '_L_over_R']['O2']:.3f};  mean z lens {SK[s]['lens_z']:.4f}, clones {SK[s]['clone_z']:.4f};  mean lg M* lens {SK[s]['lens_lM']:.4f}, clones {SK[s]['clone_lM']:.4f}")
TAB = {}; CHG = []; CHG20 = []
for foot in ("canonical", "alt"):
    Q(f"\n=== [{foot}]")
    for s in ("S3", "S1"):
        Q(f"  {s}")
        for ln, name in LINES:
            r = {t: RUN[t]["si2"]["foot"][foot][s][ln] for t in RUN}; c = {t: r[t]["all"] for t in RUN}; TAB[f"{foot}|{s}|{ln}"] = {t: dict(chi2_L=c[t]["chi2_L"], pL=c[t]["pL"], chi2_H=c[t]["chi2_H"], pH=c[t]["pH"], dchi2=c[t]["dchi2"], D=c[t]["D"], cls=r[t]["cls"], inner=r[t]["inner"]["dchi2"], outer=r[t]["outer"]["dchi2"]) for t in RUN}
            ch = r["old"]["cls"] != r["new"]["cls"]; ch20 = r["old"]["cls"] != r["k20"]["cls"]
            if ln != "all_R2_raw" and ch: CHG.append((foot, s, ln, r["old"]["cls"], r["new"]["cls"], r["k20"]["cls"]))
            if ln != "all_R2_raw" and ch20: CHG20.append((foot, s, ln, r["old"]["cls"], r["k20"]["cls"]))
            Q(f"    {name:28s} old L {c['old']['chi2_L']:6.1f} (p {fp(c['old']['pL'])}) H {c['old']['chi2_H']:6.1f} (p {fp(c['old']['pH'])}) dchi2 {c['old']['dchi2']:+6.1f} D {c['old']['D']:.2f} {r['old']['cls']:18s} | new L {c['new']['chi2_L']:6.1f} (p {fp(c['new']['pL'])}) H {c['new']['chi2_H']:6.1f} (p {fp(c['new']['pH'])}) dchi2 {c['new']['dchi2']:+6.1f} D {c['new']['D']:.2f} {r['new']['cls']:18s}{' CHANGED' if ch else ''} | k20 dchi2 {c['k20']['dchi2']:+6.1f} D {c['k20']['D']:.2f} {r['k20']['cls']}")
Q("\nSI2's combined reading [canonical, all at R2]: " + "; ".join(f"{t}: {RUN[t]['si2']['combined']}" for t in RUN))
Q("P2's lane line: " + "; ".join(f"{t}: {RUN[t]['P2']['lane']}" for t in RUN))
for foot in ("canonical", "alt"):
    for t in RUN:
        v = RUN[t]["P2"]["verdict"][foot]; a, b = v["amps"]["a"], v["amps"]["b"]; Q(f"  P2 [{foot}] {t:4s}: {v['verdict']}; S {v['Smax']:.2f}; (a) A_in {a['A_in']:.2f}+-{a['sA_in']:.2f} A_O1 {a['A_O1']:.2f}+-{a['sA_O1']:.2f} A_O2 {a['A_O2']:.2f}+-{a['sA_O2']:.2f} {v['cls_a']}; (b) A_O1 {b['A_O1']:.2f}+-{b['sA_O1']:.2f} A_O2 {b['A_O2']:.2f}+-{b['sA_O2']:.2f} {v['cls_b']}")
Q("\nI's own noise in dchi2 (half A, half B, sigma of I), all lenses:")
for t in RUN:
    for k, v in RUN[t]["noise"].items(): Q(f"  {t:4s} {k:22s} dchi2 {v['dchi2']:+7.1f}; halves {v['half_A']:+7.1f}, {v['half_B']:+7.1f}; sigma(I) {v['sig_I']:.1f}")
Q(f"\nCLASSES CHANGED, old to new at the same counts ({len(CHG)}): {CHG}"); Q(f"classes that differ from old on k20 ({len(CHG20)}): {CHG20}")
Q("CPU, s: " + ", ".join(f"{t} {RUN[t]['cpu_s']:.0f}" for t in RUN))
json.dump(dict(table=TAB, changed=CHG, changed_k20=CHG20, combined={t: RUN[t]["si2"]["combined"] for t in RUN}, P2={t: RUN[t]["P2"]["lane"] for t in RUN}, weight_ratios=WR), open(os.path.join(H, "sc2_classes.json"), "w"), indent=1, default=float)
open(os.path.join(H, "sc2_classes.out"), "w").write("\n".join(OUT) + "\n")
