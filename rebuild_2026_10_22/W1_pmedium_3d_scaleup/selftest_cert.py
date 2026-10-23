#!/usr/bin/env python3
"""Certificate self-test C-S1 (FROZEN_CRITERIA.md section 6): unperturbed lattice (amp = 0), pure Hubble flow, A = 1, n = 32,
aperture of comoving radius box/4. EdS is critical, so K + U = 0 for a uniform Hubble sphere; PASS iff |K + U| <= 0.10 K
(also reports that the vacuum field energy is zero to roundoff). --mutate drops the Hubble term from the velocities and must FAIL.
Run: /usr/bin/python3 selftest_cert.py [--mutate]. Writes selftest_cert.json (or selftest_cert_MUTATE.json)."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'engine'))
import pmedium3d as E  # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mutate', action='store_true'); a = ap.parse_args()
    out = dict(criteria='FROZEN_CRITERIA.md 6 C-S1' + (' MUTATE (no Hubble term)' if a.mutate else ''), footings={})
    for footing in ('canonical', 'alt'):
        m = E.Model(32, 0.0, 1100, footing)
        xc = m.x0.copy(); xb = xc.copy(); pc = m.Hi * m.disp.copy(); pb = pc.copy()
        P, c, res = m.fields(xc); Q = np.zeros_like(P); V = np.zeros_like(c); A = 1.
        F = m.forces(xc, xb, P, c, A)
        R_kpc = m.box / 4 * m.ell * 1000 * A
        cr = m.certificate(F, A, m.Hi, xc, xb, P, c, pc, pb, Q, V, hubble=not a.mutate, apertures_kpc=(R_kpc,), centre_kpc=R_kpc)
        ap_ = cr['apertures'][0]
        K, U = ap_['K'], ap_['U']
        # analytic uniform Hubble sphere with the same enclosed mass, for reference
        M = ap_['N_c'] * m.mc + ap_['N_b'] * m.mb; R = m.box / 4
        rec = dict(R_kpc=R_kpc, N_c=ap_['N_c'], N_b=ap_['N_b'], K=K, U=U, K_plus_U_over_K=(K + U) / K if K else None,
                   K_analytic=.3 * M * m.Hi ** 2 * R ** 2, U_analytic=-.6 * M ** 2 / R, E_field=ap_['E_field'],
                   max_abs_force=float(max(np.max(np.abs(F[k])) for k in ('fc', 'fb', 'fP', 'fchi'))))
        rec['passed'] = bool(K > 0 and abs(K + U) <= .10 * K)  # frozen C-S1 rule
        rec['vacuum_field_energy_roundoff_ok'] = bool(abs(ap_['E_field']) <= 1e-12 * K)  # extra: vacuum fields are zero up to deposit roundoff
        out['footings'][footing] = rec
    allp = all(v['passed'] for v in out['footings'].values())
    out['C_S1'] = allp
    if a.mutate:
        out['verdict'] = 'C-S1m PASS (mutation fails the self-test)' if not allp else 'C-S1m FAIL (mutation not caught)'
    else:
        out['verdict'] = 'C-S1 PASS' if allp else 'C-S1 FAIL'
    (HERE / ('selftest_cert_MUTATE.json' if a.mutate else 'selftest_cert.json')).write_text(json.dumps(out, indent=1) + '\n')
    print(out['verdict'], json.dumps(out['footings'], indent=1))


if __name__ == '__main__':
    main()
