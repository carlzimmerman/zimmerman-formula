#!/usr/bin/env python3
"""AKS1 reported diagnostic for KA7's failure (post hoc; sets no label): the homogeneous row with the n = 1 pressure on
(as graded) and off. Locates the deviation from FRW.

    python3 aks1_ka7_probe.py -> aks1_ka7_probe.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import aks1_lib as L

out = ['AKS1 KA7 probe (reported, post hoc): homogeneous row, sink off, canonical. kappa = 1/2 FITTED; not theory closed.']
for mu, tag in ((None, 'pressure on (mu_J, as graded)'), (0, 'pressure off')):
    o = L.run('canonical', 10.5, key='off', homogeneous=True, mu_Mpc=mu)
    d = o['_r'] / (o['a_end'] * o['_X']) - 1
    i = int(np.argmax(np.abs(d)))
    n_bad = int((np.abs(d) > 1e-3).sum())
    out.append(f'{tag}: max |r/(a X) - 1| = {np.abs(d).max():.3e} at shell {i} (X = {o["_X"][i]:.1f} kpc comoving), '
               f'median {np.median(np.abs(d)):.2e}, shells above 1e-3: {n_bad}; innermost five {np.round(d[:5], 6).tolist()}')
out.append('Reading: the deviation sits at the inner edge of the shell grid, where the binned density has an empty hole inside '
           'the first shell and the n = 1 pressure pushes the innermost shells inward; with the pressure off the integrator '
           'follows FRW to the table interpolation level.')
out.append('\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.')
open(os.path.join(HERE, 'aks1_ka7_probe.out'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
