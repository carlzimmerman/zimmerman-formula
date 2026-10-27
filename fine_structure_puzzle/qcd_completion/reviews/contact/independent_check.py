"""Independent bounded response checks, without importing the target code."""
import argparse
import json
import platform
from pathlib import Path
import mpmath as mp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    mp.mp.dps = 60
    checks = []
    rows = []

    def check(name, error, bound):
        ok = bool(error < bound)
        checks.append({'name': name, 'passed': ok,
                       'error': mp.nstr(error, 20), 'bound': str(bound)})
        if not ok:
            raise AssertionError(name)

    chi = mp.mpf('1.7')
    mu = mp.mpf('1.2')
    fs = mp.mpf('0.9')
    q = 2*mp.pi*mp.sqrt(chi)
    for volume in map(mp.mpf, ('0.1', '1', '3')):
        for theta in (mp.mpf(0), mp.mpf('0.8'), mp.pi):
            def flux(v):
                return q/(mp.sqrt(2*mp.pi)*mu**4*mp.sqrt(v))*mp.fsum(
                    mp.exp(-n*n/(2*chi*v))*mp.cos(n*theta)
                    for n in range(-120, 121))

            rho_diff = -mp.diff(lambda v: mp.log(flux(v)), volume)
            weights = [mp.exp(-chi*volume*(theta+2*mp.pi*k)**2/2)
                       for k in range(-60, 61)]
            rho_branch = mp.fsum(w*chi*(theta+2*mp.pi*k)**2/2
                                for k, w in zip(range(-60, 61), weights))/mp.fsum(weights)
            check('canonical flux derivative equals branch stress',
                  abs(rho_diff-rho_branch), mp.mpf('1e-45'))
            rows.append({'kind': 'topform', 'V': str(volume), 'theta': str(theta),
                         'rho': mp.nstr(rho_diff, 30)})

    grid = list(range(-24, 25, 2))

    def zero(v, b, theta):
        # y=sqrt(chi V)(theta+x) unfolds the compact branches once.
        return mu*fs/mp.sqrt(2*mp.pi*chi)*mp.quad(
            lambda y: mp.exp(-y*y/2-v*b*(1-mp.cos(y/mp.sqrt(chi*v)-theta))), grid)

    for volume in map(mp.mpf, ('0.3', '2', '7')):
        for b in map(mp.mpf, ('0', '0.4', '5')):
            for theta in map(mp.mpf, ('0', '0.8')):
                value = zero(volume, b, theta)
                if not b:
                    check('B=0 canonical compact partition is V and theta independent',
                          abs(value-mu*fs/mp.sqrt(chi)), mp.mpf('1e-45'))
                rho_diff = -mp.diff(lambda v: mp.log(zero(v, b, theta)), volume)

                def density(y):
                    x = y/mp.sqrt(chi*volume)-theta
                    return mp.exp(-y*y/2-volume*b*(1-mp.cos(x)))

                def energy(y):
                    x = y/mp.sqrt(chi*volume)-theta
                    return chi*(theta+x)**2/2+b*(1-mp.cos(x))

                den = mp.quad(density, grid)
                rho_moment = mp.quad(lambda y: energy(y)*density(y), grid)/den-1/(2*volume)
                check('compact canonical derivative equals energy minus measure term',
                      abs(rho_diff-rho_moment), mp.mpf('1e-40'))
                if not b:
                    check('B=0 canonical stress vanishes', abs(rho_diff), mp.mpf('1e-45'))
                    mass = mp.sqrt(chi)/fs
                    check('B=0 replacement of Gaussian zero mode is unity',
                          abs(value/(mu/mass)-1), mp.mpf('1e-45'))
                rows.append({'kind': 'singlet', 'V': str(volume), 'B': str(b),
                             'theta': str(theta), 'rho': mp.nstr(rho_diff, 30)})

    volume = mp.mpf(10000)
    theta = mp.mpf('0.8')
    ratio_fast = zero(volume, volume**(-2), theta)/zero(volume, volume**(-2), 0)
    ratio_slow = zero(volume, volume**(-mp.mpf('0.5')), theta)/zero(volume, volume**(-mp.mpf('0.5')), 0)
    check('B=V^-2 gives near-screened ratio at V=10000', 1-ratio_fast, mp.mpf('1e-4'))
    check('B=V^-1/2 suppresses ratio at V=10000', ratio_slow, mp.mpf('1e-10'))
    rows.append({'kind': 'joint_limit_paths', 'V': str(volume), 'theta': str(theta),
                 'B_fast': str(volume**(-2)), 'ratio_fast': mp.nstr(ratio_fast, 30),
                 'B_slow': str(volume**(-mp.mpf('0.5'))), 'ratio_slow': mp.nstr(ratio_slow, 30)})
    result = {'claim_id': 'FSP-004-CONTACT-INDEPENDENT',
              'assertion_tested': 'Finite canonical metric-derivative identities, exact B=0 screening controls, and two nonuniform theta-limit paths',
              'software': {'Python': platform.python_version(), 'mpmath': mp.__version__},
              'passed': all(c['passed'] for c in checks), 'checks': checks, 'rows': rows,
              'non_claims': ['No full QCD matching, no interval certification, no all-volume numerical proof',
                             'No physical alpha or linear-curvature QCD coefficient computed']}
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': result['passed'], 'check_count': len(checks)}))


if __name__ == '__main__':
    main()
