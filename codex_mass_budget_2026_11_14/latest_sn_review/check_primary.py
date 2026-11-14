"""Independent AGB4 primary check; no imports from Claude's analysis lanes.

Usage: /private/tmp/forj0332-fit-venv/bin/python check_primary.py RESULT_PATH
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import cholesky, solve_triangular

HERE = Path(__file__).resolve().parent
INP = HERE / 'inputs'
table = np.genfromtxt(INP / 'PantheonPlusSH0ES.dat', names=True, dtype=None, encoding='utf8')
with (INP / 'sdsssn_master.dat2').open() as f:
    header = f.readline().split()
    rows = [r.split() for r in f if r.strip()]
positions = {name: max(j for j, value in enumerate(header) if value == name)
             for name in ['age_Ravi', 'age_lo_Ravi', 'age_hi_Ravi']}
ages = {r[0]: [float(r[positions[k]]) if r[positions[k]] != '\\N' else np.nan
               for k in positions] for r in rows}
indices = [i for i, r in enumerate(table)
           if r['IDSURVEY'] == 1 and str(r['CID']) in ages
           and np.isfinite(ages[str(r['CID'])][0]) and ages[str(r['CID'])][1] > 0]
sub = table[indices]
age = np.array([ages[str(r['CID'])][0] for r in sub])
cvraw = np.loadtxt(INP / 'PantheonPlusSH0ES_STAT+SYS.cov')
n_all = int(cvraw[0])
covariance = cvraw[1:].reshape(n_all, n_all)[np.ix_(indices, indices)]
assert len(indices) == 286
assert len(set(map(str, sub['CID']))) == 286
z = sub['zHD']
integral = np.array([quad(lambda t: 1/np.sqrt(0.334*(1+t)**3+0.666), 0, zi,
                          epsabs=1e-12, epsrel=1e-12)[0] for zi in z])
mu = 5*np.log10((1+sub['zHEL'])*integral)
edges = np.quantile(z, np.linspace(0, 1, 9))
bins = np.minimum(np.searchsorted(edges[1:-1], z, side='right'), 7)
base = np.eye(8)[bins]
low = (sub['HOST_LOGMASS'] < 10).astype(float)-0.5
reference = json.loads((INP / 'agb4_M.json').read_text())['fits']

def solve(y, raw, step, full_cov=False):
    parts = [base]
    if raw:
        parts += [sub['x1'], sub['c']]
    if step:
        parts += [low]
    parts += [-0.030*age]
    x = np.column_stack(parts)
    if full_cov:
        chol = cholesky(covariance, lower=True)
        xx = solve_triangular(chol, x, lower=True)
        yy = solve_triangular(chol, y, lower=True)
    else:
        sw = np.diag(covariance)**-0.5
        xx, yy = x*sw[:, None], y*sw
    beta, _, rank, singular = np.linalg.lstsq(xx, yy, rcond=None)
    _, r = np.linalg.qr(xx, mode='reduced')
    r_inverse = np.linalg.solve(r, np.eye(r.shape[0]))
    covariance_beta = r_inverse@r_inverse.T
    residual = yy-xx@beta
    a, sd = beta[-1], np.sqrt(covariance_beta[-1, -1])
    result = dict(A=float(a), sd_A=float(sd), D_A0=float((a/sd)**2),
                  D_A1=float(((a-1)/sd)**2), chi2=float(residual@residual),
                  rank=int(rank), n_columns=x.shape[1], condition=float(singular[0]/singular[-1]))
    if step:
        result.update(g=float(beta[-2]), sd_g=float(np.sqrt(covariance_beta[-2, -2])))
    return result

out = dict(n=len(indices), redshift=[float(z.min()),float(z.max())], bins=np.bincount(bins).tolist(), fits={})
for raw, reading in [(True,'R'), (False,'P')]:
    y = sub['mB' if raw else 'm_b_corr']-mu
    for step, name in [(False,'M0'),(True,'M1')]:
        fit = solve(y, raw, step)
        ref = reference[name]['primary' if raw else 'reading_P']
        fit['difference_from_stored_A'] = fit['A']-ref['A']
        fit['difference_from_stored_sd_A'] = fit['sd_A']-ref['sd_A']
        assert abs(fit['difference_from_stored_A']) < 1e-6
        assert abs(fit['difference_from_stored_sd_A']) < 1e-10
        out['fits'][reading+'_'+name] = fit
        out['fits'][reading+'_'+name+'_full_covariance_sensitivity'] = solve(y, raw, step, True)
out['checks'] = ['286 unique IDs', 'full-rank designs', 'direct quadrature for distances',
                 'independent SVD coefficients and QR covariance', 'all four stored fits agree']
assert all(v['rank'] == v['n_columns'] for v in out['fits'].values())
Path(sys.argv[1]).write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
