#!/usr/bin/env python3
"""SI2 POST-RESULT, reported only: R2's stars with the halo not following all of it. Red M* +0.295 for baryons in both models; route E's halo (EM1's M200 argument) moves only by h = 0, 0.123, 0.295 dex. h 0.295 must reproduce the frozen R2. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
HEREX = os.path.dirname(os.path.abspath(__file__)); srcx = open(os.path.join(HEREX, "si2_grade.py")).read(); cutx = 'J1 = None if MUT2 else'; assert srcx.count(cutx) == 1
__file__ = os.path.join(HEREX, "si2_grade.py"); exec(compile(srcx[:srcx.index(cutx)], "si2_head", "exec")); HERE2 = HEREX; R = {}
def town_mix(foot, sb, sh, fhot=0.5):
    tab = np.empty((len(LMG), 15)); Rpe = EDGES * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / H0N); lmc = lm + (-0.69 * lm70 + 6.63); Msb = 10 ** (lm + sb); Msh = 10 ** (lm + sh); Mc = 10 ** lmc; Mh_ = fhot * 10 ** lm
        Mb = Msb + Mc + Mh_ * np.minimum(1.0, (RG / 1e5) ** 3); Mh, _ = halo_of(foot, RG, Msh, Mc, Msh + Mc + Mh_, 0.0, "E"); tab[gi] = bin_avg(Rpe, lambda R_: AQ.delta_sigma(R_, RG, Mb + HF * Mh, "const"))
    return np.stack([tab, tab], 1)
J0 = json.load(open(os.path.join(HEREX, "si2_results.json")))["foot"]; dk = 0.0
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, _ = build(foot); R[foot] = {}
    TOWN[(foot, "red")] = law_table(foot, SHIFT); N["tix"], N["MBN_g"] = TIX2, MBN2; tL = tnbr(foot, node=0); mL = modl(foot, tL, "R2")
    for h in (0.295, 0.123, 0.0):
        shg = np.where(red_g, h, 0.0); lbh = np.log10(10 ** lMb_g + 10 ** lMs_g * (10 ** shg - 1)); N["tix"] = np.clip(np.round((lbh - LMB_T[0]) / 0.05).astype(int), 0, len(LMB_T) - 1); N["MBN_g"] = MBN2
        TOWN[(key, "red")] = town_mix(foot, SHIFT, h); tH = tnbr(key, node=0); mH = modl(key, tH, "R2")
        for sm in ("S3", "S1"):
            sL, sH = st(mL, sm, "all"), st(mH, sm, "all"); c = compare(sL, sH); r = compare(sL, sH, RANGE["in"]); o = compare(sL, sH, RANGE["out"]); aL, aH = amps(sL), amps(sH); g = cls(c)
            if h == 0.295: dk = max(dk, abs(c["chi2_H"] - J0[foot][sm]["all_R2"]["all"]["chi2_H"]), abs(c["chi2_L"] - J0[foot][sm]["all_R2"]["all"]["chi2_L"]))
            R[foot].setdefault(f"{h:g}", {})[sm] = dict(all=c, inner=r, outer=o, cls=g, A_L=aL, A_H=aH, m_H=sH["m"].tolist(), d=sL["d"].tolist())
            Q(f"  [{foot} {sm}] stars +0.295, halo +{h:<5g}: chi2 L {c['chi2_L']:5.1f} (p {c['pL']:.3f}), H {c['chi2_H']:5.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+6.1f}; D {c['D']:.2f}; {g}; inner {r['dchi2']:+.1f}, outer {o['dchi2']:+.1f}; H A_in {aH['A_in']:.2f}+-{aH['sA_in']:.2f} O1 {aH['A_O1']:.2f}+-{aH['sA_O1']:.2f}")
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
Q(f"K h 0.295 reproduces the frozen R2 chi2 (S3, S1, both footings): max |d| {dk:.1e}: {'PASS' if dk <= 1e-9 else 'FAIL'}"); R["K"] = dk
json.dump(R, open(os.path.join(HEREX, "si2_halo_rung.json"), "w"), indent=1, default=float); open(os.path.join(HEREX, "si2_halo_rung.out"), "w").write("\n".join(OUT2) + "\n")
