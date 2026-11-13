"""EUC11 post hoc diagnostic (after the frozen run; not a gate): which substitution breaks transfer check T1.
Run:  python3 -I euc11_t1_posthoc.py <dir with the ECLIPSE csv files and nisp_tables/>
"""
import sys, math, numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import euc11 as X
E = X.E; edir = sys.argv[1]
rows, _ = E.load(edir); E.OUT.clear(); Pm, _ = E.select(rows, ("A",)); Sm, _ = E.select(rows, ("A", "B")); pipe = X.eclipse_pipeline(edir)
def ell(fh, z): return np.log10(fh) + 2.0 * np.log10(E.EUCLID.DL(z) / X.MPC)
tr = [r for r in Sm if r["id"] in pipe]; fh = np.array([pipe[r["id"]][0] for r in tr]); zp = np.array([pipe[r["id"]][1] for r in tr]); y = E.arr(tr, "lm")
A = np.column_stack([np.ones(len(tr)), ell(fh, zp), zp]); coef = np.linalg.lstsq(A, y, rcond=None)[0]
sub = [r for r in Pm if r["id"] in pipe]; f = np.array([pipe[r["id"]][0] for r in sub]); z = np.array([pipe[r["id"]][1] for r in sub])
lmp = coef[0] + coef[1] * ell(f, z) + coef[2] * z
def sf(**kw):
    eng, zz, RE, Re, n, lm = E.build(sub, **kw); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(zz, E.ZS_INF)
    return ["%.3f / %+.3f" % (st["f25"], st["b_med"]) for st in (E.stats(eng.solve_b(Mmin, a0, "S")) for a0 in E.FOOT.values())]
print("post hoc diagnostic on ECLIPSE sample P with pipeline data (N = %d): f25 / median b, canonical ; alt" % len(sub))
print("  catalogue photo-z, catalogue mass      :", " ; ".join(sf()))
print("  pipeline photo-z, catalogue mass       :", " ; ".join(sf(z=z, lm=E.arr(sub, "lm") + 2.0 * np.log10(E.EUCLID.DL(z) / E.EUCLID.DL(E.arr(sub, "z"))))))
print("  catalogue photo-z, predicted mass      :", " ; ".join(sf(lm=coef[0] + coef[1] * ell(f, E.arr(sub, "z")) + coef[2] * E.arr(sub, "z"))))
print("  pipeline photo-z, predicted mass (T1)  :", " ; ".join(sf(z=z, lm=lmp)))
r = E.arr(sub, "lm") - lmp
print("  catalogue minus predicted log M*: median %+.3f, scatter %.3f; slope of the residual against catalogue log M*: %+.2f" % (np.median(r), np.std(r), np.polyfit(E.arr(sub, "lm"), r, 1)[0]))
