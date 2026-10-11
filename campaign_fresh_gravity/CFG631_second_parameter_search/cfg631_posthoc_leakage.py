"""CFG631 POST HOC (disclosed after the frozen run; no verdict weight): re-score the KiDS partial-property splits with each
group's OWN satellite leakage (CFG586's rule: f = clip(lambda_group / lambda_f30all x CFG529's measured f30 grid)). Motivation: the
frozen estimator gives both groups the f30-average leakage, so a split on companion count (env) can turn extra satellite signal
into apparent 'excess'. Run: nice -n 10 python3 cfg631_posthoc_leakage.py
"""
import os, sys, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg631_common as K  # noqa: E402

try:
    os.nice(10)
except OSError:
    pass
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


A, B = K.kids_heads()
raw, part, E2, qid = K.kids_props(A, B)
esd_loo, comps, all_bands, BANDS, CONS, FOOTS, NPATCH = (A[k] for k in ("esd_loo", "comps", "all_bands", "BANDS", "CONS", "FOOTS", "NPATCH"))
G = A["comps"].__globals__; MEAS, SHMRS = G["MEAS"], G["SHMRS"]
CELLS = [(c, f) for c in CONS for f in FOOTS]
lam_all = B["stat"](A["F30"], B["wl"])[0][3]


def tert(v):
    t1, t2 = np.nanquantile(v[E2], [1 / 3, 2 / 3]); return E2 & (v > t2), E2 & (v < t1)


def eps(mask, fac):
    d, Cv, Lj = esd_loo(mask); out = {}
    fl = {s: np.clip(fac * MEAS["f30"][s], 0, 1) for s in SHMRS}
    for c, f in CELLS:
        cp = comps(c, f, mask, fE=fl, fO=fl); fb = all_bands(d, Cv, cp); mM = cp["moster"][0] + cp["moster"][1]
        out[(c, f)] = (fb, {bd: (Lj[:, ii] - mM[ii][None, :]) @ np.array(fb[bd]["wvec"]) for bd, ii in BANDS.items()})
    return out


P("CFG631 POST HOC: own-leakage re-score of the KiDS splits (CFG586 rule); no verdict weight")
P(f"lambda f30 all {lam_all:.3f}")
RES = {}
for nm, (hi, lo) in [(k, tert(part[k])) for k in K.KPROPS] + [("logM_raw", tert(A["LMSL"]))]:
    lh, ll = B["stat"](hi, B["wl"])[0][3], B["stat"](lo, B["wl"])[0][3]
    gh, gl = eps(hi, lh / lam_all), eps(lo, ll / lam_all)
    row = []
    for c, f in CELLS:
        (fh, Lh), (fl_, Ll) = gh[(c, f)], gl[(c, f)]
        dv = Lh["K9"] - Ll["K9"]; vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2)
        s = math.sqrt(max(vj, fh["K9"]["sig"] ** 2 + fl_["K9"]["sig"] ** 2)); dd = fh["K9"]["eps"] - fl_["K9"]["eps"]
        RES[f"{nm}|{c}|{f}"] = dict(D=float(dd), sig=float(s), Z=float(dd / s), lam_hi=float(lh), lam_lo=float(ll))
        row.append(f"[{c} {f[:3]}] {dd:+.3f} (Z {dd / s:+.2f})")
    P(f"  {nm:8s} lambda HIGH {lh:.3f} LOW {ll:.3f}   D(K9, own leakage) " + "  ".join(row))
json.dump(RES, open(os.path.join(K.HERE, "cfg631_posthoc_leakage_results.json"), "w"), indent=1)
open(os.path.join(K.HERE, "cfg631_posthoc_leakage.out"), "w").write("\n".join(OUT) + "\n")
