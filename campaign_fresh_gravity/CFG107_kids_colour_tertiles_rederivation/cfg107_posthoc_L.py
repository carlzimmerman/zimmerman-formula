"""POST HOC (after the frozen main and MUTATE runs; labelled): does CFG115's colour-split LCDM reference (a class-mix of the two class stacks, weighted by each class's pair weights) reproduce
its jackknifed-reference zero-offset chi2 77.6 (mine, all-lens stack reference: 22.7)?  Read from the CFG115 script AFTER my runs: refL = (wcls0*L_blue(late) + wcls1*L_red(early))/(wcls0+wcls1)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg107_body.py")).read()
src = src[:src.index('# ---- R6 / A1 amplitude definition table')] if '# ---- R6 / A1 amplitude definition table' in src else src[:src.index('log("== R6 / A1')]
g = {"__file__": os.path.join(HERE, "cfg107_run.py")}
exec(compile(src, "body_prefix", "exec"), g)
np = g["np"]; L = g["L"]; math = g["math"]
B6, A0, W0, K1, typ, WW, Mgal, z, lmg, logMs, nL, psum, allm, h6 = [g[k] for k in ("B6", "A0", "W0", "K1", "typ", "WW", "Mgal", "z", "lmg", "logMs", "nL", "psum", "allm", "h6")]
key = typ.astype(np.int64) * 10 ** 9 + np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
uk, gi, cnt = np.unique(key, return_inverse=True, return_counts=True); NG = len(cnt)
mean_ = lambda x: np.bincount(gi, weights=x) / cnt
GR = dict(Mgal=10 ** mean_(lmg), logM=mean_(logMs), z=mean_(z), typ=np.bincount(gi, weights=typ) / cnt)
tab = np.zeros((NG, 15))
for i in range(NG): tab[i] = L.v_one("L", GR["Mgal"][i], GR["logM"][i], GR["z"][i], int(round(GR["typ"][i])))
def stack_m(mask):
    w = np.bincount(gi[mask], weights=Mgal[mask], minlength=NG); return (w @ tab) / w.sum()
wcls = {c: WW[typ == c][:, K1].sum(0) for c in (0, 1)}
refA = stack_m(allm)[K1]
refC = (wcls[0] * stack_m(typ == 0)[K1] + wcls[1] * stack_m(typ == 1)[K1]) / (wcls[0] + wcls[1])
wk1 = psum(allm, WW, K1).sum(0)
Cj, Cf = W0["Cs"]["jkref"], W0["Cs"]["fixref"]
for nm, ref in (("all-lens stack reference", refA), ("class-mix reference (CFG115 construction)", refC)):
    Am = np.array([math.log10((wk1 * stack_m(m)[K1]).sum() / (wk1 * ref).sum()) for m in B6["masks"]])
    r = A0 - Am; one = np.ones(6)
    Pj, Pf = h6 * np.linalg.inv(Cj), h6 * np.linalg.inv(Cf)
    # normalisation defect: sum_c omega_c 10^{A_c}, omega_c = the data's pair-weight share of bin c (K1)
    om = np.array([psum(m, WW, K1).sum(0) @ np.ones(len(K1)) for m in B6["masks"]]); om = om / om.sum()
    print("%-45s model A %s  chi2 (a) %.1f (b) %.1f (c) %.1f ; normalisation defect sum om 10^A - 1: model %+.4f  data %+.4f" %
          (nm, np.round(Am, 3), r @ Pj @ r, r @ Pf @ r, r @ Pj @ r - (one @ Pj @ r) ** 2 / (one @ Pj @ one), (om * 10 ** Am).sum() - 1, (om * 10 ** A0).sum() - 1))
