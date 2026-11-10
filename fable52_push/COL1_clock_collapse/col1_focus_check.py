#!/usr/bin/env python3
"""COL1 cross-check (reported, not graded): time for a test shell at rest in Hubble flow at z 10, inside the softened
point mass (eps 1 kpc, smoothstep ramp over 1 Gyr), to reach the centre. Inside the core the force is harmonic, so every
shell arrives together: a central focusing whose time does not depend on the shell. Compared with the primary rows' events.

    python3 col1_focus_check.py -> col1_focus_check.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import col1_lib as L
kd1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
out = ['COL1 focusing check: test shell in the softened ramping point mass, Hubble start at z 10. kappa = 1/2 FITTED; not theory closed.']
for f in ('canonical', 'alt'):
    s = kd1['footings'][f]['setting']; cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    ti = cos.t_of_a(1 / 11); H = cos.H_of_a(1 / 11)
    for lM in (9.4, 10.45, 10.7, 10.9):
        Mb = 10 ** lM; ts = []
        for r0 in (0.001, 0.01, 0.1):
            def rhs(t, y):
                a = cos.a_of_t(t); M = Mb * float(L.smoothstep((t - ti) / (1 / L.TU)))
                g = -L.G * M * y[0] / (y[0] ** 2 + 1.0) ** 1.5 + (-(4 * math.pi / 3) * L.G * (cos.nbar0 + cos.rhob0) * a ** -3 + cos.OL * cos.H0 ** 2) * y[0]
                return [y[1], g]
            ev = lambda t, y: y[0] - 1e-6 * r0; ev.terminal = True; ev.direction = -1
            sol = solve_ivp(rhs, (ti, ti + 1 / L.TU), [r0, H * r0], events=ev, rtol=1e-10, atol=1e-14, max_step=1e-4)
            ts.append((sol.t_events[0][0] - ti) * L.TU if len(sol.t_events[0]) else float('nan'))
        out.append(f'{f:9s} log M_b {lM:5g}: centre reached after {ts[0]:.4f} / {ts[1]:.4f} / {ts[2]:.4f} Gyr (r0 0.001 / 0.01 / 0.1 kpc)')
out.append('\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.')
open(os.path.join(HERE, 'col1_focus_check.out'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
