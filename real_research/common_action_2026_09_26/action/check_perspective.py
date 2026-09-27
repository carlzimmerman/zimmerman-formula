#!/usr/bin/env python3
"""Exact action identities for the separately declared perspective carrier."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    checks = {}

    def exact(name, expr):
        residual = s.factor(s.simplify(expr))
        assert residual == 0, (name, residual)
        checks[name] = {'passed': True, 'residual': str(residual)}

    t, N, h, W = s.symbols('t N h W', positive=True)
    v, p, dt, dp = s.symbols('v p dt dp', real=True)
    z, eps = s.symbols('z epsilon', real=True)
    K = v*v/2
    L = t*K-W/t
    rho = t*K+W/t
    sigma = K+W/t**2
    exact('local_Z_source_equals_rho_over_t', s.diff(L, t)-rho/t)
    exact('source_differs_from_density_at_finite_t', sigma-rho-(1-t)*rho/t)
    exact('first_order_coupling_is_bare_energy', s.diff(L.subs(t, 1+z), z).subs(z, 0)-(K+W))
    exact('second_order_differs_from_exponential',
          s.diff(L.subs(t, 1+z), z, 2).subs(z, 0)-(-2*W))
    # Use qdot=N*v and p=Pi/sqrt(h); p=t*v exactly.
    vcanon = p/t
    H = p*vcanon-L.subs(v, vcanon)
    exact('Legendre_transform', H-(p*p/2+W)/t)
    exact('canonical_gate_source', -s.diff(H, t)-sigma.subs(v, vcanon))
    exact('canonical_density', rho.subs(v, vcanon)-H)
    exact('carrier_lapse_identity',
          N*L-N/t*((t*v)**2/2-W))
    # Fixed-h lapse derivative holds qdot and t fixed.
    qdot = s.symbols('qdot', real=True)
    LN = N*(t*qdot**2/(2*N**2)-W/t)
    exact('physical_lapse_density', -s.diff(LN, N)-rho.subs(v, qdot/N))
    Hvar = H.subs({p:p+eps*dp, t:t+eps*dt}, simultaneous=True)
    hess = s.diff(Hvar, eps, 2).subs(eps, 0)
    exact('joint_momentum_gate_Hessian_square',
          hess-((dp-p*dt/t)**2/t+2*W*dt**2/t**3))
    hh = s.hessian(H, (p, t))
    exact('local_Hessian_determinant', hh.det()-2*W/t**4)
    exact('zero_floor_Hessian_null_direction_control', hess.subs({W:0, dp:p*dt/t}))
    # Two h-volume cells: fixed canonical epsilon_i, N_i, volume weights.
    N1,N2,h1,h2,E1,E2,Z1,Z2 = s.symbols('N1 N2 h1 h2 E1 E2 Z1 Z2', positive=True)
    zm = (h1*Z1+h2*Z2)/(h1+h2)
    t1,t2 = 1+Z1-zm,1+Z2-zm
    HH = h1*N1*E1/t1+h2*N2*E2/t2
    sg1,sg2 = E1/t1**2,E2/t2**2
    msg = (h1*N1*sg1+h2*N2*sg2)/(h1+h2)
    exact('projected_canonical_Z_source', s.diff(HH,Z1)+h1*N1*(sg1-msg/N1))
    exact('projected_source_integral_zero', h1*N1*(sg1-msg/N1)+h2*N2*(sg2-msg/N2))
    exact('h_volume_mean_t_is_one', (h1*t1+h2*t2)/(h1+h2)-1)
    exact('homogeneous_t_is_one', t1.subs(Z2,Z1)-1)
    # Time-dependent oscillator: equation d(t*v)/dtime + V'/t=0.
    Vprime, tdot = s.symbols('Vprime tdot', real=True)
    vdot = -(tdot*v+Vprime/t)/t
    Edot = tdot*K+t*v*vdot+Vprime*v/t-W*tdot/t**2
    exact('energy_exchange_is_minus_tdot_sigma', Edot+tdot*sigma)
    V0 = s.symbols('V0', positive=True)
    exact('homogeneous_vacuum_floor_rho', rho.subs({t:1,v:0,W:V0})-V0)
    exact('homogeneous_vacuum_floor_pressure', L.subs({t:1,v:0,W:V0})+V0)
    floor_rho = V0/(1+z)
    floor_sigma = V0/(1+z)**2
    exact('vacuum_floor_density_susceptibility', s.diff(floor_rho,z).subs(z,0)+V0)
    exact('vacuum_floor_source_susceptibility', s.diff(floor_sigma,z).subs(z,0)+2*V0)
    exact('vacuum_floor_source_difference_survives_mean_subtraction',
          s.diff(floor_rho-floor_sigma,z).subs(z,0)-V0)
    out = {
        'claim_id':'CD26_4_PERSPECTIVE_CARRIER_VARIANT',
        'number_of_checks':len(checks), 'checks':checks,
        'scope':[
            'Separate action from exponential GNC; t=1+P_h Z>0',
            'Exact source sigma=rho/t, Legendre and projector identities',
            'Hessian positivity fixes carrier coordinates and their spatial gradients',
            'No full Dirac, global gravity evolution, or observational pass',
            'No numerical approximation or random sampling']}
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True},indent=2))


if __name__ == '__main__':
    main()
