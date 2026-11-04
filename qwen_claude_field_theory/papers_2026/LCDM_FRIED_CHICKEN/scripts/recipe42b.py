"""A41 post-result diagnostic (not a grade): why the BEC matching has no root in about half of SPARC at the b1 R.
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe42.py')).read()
exec(s[:s.index('SMJ = [')])
exec(s[s.index('NRC, NRR = 48, 400'):s.index('def sec_b():')])
R = 10**0.5478 * kpc  # b1 R 3.53 kpc
cls = {'all h > 0 (core heavier than NFW at every crossing)': 0, 'all h < 0': 0, 'no crossing at all': 0, 'mixed signs but gaps (nan between)': 0, 'root': 0}
rtR = []
for i, g in enumerate(GS):
    M = M0S[i]; c = float(cflat(M, 0., 0.)); fb = min(g.Mb / M, .5)
    R2 = (3 * M * Msun / (800 * np.pi * RHOC))**(1 / 3); rs = R2 / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); w = 1 - fb
    rN = lambda r: w * rhos / ((r / rs) * (1 + r / rs)**2); mN = lambda r: w * M * Msun * mu(r / rs) / mu(c)
    K2 = 4 * G * R**2 / np.pi; r = np.logspace(np.log10(R * 1e-4), np.log10(R * 1.2), NRR); B = MBF[i](r); Bm = MBF[i](np.sqrt(r[:-1] * r[1:]))
    LR = np.linspace(np.log(rN(R)) - 1, np.log(rN(R * 1e-3)) + 3, NRC); Rh, Ms = bint(LR, r, B, Bm, K2); sg = Rh - rN(r)[None, :]; hh = []
    for t in range(NRC):
        idx = np.where((sg[t, :-1] > 0) & (sg[t, 1:] <= 0))[0]
        if not len(idx): hh.append(np.nan); continue
        j = idx[-1]; rt = r[j]; hh.append(np.log(Ms[t, j]) - np.log(mN(rt)))
    hh = np.array(hh); f = np.isfinite(hh)
    o = bec_core(MBF[i], M, c, fb, R)
    if o is not None: cls['root'] += 1; rtR.append(o['rt'] / R); continue
    if not f.any(): cls['no crossing at all'] += 1
    elif (hh[f] > 0).all(): cls['all h > 0 (core heavier than NFW at every crossing)'] += 1
    elif (hh[f] < 0).all(): cls['all h < 0'] += 1
    else: cls['mixed signs but gaps (nan between)'] += 1
print('BEC matching at R 3.53 kpc, base halo, 171 galaxies:'); [print(f'  {k}: {v}') for k, v in cls.items()]
print(f'  r_t/R where a root exists: median {np.median(rtR):.3f}, p16-84 {np.percentile(rtR, 16):.3f}-{np.percentile(rtR, 84):.3f}')
lb = np.log10([g.Mb for g in GS]); ok = np.array([bec_core(MBF[i], M0S[i], float(cflat(M0S[i], 0, 0)), min(g.Mb / M0S[i], .5), R) is not None for i, g in enumerate(GS)])
print(f'  median log M_b with root {np.median(lb[ok]):.2f}, without {np.median(lb[~ok]):.2f}')
print('Diagnostic only, post-result. Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
