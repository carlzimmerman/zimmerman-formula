#!/usr/bin/env python3
"""PN28 finite algebra/ODE checks; analytical scope is in DERIVATION.md."""
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import quad, solve_ivp


def main():
    z, b, A, C, rr, c, theta = s.symbols('z b A C rho_ref c theta', positive=True)
    w = b-1
    p = A*z
    rho = rr*s.exp(z)
    forcing = (5*p-3*A)/2
    e = C*s.exp(b*z)-A*(5*z/(2*b)+5/(2*b*b)-3/(2*b))
    ev = C+5*p*p/(4*A)-3*p/2
    energy = rho*c*c+s.Rational(3,2)*p+e
    pressure = p+w*e
    checks = {}

    def exact(label, expr):
        checks[label] = s.simplify(expr) == 0

    exact('general_reservoir_ODE', s.diff(e,z)-b*e-forcing)
    exact('vacuum_reservoir_ODE', s.diff(ev,z)-forcing)
    exact('pressureless_special_case', e.subs(b,1)-(C*s.exp(z)-5*p/2-A))
    exact('radiation_special_case', e.subs(b,s.Rational(4,3))-
          (C*s.exp(s.Rational(4,3)*z)-s.Rational(15,8)*p-s.Rational(9,32)*A))
    exact('total_energy_balance', s.diff(energy,z)-(energy+pressure))
    exact('general_sound_numerator', s.diff(pressure,z)-(A+w*(b*e+forcing)))
    exact('general_sound_denominator', s.diff(energy,z)-(rho*c*c+5*p/2+b*e))
    ev_energy = rho*c*c+s.Rational(3,2)*p+ev
    ev_pressure = p-ev
    exact('vacuum_sound_speed', s.diff(ev_pressure,z)/s.diff(ev_energy,z)-
          5*(A-p)/(2*rho*c*c+5*p))
    exact('vacuum_pressure_gradient', s.diff(ev_pressure,z)/A-s.Rational(5,2)*(1-z))
    ae, net, da = s.symbols('A_eff net_transfer D_A_eff', real=True)
    dp = z*da-ae*theta
    moment = dp+s.Rational(5,3)*ae*z*theta-s.Rational(2,3)*net
    da_formula = (2*net-(5*ae*z-3*ae)*theta)/(3*z)
    exact('running_coefficient_identity', moment.subs(da,da_formula))

    rows=[]
    for wv in (-1.,0.,1/3):
        bv=1+wv
        for th in (-.2,.2):
            # Stay on a positive-pressure interval in both directions.
            av, cv, z0, rest_c2, tmax = 1., 25., 2., 1e6, 5.
            def state(zv):
                if bv == 0:
                    return cv+av*(1.25*zv*zv-1.5*zv)
                return cv*math.exp(bv*zv)-av*(2.5*zv/bv+2.5/(bv*bv)-1.5/bv)
            e0=state(z0)
            def rhs(t, y):
                zv, pp, ee, work = y
                q=(5*pp-3*av)*th/2
                volume=math.exp(th*t)
                return [-th,-av*th,-bv*ee*th-q,(pp+wv*ee)*th*volume]
            sol=solve_ivp(rhs,(0,tmax),[z0,av*z0,e0,0.],rtol=2e-11,atol=2e-12,
                          dense_output=True,max_step=.1)
            assert sol.success
            samples=np.linspace(0,tmax,41)
            errors=[]
            ledger=[]
            for tt in samples:
                zz, pp, ee, work=sol.sol(tt)
                errors.append(abs(ee-state(zz))/max(1.,abs(state(zz))))
                vol=math.exp(th*tt)
                # Rest energy is fixed and cancels from the finite cell ledger.
                ledger.append(abs((1.5*pp+ee)*vol+work-(1.5*av*z0+e0))/max(1.,e0))
            def analytic_work(tt):
                zz=z0-th*tt
                return (av*zz+wv*state(zz))*th*math.exp(th*tt)
            integral=quad(analytic_work,0,tmax,epsabs=1e-10,epsrel=1e-11)[0]
            rows.append({'w':wv,'theta':th,'samples':len(samples),
                         'max_state_relative_error':max(errors),
                         'max_work_ledger_scaled_error':max(ledger),
                         'work_vs_independent_quadrature':abs(sol.y[3,-1]-integral)/max(1.,abs(integral))})
    checks['six_finite_ODE_states'] = max(r['max_state_relative_error'] for r in rows)<1e-8
    checks['six_energy_work_ledgers'] = max(r['max_work_ledger_scaled_error'] for r in rows)<1e-8
    checks['six_independent_work_quadratures'] = max(r['work_vs_independent_quadrature'] for r in rows)<1e-8

    # A positive local reservoir reference value does not select A.
    freedom=[]
    for av in (.25,1.,4.):
        z0=2.
        target_e=100.
        cc=target_e-av*(1.25*z0*z0-1.5*z0)
        def ef(zz):
            return cc+av*(1.25*zz*zz-1.5*zz)
        freedom.append({'A':av,'reference_reservoir':ef(z0),
                        'min_on_tested_z_interval':min(ef(zz) for zz in np.linspace(1,3,41))})
    checks['three_A_same_reference_reservoir'] = all(r['reference_reservoir']==100. and
                                                  r['min_on_tested_z_interval']>0 for r in freedom)
    xc_values=(.01,.05,.1,.25)
    core=[{'x_c':xc,'p_c_over_A':-math.log(xc)+2/3,
           'vacuum_sound_numerator_over_A':5*(1+math.log(xc)-2/3)} for xc in xc_values]
    checks['four_MC27_centers_negative_sound_numerator'] = all(r['vacuum_sound_numerator_over_A']<0 for r in core)
    checks['threshold_agrees'] = abs((-math.log(math.exp(-1/3))+2/3)-1.)<1e-14
    checks={key:bool(value) for key,value in checks.items()}
    result={'claim_id':'PN28_RES','checks':checks,'symbolic_count':10,
            'trajectories':rows,'amplitude_freedom_examples':freedom,'MC27_centers':core,
            'x_threshold':math.exp(-1/3),
            'non_claims':['No particle-level model or selected amplitude',
                          'No universal interacting-vacuum instability',
                          'No kinetic PDE existence or global stability result']}
    assert all(checks.values()), checks
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':checks,'max_state_error':max(r['max_state_relative_error'] for r in rows),
                      'max_ledger_error':max(r['max_work_ledger_scaled_error'] for r in rows)},indent=2))


if __name__=='__main__':
    main()
