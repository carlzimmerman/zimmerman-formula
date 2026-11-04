"""A46 post-hoc diagnostic (added after recipe47.out, labelled as such): MOG and conformal gravity with the papers' per-galaxy M/L freedom.
One baryon-mass scale f per galaxy (bounded 0.2 to 5), universal published constants. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import i1e, k1e
c_ = 2.998e8; NSH = 2000
def gyuk(r, s, dm, mu):
    R = r[:, None]; S = s[None, :]; ms = mu * S; mr = mu * R
    out = (np.exp(mu * (S - R)) - np.exp(-mu * (S + R))) / 2 / ms * (1 + mr) / R**2
    inn = -(np.exp(mu * (R - S)) * (mr - 1) + np.exp(-mu * (R + S)) * (mr + 1)) / 2 / ms / R**2
    return G * ((np.where(R > S, out, inn)) * dm[None, :]).sum(1)
GST, GAM0, KAP = 5.42e-39, 3.06e-28, 9.54e-50
def mog_f(g, f):
    M = f * g.vb2 * g.r / G; e = np.union1d(np.linspace(0, g.r[-1], NSH + 1), g.r); Me = np.interp(e, np.r_[0., g.r], np.r_[0., M])
    return np.maximum(9.89 * f * g.gb - 8.89 * gyuk(g.r, .5 * (e[1:] + e[:-1]), np.diff(Me), .042 / kpc), 1e-14)
def cg_f(g, f):
    x = g.r / (2 * g.Rd); return np.maximum(f * g.gb + f * g.Mb * GST * c_**2 * x * i1e(x) * k1e(x) + GAM0 * c_**2 / 2 - KAP * c_**2 * g.r, 1e-14)
for tag, fn in (('MOG universal alpha 8.89, mu 0.042', mog_f), ('CG published constants, N* = stars + gas', cg_f)):
    cur, fs = [], []
    for g in GS:
        r = minimize_scalar(lambda lf: ((np.log10(fn(g, 10**lf)) - np.log10(g.gl))**2).sum(), bounds=(np.log10(.2), np.log10(5)), method='bounded')
        fs.append(10**r.x); cur.append(fn(g, 10**r.x))
    fs = np.array(fs); nb = int(((np.abs(np.log10(fs)) > np.log10(5) - 1e-3)).sum())
    grade(f'DIAG (post hoc) {tag}, one mass scale per galaxy fitted to the law (171 knobs)', cur, f'(f median {np.median(fs):.3f}, p16-p84 {np.percentile(fs, 16):.3f}-{np.percentile(fs, 84):.3f}; at bound {nb})')
print('Post-hoc diagnostic, not a frozen row. Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
