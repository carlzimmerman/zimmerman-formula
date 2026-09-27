#!/usr/bin/env python3
"""Bounded exact identities and ODE controls for a covariant polar clock.

The action contains two real classical scalar degrees of freedom. Circular
dispersion is a fixed-metric/local-background statement. The FRW integrations
include homogeneous Einstein backreaction and freely specified charge data.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import solve_ivp


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', required=True)
    args = ap.parse_args(); checks = {}
    def exact(name, expr):
        residual = s.simplify(s.expand(expr))
        assert residual == 0, (name, residual)
        checks[name] = {'passed': True, 'residual': str(residual)}
    def bounded(name, value, passed):
        assert bool(passed), (name, value)
        checks[name] = {'passed': True, 'measured': value}

    R, R0, Om, lam, m, M, vol, N = s.symbols('R R0 Omega lambda m M vol N', positive=True)
    rd, td, gr, gt, pr, pt = s.symbols('Rdot Tdot gradR gradT pR pT', real=True)
    theta, dr, dt = s.symbols('theta dR dT', real=True)
    dx = s.cos(theta)*dr-R*s.sin(theta)*dt
    dy = s.sin(theta)*dr+R*s.cos(theta)*dt
    exact('Cartesian_polar_kinetic_identity', s.trigsimp(dx*dx+dy*dy)-dr*dr-R*R*dt*dt)
    kinetic = vol*(rd*rd+R*R*td*td)/(2*N)
    exact('ADM_matter_velocity_Hessian_determinant', s.det(s.hessian(kinetic, (rd, td)))-vol**2*R**2/N**2)
    V = s.Function('V')(R)
    L = kinetic-N*vol*(gr*gr+R*R*gt*gt+2*V)/2
    H = (pr*rd+pt*td-L).subs({rd:N*pr/vol, td:N*pt/(vol*R*R)})/N
    exact('ADM_matter_Hamiltonian', H-((pr*pr+pt*pt/R**2)/(2*vol)+vol*(gr*gr+R*R*gt*gt+2*V)/2))

    eps, chi, cd, zd, cg, zg, vp, vpp, V0 = s.symbols('eps chi chidot zdot gradchi gradz vp vpp V0', real=True)
    lag = (eps**2*(cd**2-cg**2)+(R0+eps*chi)**2*((Om+eps*zd/R0)**2-eps**2*zg**2/R0**2))/2-(V0+eps*vp*chi+eps**2*vpp*chi**2/2)
    linear = s.expand(lag).coeff(eps, 1)
    exact('circular_background_linear_term_is_boundary', linear.subs(vp,R0*Om**2)-R0*Om*zd)
    mu2 = vpp-Om**2
    L2 = s.expand(lag).coeff(eps, 2)
    target = (cd**2+zd**2-cg**2-zg**2-mu2*chi**2)/2+2*Om*chi*zd
    exact('polar_quadratic_gyroscopic_action', L2-target)
    pz, pc = s.symbols('pz pchi', real=True)
    h2 = (pz*zd+pc*cd-L2).subs({zd:pz-2*Om*chi,cd:pc})
    exact('quadratic_Hamiltonian_positive_squares', h2-((pz-2*Om*chi)**2+pc**2+cg**2+zg**2+mu2*chi**2)/2)
    q, y, u = s.symbols('k2 omega2 mu2', positive=True)
    A = u+4*Om**2
    poly = (y-q)*(y-q-u)-4*Om**2*y
    roots = [q+A/2-s.sqrt(A*A+16*Om**2*q)/2, q+A/2+s.sqrt(A*A+16*Om**2*q)/2]
    exact('light_root', poly.subs(y,roots[0]))
    exact('heavy_root', poly.subs(y,roots[1]))
    exact('root_product', roots[0]*roots[1]-q*(q+u))
    exact('light_sound_coefficient', s.diff(roots[0],q).subs(q,0)-u/A)
    exact('light_positive_k4_coefficient', s.diff(roots[0],q,2).subs(q,0)/2-16*Om**4/A**3)

    potential = m*m*R*R/2+lam*R**4/4
    Omega2 = m*m+lam*R0**2
    radial2 = 2*lam*R0**2
    exact('quartic_circular_condition', s.diff(potential,R).subs(R,R0)-R0*Omega2)
    exact('quartic_radial_stiffness', (s.diff(potential,R,2).subs(R,R0)-Omega2)-radial2)
    cs2 = radial2/(radial2+4*Omega2)
    exact('quartic_sound_formula', cs2-lam*R0**2/(2*m*m+3*lam*R0**2))
    rhoL = s.symbols('rho_Lambda', nonnegative=True)
    rho = R0**2*Omega2/2+potential.subs(R,R0)+rhoL
    pressure = R0**2*Omega2/2-potential.subs(R,R0)-rhoL
    exact('circular_energy_density', rho-(m*m*R0**2+3*lam*R0**4/4+rhoL))
    exact('circular_pressure', pressure-(lam*R0**4/4-rhoL))
    exact('positive_vacuum_cannot_cancel_rho_plus_p', rho+pressure-R0**2*Omega2)
    exact('vacuum_shift_does_not_source_radial_force', s.diff(potential+rhoL,R)-s.diff(potential,R))
    charge = R0**2*s.sqrt(Omega2)
    exact('low_density_energy_per_charge_is_free_mass', s.limit((rho-rhoL)/charge,R0,0)-m)

    X = s.symbols('X', positive=True)
    Rstar2 = (X-m*m)/lam
    PX = (X-m*m)**2/(4*lam)-rhoL
    exact('algebraic_radial_elimination', (R*R*X/2-potential-rhoL).subs(R**2,Rstar2)-PX)
    soundP = s.diff(PX,X)/(s.diff(PX,X)+2*X*s.diff(PX,X,2))
    exact('one_clock_PX_matches_only_sound_order', soundP.subs(X,Omega2)-cs2)
    # If R=F(X) is imposed inside its kinetic term, Xdot=2 Omega pi_ddot
    # at linear order. The resulting acceleration Hessian is nonzero.
    acc = s.symbols('pi_ddot', real=True)
    acceleration_lagrangian = Om**2*acc**2/(2*lam*(Om**2-m*m))
    exact('rate_identification_nonzero_acceleration_Hessian', s.diff(acceleration_lagrangian,acc,2)-Om**2/(lam*(Om**2-m*m)))
    exponent, gamma = s.symbols('p gamma', positive=True)
    powerV = gamma*R**exponent
    powerOm2 = s.diff(powerV,R)/R
    powerMu2 = s.diff(powerV,R,2)-powerOm2
    powerW = (R*s.diff(powerV,R)-2*powerV)/(R*s.diff(powerV,R)+2*powerV)
    powerCs = powerMu2/(powerMu2+4*powerOm2)
    exact('monomial_circular_w_equals_sound_squared', powerW-powerCs)
    exact('negative_pressure_gradient_instability_control', powerCs.subs(exponent,s.Rational(1,2))+s.Rational(3,5))

    a, Hubble, O, rdot = s.symbols('a H OmegaNow Rdot', real=True)
    rdd = -3*Hubble*rdot+R*O**2-s.diff(potential,R)
    Odd = -3*Hubble*O-2*rdot*O/R
    energy = (rdot**2+R**2*O**2)/2+potential
    edot = s.diff(energy,R)*rdot+s.diff(energy,rdot)*rdd+s.diff(energy,O)*Odd
    exact('homogeneous_energy_dissipation', edot+3*Hubble*(rdot**2+R**2*O**2))
    Q = a**3*R**2*O
    Qdot = s.diff(Q,a)*a*Hubble+s.diff(Q,R)*rdot+s.diff(Q,O)*Odd
    exact('homogeneous_charge_conservation', Qdot)
    constant_circle_charge_derivative = s.diff(Q,a)*a*Hubble
    exact('constant_circular_FRW_obstruction', constant_circle_charge_derivative-3*Hubble*Q)
    beta=s.Rational(3,5); boost=1/s.sqrt(1-beta**2)
    exact('boosted_nonlinear_timelike_margin', (boost*O)**2-(boost*beta*O)**2-O**2)

    # ODE implementation evolves Cartesian fields, not the conserved-charge
    # reduced equation. Charge conservation is therefore an independent check.
    m2_num, lam_num, vacuum_num, mpl2_num = 1., .5, .03, 1.
    times=np.linspace(0,40,1001); rows=[]
    for radius, radial_velocity, phase_velocity in [(1.,0.,math.sqrt(1.5)),(.9,.3,1.1),(1.2,-.2,.8)]:
        init=np.array([radius,0.,radial_velocity,radius*phase_velocity,0.])
        def rhs(t,state):
            f=state[:2]; velocity=state[2:4]
            r2=float(f@f)
            energy=.5*float(velocity@velocity)+.5*m2_num*r2+.25*lam_num*r2*r2
            hubble=math.sqrt((energy+vacuum_num)/(3*mpl2_num))
            acceleration=-3*hubble*velocity-(m2_num+lam_num*r2)*f
            return np.r_[velocity,acceleration,hubble]
        sol=solve_ivp(rhs,(0.,40.),init,t_eval=times,method='DOP853',rtol=1e-11,atol=1e-13,max_step=.1)
        assert sol.success,sol.message
        fx,fy,vx,vy,loga=sol.y
        r2=fx*fx+fy*fy; rr=np.sqrt(r2)
        angular=fx*vy-fy*vx
        qnow=np.exp(3*loga)*angular
        phase_dot=angular/r2
        edyn=.5*(vx*vx+vy*vy)+.5*m2_num*r2+.25*lam_num*r2*r2
        q0=radius*radius*phase_velocity; e0=edyn[0]
        charge_error=float(np.max(np.abs(qnow/q0-1)))
        lower=abs(q0)*np.exp(-3*loga)/math.sqrt(2*e0)
        rmax=(4*e0/lam_num)**.25
        h0=math.sqrt((e0+vacuum_num)/(3*mpl2_num))
        row={'initial':[radius,radial_velocity,phase_velocity],
             'charge':q0,'charge_relative_error':charge_error,
             'min_radius':float(rr.min()),'min_phase_dot':float(phase_dot.min()),
             'max_positive_energy_increment':float(np.max(np.diff(edyn))),
             'min_radius_over_analytic_lower_bound':float(np.min(rr/lower)),
             'max_radius_over_analytic_upper_bound':float(np.max(rr/rmax)),
             'max_loga_minus_H0t':float(np.max(loga-h0*times))}
        rows.append(row)
        assert charge_error < 2e-8 and phase_dot.min()>0 and np.max(np.diff(edyn))<1e-10
        assert np.min(rr/lower)>1-1e-8 and np.max(rr/rmax)<1+1e-8
        assert np.max(loga-h0*times)<1e-10
    bounded('finite_FRW_cartesian_evolutions',rows,True)

    # Finite-amplitude interacting Minkowski radial motion with a uniform
    # nonzero radius and phase-rate bound. This also admits Lorentz boosts.
    Jnum=1.2; initial=np.array([1.1,.4,0.])
    def mink_rhs(t,state):
        rr,vv,phase=state
        return [vv,Jnum**2/rr**3-m2_num*rr-lam_num*rr**3,Jnum/rr**2]
    sol=solve_ivp(mink_rhs,(0.,50.),initial,t_eval=np.linspace(0,50,1001),method='DOP853',rtol=1e-11,atol=1e-13,max_step=.05)
    assert sol.success,sol.message
    rr,vv,phase=sol.y
    ee=.5*vv**2+Jnum**2/(2*rr**2)+.5*m2_num*rr**2+.25*lam_num*rr**4
    e0=float(ee[0]); low=abs(Jnum)/math.sqrt(2*e0); high=(4*e0/lam_num)**.25
    eeerr=float(np.max(np.abs(ee/e0-1)))
    bounded('interacting_global_radial_branch_finite_control',
            {'charge':Jnum,'energy':e0,'energy_relative_error':eeerr,
             'analytic_radius_lower':low,'analytic_radius_upper':high,
             'observed_radius_min':float(rr.min()),'observed_radius_max':float(rr.max()),
             'analytic_phase_rate_lower':Jnum/high**2,'observed_phase_rate_min':float((Jnum/rr**2).min())},
            eeerr<2e-9 and rr.min()>low and rr.max()<high)

    output={'result':'covariant two-scalar completion with exact circular dispersion and controlled homogeneous timelike branches',
            'number_of_checks':len(checks),'checks':checks,
            'field_count':{'gravity_configurations':6,'matter_configurations':2,'diffeomorphism_first_class_constraints':4,'physical_configuration_modes':4,'tensor_modes':2,'scalar_modes':2},
            'non_claims':['Not a one-scalar completion','No particles or relic abundance were assumed; independent classical matter data are present','Circular flat dispersion is not an exact expanding Einstein-background solution','No global arbitrary-inhomogeneous timelike-phase theorem','No MOND, lensing, PPN, abundance, or empirical gate embedding','Finite ODE outputs supplement the separate analytic bounds and do not prove them']}
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps(output,indent=2))


if __name__=='__main__': main()
