#!/usr/bin/env python3
"""CFG316 Stage B POST HOC diagnostics (labelled; they change no frozen verdict).  They read only the Stage B stack outputs and the global
source ellipticity means (no new lens is stacked).
  P1  the C4 failure: the random-point cross shear per K1 bin, the weighted mean source ellipticities (additive c-terms, which the June
      estimator does not remove), and whether the class difference D can see them (a signal common to both classes cancels in D).
  P2  the absolute ESD amplitude Q with a DIAGONAL covariance (the 14x14 jackknife from 30 patches of ~10-35 lenses is noisy; the
      Hartlap factor is 0.48), per class and joint.
  P3  the Stage A power model's predicted sigma(D) on K1 for ISO-P against the measured jackknife sigma.
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_stageB_posthoc.py
"""
import os, sys, json
import numpy as np
from scipy.stats import chi2 as CHI2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *   # noqa
sys.path.insert(0, CFG)
import CFG7_common as C7       # noqa: E402

R = C7.Report("cfg316_stageB_posthoc", False)
P, check = R.P, R.check
P(__doc__.split("Run from")[0].strip())
pv = lambda x, k=7: float(CHI2.sf(x, k))
L = np.load(os.path.join(WORK, "cfg316_lenses.npz"))
ST = np.load(os.path.join(WORK, "cfg316_stack.npz"))
B = json.load(open(os.path.join(HERE, "cfg316_stageB_results.json")))
A = json.load(open(os.path.join(HERE, "cfg316_stageA_results.json")))
idx, PL = ST["idx"], ST["PL"]
cl, pa = L["clsb"][idx].astype(int), L["patch"][idx]
hb = L["mass_ok"][idx] & L["matched"][idx] & L["complete"][idx]
isoP = hb & L["isoP"][idx]

# P1
S = read_shear_columns(["e1", "e2", "weight"])
w = S["weight"].astype("f8")
c1m, c2m = float(np.sum(w * S["e1"]) / w.sum()), float(np.sum(w * S["e2"]) / w.sum())
del S
PLr, rp = ST["PLr"], ST["rpatch"]
Sr = np.zeros((4, NPATCH, 15))
for q in range(4):
    np.add.at(Sr[q], rp, PLr[:, q, :])
tw = Sr[1].sum(0)
et, ex = Sr[0].sum(0) / tw / KG, Sr[3].sum(0) / tw / KG
looX = (Sr[3].sum(0)[None] - Sr[3]) / (tw[None] - Sr[1]) / KG
sx = np.sqrt(np.diag(jk_cov(looX[:, K1])))
sD = np.array(B["numbers"]["ISO-P"]["sigma"])
check("P1 (post hoc) the C4 failure: random-point cross shear on K1 vs the split's errors",
      f"random cross [Msun/pc^2] {np.round(ex[K1], 2).tolist()} +- {np.round(sx, 2).tolist()}; random tangential {np.round(et[K1], 2).tolist()}; "
      f"weighted mean source e1 {c1m:+.2e}, e2 {c2m:+.2e} (raw lensfit; the June estimator subtracts no c-term); largest |random cross| / "
      f"sigma(D, ISO-P) = {np.max(np.abs(ex[K1]) / sD):.3f}; an additive term common to both classes cancels in D at fixed geometry",
      True, load_bearing=False)

# P2
ABS = B["numbers"]["ABS"]
rows = []
for nm, sel in (("ISO-P", isoP), ("complete base", hb)):
    Sx = class_patch_sums(PL, cl, pa, sel)
    esd, loo = esd_loo(Sx)
    key = "ISO-P (photo-z isolated)" if nm == "ISO-P" else "complete base (NOT isolated)"
    for c_, lab in ((0, "late"), (1, "early")):
        s2 = np.diag(jk_cov(loo[:, c_, K1]))
        rows.append(f"{nm} {lab}: ESD/sigma per K1 bin {np.round(esd[c_, K1] / np.sqrt(s2), 1).tolist()}")
    P(f"  {nm}: N early {int(np.sum(sel & (cl == 1)))}, late {int(np.sum(sel & (cl == 0)))}")
R.banner("P2 (post hoc) diagonal-covariance absolute amplitude Q (law at catalogue M*, both footings)")
sys.path.insert(0, HERE)
# the law stacks are recomputed in cfg316_stageB.py; here the diagonal Q uses the model values stored by re-running the model machinery
import io, contextlib
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(CFG, "CFG95_kids_split_own_calibration.py")).read()
g95 = {"__file__": os.path.join(CFG, "CFG95_kids_split_own_calibration.py"), "__name__": "lane95"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================== C1-C3")], "CFG95", "exec"), g95)
g61 = g95["g61"]; LMG, ZG = g61["LMG"], g61["ZG"]
lm, z, Mg = L["logM"][idx], L["z"][idx], L["Mgal"][idx]
im = np.clip(np.round((lm - LMG[0]) / 0.05).astype(int), 0, len(LMG) - 1)
iz = np.clip(np.round((z - 0.05) / 0.10).astype(int), 0, len(ZG) - 1)
QD = {}
for nm, sel in (("ISO-P", isoP), ("complete base", hb)):
    def weights(c_, scrit=False, sel=sel):
        ww = np.zeros((len(LMG), len(ZG))); s = sel & (cl == c_)
        np.add.at(ww, (im[s], iz[s]), Mg[s]); return ww
    g61["weights"] = weights
    Sx = class_patch_sums(PL, cl, pa, sel)
    esd, loo = esd_loo(Sx)
    for foot in ("canonical", "alt"):
        ml, me = g61["stack"](0, foot, "L", "blue"), g61["stack"](1, foot, "L", "red")
        out = []
        num = den = 0.0
        for c_, mm in ((0, ml), (1, me)):
            v = np.diag(jk_cov(loo[:, c_, K1]))
            q = float(np.sum(mm[K1] * esd[c_, K1] / v) / np.sum(mm[K1] ** 2 / v)); sq = float(1 / np.sqrt(np.sum(mm[K1] ** 2 / v)))
            out.append((q, sq)); num += np.sum(mm[K1] * esd[c_, K1] / v); den += np.sum(mm[K1] ** 2 / v)
        QD[f"{nm}|{foot}"] = dict(late=out[0], early=out[1], joint=(float(num / den), float(1 / np.sqrt(den))))
        P(f"  {nm:14s} {foot:9s}: diagonal Q late {out[0][0]:.2f} +- {out[0][1]:.2f}, early {out[1][0]:.2f} +- {out[1][1]:.2f}, "
          f"joint {num / den:.2f} +- {1 / np.sqrt(den):.2f}")
check("P2 (post hoc) the absolute amplitude with a diagonal covariance (robustness of the GLS Q in cfg316_stageB.out)",
      json.dumps(QD) + " | " + "; ".join(rows), True, load_bearing=False)

# P3
pred = np.array(A["numbers"]["power"]["P"]["sigma_D_K1"])
check("P3 (post hoc) the Stage A power model vs the measured ISO-P jackknife sigma(D) on K1",
      f"predicted {np.round(pred, 1).tolist()}; measured {np.round(sD, 1).tolist()}; ratio measured/predicted {np.round(sD / pred, 2).tolist()} "
      f"(median {np.median(sD / pred):.2f})", True, load_bearing=False)
R.num("P1", dict(cross=ex[K1].tolist(), sig=sx.tolist(), c1=c1m, c2=c2m)); R.num("P2", QD); R.num("P3", dict(pred=pred.tolist(), meas=sD.tolist()))
R.write(here=HERE)
