"""Bounded exact-EOS TOV diagnostic; no full scalar-gradient/stability claim."""
import argparse
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

parser = argparse.ArgumentParser()
parser.add_argument('--contract', required=True)
parser.add_argument('--result', required=True)
args = parser.parse_args()
contract = json.loads(Path(args.contract).read_text())
p = contract['parameters']
m, G, u, rlam, lam = [float(p[k]) for k in ['m', 'G', 'u_star', 'r_lambda', 'lambda_total']]
Delta = 4*m*m*u*u
g = math.sqrt(lam*Delta/(1+rlam))
lrep = lam*rlam/(1+rlam)
zeta = u*u*rlam/(1+rlam)
Hcap = .5*math.log1p(zeta)
a = math.sqrt(lrep/(8*math.pi*G*m**4))
Mscale = zeta*a/G
checks = []

def check(name, passed, detail):
    checks.append(dict(name=name, passed=bool(passed), detail=detail))
    if not passed:
        raise AssertionError((name, detail))

def eos(t):
    if t <= 0:
        return (0., 0., 0., 0.)
    if not t < 1:
        raise ValueError('outside the stated coherent branch')
    delta = m*m*zeta*t
    D = Delta-4*delta
    A = g*g*rlam*(1-t)
    n = delta*D/(2*A)
    h = -g*delta/(2*A)
    S = n+4*h*h
    w2 = m*m+delta
    pressure = .5*delta*n
    energy = 2*w2*S-pressure
    charge = 2*math.sqrt(w2)*S
    nd = (D-4*delta)/(2*A)+2*lam*delta*D/(A*A)
    hd = -g/(2*A)-2*g*lam*delta/(A*A)
    Sd = nd+8*h*hd
    cs2 = S/(S+2*w2*Sd)
    return pressure, energy, charge, cs2

def run(tc, tol):
    hc = .5*math.log1p(zeta*tc)
    pc, ec, qc, csc = eos(tc)
    x0 = float(p['radial_start'])
    r0 = a*x0
    M0 = 4*math.pi*ec*r0**3/3
    Q0 = 4*math.pi*qc*r0**3/3
    H0 = hc-2*math.pi*G*(ec/3+pc)*r0*r0

    def rhs(x, v):
        Ms, ys, Qs = v
        H = Hcap*ys
        t = math.expm1(2*H)/zeta
        pressure, energy, charge, cs2 = eos(t)
        radius = a*x
        mass = Ms*Mscale
        den = 1-2*G*mass/radius
        if den <= 0:
            raise RuntimeError('horizon encountered')
        return [4*math.pi*a**3*x*x*energy/Mscale,
                -a*G*(mass+4*math.pi*radius**3*pressure)/(radius*radius*den*Hcap),
                4*math.pi*a**3*x*x*charge/(Mscale*math.sqrt(den))]

    def event(x, v):
        return v[1]
    event.terminal = True
    event.direction = -1
    sol = solve_ivp(rhs, (x0, float(p['radial_end'])),
                    [M0/Mscale, H0/Hcap, Q0/Mscale], rtol=tol,
                    atol=tol*float(p['absolute_tolerance_ratio']),
                    events=event, max_step=float(p['max_step']))
    if not sol.success or len(sol.t_events[0]) != 1:
        raise RuntimeError(sol.message)
    xs = float(sol.t_events[0][0])
    vs = sol.y_events[0][0]
    radius = a*xs
    mass = Mscale*float(vs[0])
    charge = Mscale*float(vs[2])
    compactness = G*mass/radius
    return dict(central_x=tc, radius=radius, mass=mass, charge=charge,
                compactness=compactness, energy_over_mQ=mass/(m*charge),
                central_enthalpy=hc, central_cs2=csc, nodes=len(sol.t))

rows = []
for tc in p['central_states']:
    low = run(float(tc), float(p['tolerances'][0]))
    high = run(float(tc), float(p['tolerances'][1]))
    resolution_change = max(abs(low[k]/high[k]-1) for k in ['radius', 'mass', 'charge'])
    check('resolution_'+str(tc), resolution_change < float(p['resolution_relative_gate']), resolution_change)
    check('sub_free_threshold_'+str(tc), high['energy_over_mQ'] < 1, high['energy_over_mQ'])
    own_bound = -math.expm1(-4*high['central_enthalpy'])/2
    check('central_enthalpy_bound_'+str(tc), high['compactness'] < own_bound, own_bound)
    cap_bound = .5*(1-(1+zeta)**-2)
    check('universal_cap_bound_'+str(tc), high['compactness'] < cap_bound, cap_bound)
    check('positive_subluminal_sound_'+str(tc), 0 < high['central_cs2'] < 1, high['central_cs2'])
    high['resolution_relative_change'] = resolution_change
    rows.append(high)

result = dict(status='completed', assertion_tested=contract['mathematics']['assertion_tested'],
              parameters=p, derived=dict(Delta=Delta,g=g,lambda_rep=lrep,zeta=zeta,
              Hcap=Hcap,length_a=a,mass_scale=Mscale,
              compactness_cap=.5*(1-(1+zeta)**-2)),
              software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
              rows=rows,checks=checks,
              non_claims=contract['mathematics']['non_claims'])
Path(args.result).write_text(json.dumps(result, indent=2)+'\n')
print('Completed',len(rows),'central states,',len(checks),'checks; max resolution change',
      max(r['resolution_relative_change'] for r in rows))
