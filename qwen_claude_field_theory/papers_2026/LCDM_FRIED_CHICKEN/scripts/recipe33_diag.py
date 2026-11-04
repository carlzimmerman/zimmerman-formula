"""A31 post-result diagnostic (not a gate): continuous minimax of G1 and GT residuals for Qv, Qm, Qc.
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe33.py')).read(); exec(src[:src.index('# ---------- (a) ----------')])
from scipy.optimize import minimize
def ob(p, typ):
    R = integ(typ, [p[0]], [p[1]])
    if not R['ok'][0]: return 9.
    d = grade_pt(mfun(R, 0, 'S8'), LCF['S8']); return max(abs(np.log10(d['ke'] / .5)), max(abs(v) for v in d['gt'].values()))
for typ, st in (('Qv', [(-.6, .8), (-.5, .3), (-1., 1.)]), ('Qm', [(-.6, -.8), (-1., -1.), (-1., 1.)]), ('Qc', [(.3, -1.), (-.5, 0.)])):
    best = min((minimize(ob, s, args=(typ,), method='Nelder-Mead', options=dict(xatol=1e-3, fatol=1e-4, maxiter=150)) for s in st), key=lambda r: r.fun)
    R = integ(typ, [best.x[0]], [best.x[1]]); d = grade_pt(mfun(R, 0, 'S8'), LCF['S8'])
    print(f'{typ} minimax at xi0 {best.x[0]:+.3f} xi1 {best.x[1]:+.3f}: max residual {best.fun:.3f} dex (tol 0.05); kappa_eff {d["ke"]:.3f}; GT ' + ' '.join(f'{v:+.3f}' for v in d['gt'].values()) + f'; G4 {d["sp"]:.3f}')
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
