#!/usr/bin/env python3
"""SI2 POST-RESULT, reported only: how the frozen line 3 (all lenses, both samples) moves with the red stellar-mass shift. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
HEREX = os.path.dirname(os.path.abspath(__file__)); srcx = open(os.path.join(HEREX, "si2_grade.py")).read(); cutx = 'J1 = None if MUT2 else'; assert srcx.count(cutx) == 1
__file__ = os.path.join(HEREX, "si2_grade.py"); exec(compile(srcx[:srcx.index(cutx)], "si2_head", "exec")); HERE2 = HEREX
R = {}
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, _ = build(foot); R[foot] = {}
    for s in (0.0, 0.1, 0.123, 0.2, 0.295, 0.4):
        shg = np.where(red_g, s, 0.0); lb = np.log10(10 ** lMb_g + 10 ** lMs_g * (10 ** shg - 1)); N["tix"] = np.clip(np.round((lb - LMB_T[0]) / 0.05).astype(int), 0, len(LMB_T) - 1); N["MBN_g"] = 10 ** lb
        TOWN[(foot, "red")] = law_table(foot, s); TOWN[(key, "red")] = town_H(foot, dMs=s); tH = tnbr(key, node=0); tL = tnbr(foot, node=0); mL, mH = modl(foot, tL, "R2"), modl(key, tH, "R2")
        for sm in ("S3", "S1"):
            sL, sH = st(mL, sm, "all"), st(mH, sm, "all"); c = compare(sL, sH); r = compare(sL, sH, RANGE["in"]); o = compare(sL, sH, RANGE["out"]); aL, aH = amps(sL), amps(sH)
            R[foot].setdefault(f"{s:g}", {})[sm] = dict(all=c, inner=r, outer=o, cls=cls(c), A_L={k: aL[k] for k in aL}, A_H={k: aH[k] for k in aH})
            Q(f"  [{foot} {sm}] red +{s:<5g}: chi2 L {c['chi2_L']:5.1f} (p {c['pL']:.3f}), H {c['chi2_H']:5.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+6.1f}; D {c['D']:.2f}; {cls(c)}; inner {r['dchi2']:+.1f}, outer {o['dchi2']:+.1f}; L A_in {aL['A_in']:.2f} O1 {aL['A_O1']:.2f} O2 {aL['A_O2']:.2f}+-{aL['sA_O2']:.2f}; H A_in {aH['A_in']:.2f} O1 {aH['A_O1']:.2f}")
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
json.dump(R, open(os.path.join(HEREX, "si2_sens.json"), "w"), indent=1, default=float); open(os.path.join(HEREX, "si2_sens.out"), "w").write("\n".join(OUT2) + "\n")
