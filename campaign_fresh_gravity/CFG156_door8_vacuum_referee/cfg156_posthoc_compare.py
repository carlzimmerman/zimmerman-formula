#!/usr/bin/env python3
"""
CFG156 POST-HOC comparison (not frozen). Written AFTER both frozen runs of cfg156_referee.py and AFTER reading CFG131's
Dcommon.py, D3_linear_growth.py/.out and D1_covariant_constraint_and_target.out. It changes no pass line and is not
part of the headline.

Question: CFG156's z = 0 bounds agree with CFG131's D3 to <= 0.3%, but its z = 10 bounds are ~1% lower. CFG131's background
(Dcommon.py) adds radiation, Omega_r = 9.1e-5, while keeping Omega_L = 0.685 (E^2(a=1) = 1.000091). CFG156's main reading
has no radiation, and its declared R-rad row (flat, Omega_r = 9.2e-5) was run at z = 0, k = 30 only. Is the ~1% at z = 10 the
radiation convention?

Method: CFG156's own solver and bound search (imported from cfg156_referee.py, unmutated) on CFG131's background, all four k
at z = 0 and z = 10, against the numbers CFG131's D3 printed (3 significant figures; its brentq xtol is 1e-4 in log10).
No MUTATE: this is a diagnostic with no pass line.

  python3 cfg156_posthoc_compare.py  -> cfg156_posthoc_compare.out
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import cfg156_referee as R   # noqa: E402  (CFG156's own module; its main() does not run on import)

D3_PRINTED = {'z0': {0.5: 1.66e-08, 2.0: 1.04e-09, 10.0: 4.15e-11, 30.0: 4.61e-12},
              'z10': {0.5: 1.53e-07, 2.0: 9.56e-09, 10.0: 3.82e-10, 30.0: 4.25e-11}}

LINES = []


def P(s=''):
    print(s, flush=True)
    LINES.append(s)


def main():
    P('CFG156 POST-HOC comparison (after the frozen runs and after reading CFG131 Dcommon.py / D3 / D1); no pass line')
    cos_main = R.cosmology()
    cos_131 = {'H0': R.H0_KMS, 'h0c': R.H0_KMS/(R.C_LIGHT/1e3), 'om_c': 0.265, 'om_b': 0.050, 'om_r': 9.1e-5,
               'om_l': 0.685}
    P(f"CFG131 background: Omega_c 0.265, Omega_b 0.050, Omega_r 9.1e-5, Omega_L 0.685 (E^2(1) = "
      f"{0.265 + 0.050 + 9.1e-5 + 0.685:.6f}); CFG156 main: Omega_r = 0, Omega_L = {cos_main['om_l']:.3f}")
    P()
    P(f"{'':>10} {'k':>5} {'CFG156 main':>12} {'CFG156 on CFG131 bg':>20} {'CFG131 D3':>10} {'main/D3':>8} {'131bg/D3':>9}")
    worst_main, worst_131 = 0.0, 0.0
    for zlab, zev in (('z0', 0.0), ('z10', 10.0)):
        for k in R.KS:
            b_main = R.bound(k, cos_main, zev, pfac=1.0)
            b_131 = R.bound(k, cos_131, zev, pfac=1.0)
            d3 = D3_PRINTED[zlab][k]
            worst_main = max(worst_main, abs(b_main/d3 - 1.0))
            worst_131 = max(worst_131, abs(b_131/d3 - 1.0))
            P(f"{('z = 0' if zev == 0 else 'z = 10'):>10} {k:5.1f} {b_main:12.4e} {b_131:20.4e} {d3:10.2e} "
              f"{b_main/d3:8.4f} {b_131/d3:9.4f}")
    P()
    P(f'largest |ratio - 1| against CFG131 D3: CFG156 main reading {worst_main:.2%}; CFG156 solver on CFG131\'s background '
      f'{worst_131:.2%} (D3 prints 3 significant figures, so ~0.3% is its rounding)')
    P('reading: if the second number is at the rounding level, the residual ~1% at z = 10 is the radiation convention, not a '
      'solver difference.')
    with open(os.path.join(HERE, 'cfg156_posthoc_compare.out'), 'w') as fh:
        fh.write('\n'.join(LINES) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
