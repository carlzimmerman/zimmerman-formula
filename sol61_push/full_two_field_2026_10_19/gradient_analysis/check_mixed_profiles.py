"""Independent finite-profile stress/current checks; no spectral stability test."""
import argparse
import json
import math
from pathlib import Path

import numpy as np

p = argparse.ArgumentParser()
p.add_argument('--contract', required=True)
p.add_argument('--result', required=True)
args = p.parse_args()
contract = json.loads(Path(args.contract).read_text())
rows = []
checks = []


def check(name, condition, value):
    checks.append(dict(name=name, passed=bool(condition), value=float(value)))
    if not condition:
        raise AssertionError((name, value))


for item in contract['profiles']:
    d = np.load(item['path'])
    r = d['r']
    if item['kind'] == 'pureX':
        G = 1/(4*math.pi)
        M = 1.
        m = M/(2*math.sqrt(1+item['u_star']**2))
        lam = item['lambda_total']
        g = math.sqrt(lam*(M*M-4*m*m)/(1+item['r_lambda']))
        f = np.zeros_like(r)
        fp = np.zeros_like(r)
        h, hp = d['h'], d['hp']
        U = d['mass_G']
        alpha = np.exp(d['logalpha'])
        omega = float(d['omega_X'])/2
    else:
        G, m, M, lam, g = [float(d[k]) for k in ['G', 'm', 'M', 'lambda_total', 'g']]
        f, fp, h, hp = [d[k] for k in ['f', 'fp', 'h', 'hp']]
        U = d['U'] if 'U' in d else d['v']/math.sqrt(G)
        alpha, omega = d['alpha'], float(d['omega'])
    N = 1-2*np.divide(U, r, out=np.zeros_like(U), where=r > 0)
    local_omega = omega/alpha
    T = local_omega**2*(f*f+4*h*h)
    K = N*(fp*fp+hp*hp)
    V = m*m*f*f+M*M*h*h-2*g*h*f*f+lam*f**4
    rho, pr, pt = T+K+V, T+K-V, T-K-V
    q = 2*local_omega*(f*f+4*h*h)
    mass_integral = 4*math.pi*G*np.trapz(r*r*rho, r)
    mass_rel = abs(mass_integral/U[-1]-1)
    Q = 4*math.pi*np.trapz(r*r*q/np.sqrt(N), r)
    R99 = float(np.interp(.99*U[-1], U, r))
    C99 = float(U[-1]/R99)
    C_local_max = float(np.max(np.divide(U, r, out=np.zeros_like(U), where=r > 0)))
    zeta = item['u_star']**2*item['r_lambda']/(1+item['r_lambda'])
    cap = m*math.sqrt(1+zeta)
    tf_C_bound = .5*(1-(1+zeta)**(-2))
    scale = max(float(np.max(rho)), 1e-100)
    check(item['name']+'_mass_integral', mass_rel < 2e-5, mass_rel)
    check(item['name']+'_no_horizon', float(np.min(N)) > 0, np.min(N))
    check(item['name']+'_positive_V', float(np.min(V)) >= -1e-14*scale, np.min(V))
    check(item['name']+'_radial_pressure', float(np.min(pr)) >= -1e-12*scale, np.min(pr))
    check(item['name']+'_anisotropy', float(np.max(pt-pr)) <= 1e-12*scale, np.max(pt-pr))
    check(item['name']+'_three_rho', float(np.max(pr+2*pt-3*rho)) <= 1e-12*scale, np.max(pr+2*pt-3*rho))
    check(item['name']+'_general_bound', C_local_max <= 24/49, C_local_max)
    if item['kind'] == 'pureX' or item.get('expect_cap_violation', False):
        check(item['name']+'_local_cap_extension_fails', local_omega[0] > cap, local_omega[0]/cap)
        check(item['name']+'_R99_extension_fails', C99 > tf_C_bound, C99/tf_C_bound)
    if item.get('positive_both_fields', False):
        check(item['name']+'_positive_f_grid', np.min(f) >= -1e-10*np.max(f), np.min(f))
        check(item['name']+'_positive_h_grid', np.min(h) >= -1e-10*np.max(h), np.min(h))
        check(item['name']+'_positive_f_center', f[0] > 0, f[0])
        check(item['name']+'_positive_h_center', h[0] > 0, h[0])
    rows.append(dict(name=item['name'], path=item['path'], G=G, m=m, M=M,
        lambda_total=lam, g=g, omega=omega, alpha0=float(alpha[0]),
        omega_local_center=float(local_omega[0]), TF_chemical_cap=cap,
        R99=R99, C99=C99, max_Gmass_over_r=C_local_max,
        TF_finite_surface_bound=tf_C_bound, ADM_over_mQ=float((U[-1]/G)/(m*Q)),
        mass_constraint_relative_quadrature_error=float(mass_rel),
        min_radial_pressure=float(np.min(pr))))

result = dict(assertion_tested=contract['mathematics']['assertion_tested'],
              rows=rows, checks=checks, non_claims=contract['mathematics']['non_claims'])
Path(args.result).write_text(json.dumps(result, indent=2)+'\n')
print('Checked', len(rows), 'saved profiles,', len(checks), 'finite assertions.')
