"""Bounded spectrum for a large homogeneous clock response.

Uses the previously pinned general ADM reduction. A nonlinear acceleration
function can have this slope at zero acceleration; its static and finite-
amplitude behavior require separate checks. No PPN or closure claim follows.
"""
from pathlib import Path
import json
import sympy as s
import mpmath as mp

here = Path(__file__).resolve().parent
source = here.parents[1] / 'frw_repair/run_verified/general_reduced.json'
d = json.loads(source.read_text())
M, R = (s.sympify(d[x]) for x in ('mass', 'rest'))
lookup = {str(x): x for x in M.free_symbols | R.free_symbols}
variables = [lookup[x] for x in ('av', 'H', 'q', 'j', 'ep', 'xi', 'k', 'clock_alpha', 'clock_alpha_dot', 'clock_c2')]
mf = s.lambdify(variables, M, 'mpmath', cse=True)
rf = s.lambdify(variables, R, 'mpmath', cse=True)
mp.mp.dps = 65
ep = mp.mpf('1e-9')
c2 = mp.mpf('.03')
gc = 1+3*c2/2
j0 = -mp.mpf('1.86')/(1-ep)
lam = 3*gc-(ep-1)*j0/2
scale = mp.mpf(299792458)/67400
xi = mp.mpf('.000004')/scale
rows = []
for alpha_text in ('.05', '.2', '.5'):
    alpha = mp.mpf(alpha_text)
    for index in range(33):
        a = mp.power(10, -mp.mpf(index)/8)
        q = 1-3*ep*mp.log(a)
        j = j0/a**3
        h = mp.sqrt(((ep-q)*j/2+lam)/(3*gc))
        for k_text in ('.000001', '.00001', '.0001', '.001', '.01', '.1', '1', '10'):
            k = mp.mpf(k_text)*scale
            args = (a,h,q,j,ep,xi,k,alpha,0,c2)
            m, r = mp.matrix(mf(*args)), mp.matrix(rf(*args))
            A2 = -(m**-1)*r
            A = mp.matrix([[0,1,0,0],list(A2[0,:]),[0,0,0,1],list(A2[1,:])])
            eig = mp.eig(A,left=False,right=False)
            positive = -m[0,0]>0 and mp.det(m)>0
            assert positive
            rows.append({'alpha':alpha_text, 'a':float(a),'k_Mpc_inv':k_text,
                         'k_over_aH':float(k/(a*h)), 'kinetic_positive':bool(positive),
                         'largest_frozen_real_rate_over_H':float(max(mp.re(z) for z in eig)/h),
                         'eigenvalues_over_H':[[float(mp.re(z)/h),float(mp.im(z)/h)] for z in eig]})
    selected = [r for r in rows if r['alpha']==alpha_text]
    print('alpha',alpha_text,'points',len(selected),'max frozen rate/H',max(r['largest_frozen_real_rate_over_H'] for r in selected),flush=True)
(here/'spectrum.json').write_text(json.dumps(rows,indent=2)+'\n')
