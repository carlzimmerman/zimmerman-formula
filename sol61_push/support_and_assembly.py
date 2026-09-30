#!/usr/bin/env python3
"""Bounded research checks; not a formation mechanism or a completed theory.

Run: python3 sol61_push/support_and_assembly.py --output sol61_push/support_results.json
Negative control: add --mutate-drop-centrifugal (must exit 1).
Dimensionless units G = M_b = a0 = 1; physical footings are explicit below.
No imports from the prior research code. No files written except --output.
"""
import argparse
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--mutate-drop-centrifugal', action='store_true')
    args = parser.parse_args()
    checks, numbers = [], {}

    def check(name, passed, detail):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
        print(f"{'PASS' if passed else 'FAIL'} {name}: {detail}")

    # R1: exact P2 phantom dictionary (analytically independent of CFG44).
    r, G, M, a0, rhob, b, bp = sp.symbols('r G M a0 rho_b b bp', positive=True)
    g = sp.sqrt(b*b + a0*b)
    gp = sp.diff(g, b) * (4*sp.pi*G*rhob - 2*b/r)
    rhoc = (2*g/r + gp)/(4*sp.pi*G) - rhob
    exact = a0*b/(4*sp.pi*G*r*g) + (b+a0/2-g)*rhob/g
    residual = sp.simplify(rhoc-exact)
    check('exact_extended_P2_density', residual == 0, str(residual))
    # The coefficient of rhob is nonnegative by (b+a0/2)^2-g^2=a0^2/4.
    check('extra_density_nonnegative', sp.simplify((b+a0/2)**2-g**2-a0*a0/4) == 0,
          'positive square-root branch; coefficient vanishes only as a0 -> 0 or rhob = 0')
    # Analytic diffuse/compact Plummer examples; numerical differentiation audit.
    target_rows = []
    grid = np.geomspace(0.03, 30, 301)
    for h in (0.1, 1.0, 3.0):
        mb = grid**3/(grid**2+h*h)**1.5
        mbp = 3*h*h*grid**2/(grid**2+h*h)**2.5
        rb = mbp/(4*np.pi*grid**2)
        gn = mb/grid**2
        gt = np.sqrt(gn*gn+gn)
        rho = gn/(4*np.pi*grid*gt)+(gn+0.5-gt)*rb/gt
        eps = 1e-5
        def mc_at(x):
            bn = x**3/(x*x+h*h)**1.5
            return np.sqrt(bn*bn+bn*x*x)-bn
        fd = (mc_at(grid*(1+eps))-mc_at(grid*(1-eps)))/(2*grid*eps)/(4*np.pi*grid**2)
        err = float(np.max(np.abs(fd/rho-1)))
        charge = 4*np.pi*grid**3*rho*gt/mb
        target_rows.append(dict(h_over_rM=h, max_derivative_relative_error=err,
                                charge_min=float(charge.min()), charge_max=float(charge.max())))
        check(f'Plummer_density_h={h}', err < 2e-6 and np.all(rho > 0), f'max FD error {err:.3g}')
    numbers['target_dictionary'] = target_rows
    check('charge_closure_is_not_exact_extended_P2', target_rows[-1]['charge_max'] > 1.5,
          f"diffuse Plummer max C/C_charge={target_rows[-1]['charge_max']:.6g}")

    # R2: anisotropic Jeans balance, no radial edge pressure.
    rho, gt = sp.symbols('rho g', positive=True)
    pr, pt = 0, rho*r*gt/2
    jeans = sp.simplify(0 + 2*(pr-pt)/r + rho*gt)
    check('circular_orbit_Jeans', jeans == 0, 'p_r=0, p_theta=p_phi=rho*r*g/2')

    # Ordered-shell action, including self-gravity, not frozen-field orbital stability.
    # U = sum_i[-G m_i(M_b + sum_{j<i}m_j + m_i/2)/r_i];
    # V_eff = U + sum_i m_i j_i^2/(2 r_i^2), for fixed ordering.
    mi, A, j2, R = sp.symbols('mi A j2 R', positive=True)
    effective = -G*mi*A/r + mi*j2/(2*r*r)
    eq = {r:R, j2:G*A*R}
    force_res = sp.simplify(sp.diff(effective,r).subs(eq))
    stiffness = sp.simplify(sp.diff(effective,r,2).subs(eq))
    check('action_equilibrium', force_res == 0, str(force_res))
    check('self_gravitating_shell_stiffness', sp.simplify(stiffness-G*mi*A/R**3) == 0,
          'diagonal Hessian G*m_i*A_i/R_i^3 > 0 within noncrossing sector')
    # Extended fixed baryons add the nonnegative enclosed-mass derivative.
    acc = j2/r**3-G*(A+sp.Function('Mb')(r))/r**2
    deriv = sp.diff(acc,r).subs({j2:G*(A+sp.Function('Mb')(r))*r,
                               sp.Derivative(sp.Function('Mb')(r),r):bp})
    check('extended_baryon_shell_frequency',
          sp.simplify(-deriv-G*(A+sp.Function('Mb')(r))/r**3-G*bp/r**2) == 0,
          'omega^2=G*(M_dark,enclosed+Mb)/r^3 + G*Mb_prime/r^2')

    # Independent nonlinear Hamiltonian orbit test with fixed Lagrangian mass.
    # Single-shell tests are exact decoupled shell equations until shell crossing.
    orbit_rows = []
    for radius in (0.1, 1.0, 3.0, 30.0):
        enclosed = math.sqrt(1+radius*radius)
        angular = enclosed*radius
        omega = math.sqrt(enclosed/radius**3)
        for amplitude in (1e-4, 1e-2):
            # z=r/R, tau=omega*t; z''=1/z^3-1/z^2.
            centrifugal = 0.0 if args.mutate_drop_centrifugal else 1.0
            def rhs(t,y):
                return [y[1], centrifugal/y[0]**3-1/y[0]**2]
            def guard(t,y):
                return y[0]-0.05
            guard.terminal = True
            guard.direction = -1
            tau = np.linspace(0, 20*np.pi, 4001)
            sol = solve_ivp(rhs,(tau[0],tau[-1]),[1+amplitude,0],t_eval=tau,
                            rtol=1e-11,atol=1e-13,events=guard,method='DOP853')
            z, v = sol.y
            energy = 0.5*v*v+0.5*centrifugal/z**2-1/z
            drift = float(np.max(np.abs(energy-energy[0])))
            extent = float(np.max(np.abs(z-1)))
            completed = len(sol.t)==len(tau)
            # Exact two turning points from the quadratic energy equation.
            e0 = 0.5/(1+amplitude)**2-1/(1+amplitude)
            pericentre = float(min(np.roots([e0,1,-0.5])))
            expected_extent = max(amplitude,1-pericentre)
            check(f'orbit_R={radius}_eps={amplitude}',
                  completed and abs(extent-expected_extent) < 1e-6 and drift < 1e-8,
                  f'completed={completed}, max displacement={extent:.6g}, energy drift={drift:.3g}')
            orbit_rows.append(dict(radius=radius, perturbation=amplitude, completed=completed,
                                   maximum_relative_displacement=extent, energy_drift=drift,
                                   omega_dimensionless=omega, j2_dimensionless=angular))
    numbers['orbits'] = orbit_rows
    # Deliberately distinct fixed-potential frequency includes rho_dark derivative.
    rr = np.geomspace(0.01,100,1001)
    mt = np.sqrt(1+rr*rr)
    lagrangian_omega2 = mt/rr**3
    frozen_omega2 = mt/rr**3 + 1/(rr*np.sqrt(1+rr*rr))
    check('fixed_potential_vs_self_gravitating_frequency',
          np.all(frozen_omega2 > lagrangian_omega2),
          'do not substitute fixed-potential epicyclic frequency for collective shell frequency')

    # Energy in point-mass target shell region [r_inner,R], with its inner source held.
    # -W = int g*r dMc = R-r_inner; K=0.5 int g*r dMc; U_active=-(R-r_inner).
    energy_rows=[]
    for Rval in (1,3,30,200):
        inner=1e-3
        wmag=quad(lambda x: math.sqrt(1+x*x)/x * x/math.sqrt(1+x*x),inner,Rval,
                  epsabs=1e-11)[0]
        K=0.5*wmag
        U=-wmag
        check(f'virial_energy_R={Rval}', abs(2*K+U) < 1e-12 and U < 0,
              f'K={K:.6g}, U={U:.6g}, 2K+U={2*K+U:.3g}, no radial boundary pressure')
        energy_rows.append(dict(R_over_rM=Rval,r_inner_over_rM=inner,K=K,U=U,
                                total_energy=K+U,K_over_baryon_reference=2*K))
    numbers['energy'] = energy_rows

    # Both currently used footings from CFG4/CFG118; historical values differ slightly.
    Gsi=6.67430e-11; Msun=1.98847e30; pc=3.0856775814913673e16
    footings=[]
    for label,a in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        for mbsol in (1e9,1e10,1e12):
            mass=mbsol*Msun
            rM=math.sqrt(Gsi*mass/a)
            vf2=math.sqrt(Gsi*mass*a)
            for x in (0.3,1,3,30):
                radius=x*rM
                total=mass*math.sqrt(1+x*x)
                omg2=Gsi*total/radius**3
                vt2=Gsi*total/radius
                footings.append(dict(footing=label,a0_si=a,Mb_Msun=mbsol,x=x,
                                     r_kpc=radius/(1e3*pc),v_kms=math.sqrt(vt2)/1000,
                                     radial_omega2_si=omg2,stress_over_rest_energy=vt2/299792458**2))
    check('two_footings_weak_field_scope', all(row['radial_omega2_si']>0 and
          row['stress_over_rest_energy']<1e-4 for row in footings),
          f'{len(footings)} physical cells, max stress/rest-energy={max(row["stress_over_rest_energy"] for row in footings):.3g}')
    numbers['physical_footings']=footings

    # R3: baryon growth, fixed mass label m, exact angular momentum conservation.
    m, Mb = sp.symbols('m Mb',positive=True)
    rt=sp.sqrt(G/a0)*sp.sqrt(m*m/Mb+2*m)
    jt2=G*(Mb+m)*rt
    dlog=sp.simplify(Mb*sp.diff(jt2,Mb)/jt2)
    wanted=Mb/(Mb+m)-m/(2*(m+2*Mb))
    check('required_target_angular_momentum_drift',sp.simplify(dlog-wanted)==0,
          'dln(j_target^2)/dlnMb = Mb/(Mb+m)-m/[2(m+2Mb)]')
    root=(1+math.sqrt(17))/2
    check('one_stationary_shell_not_a_profile', abs(1/(1+root)-root/(2*(root+2)))<1e-14,
          f'zero only at m/Mb={root:.12g}; cannot preserve a continuum')
    assembly=[]
    for q in (0.5,0.8,1.2,2.0):
        for z in (0.1,1.0,3.0,30.0):
            r_old=math.sqrt(z*z+2*z)
            j_old2=(1+z)*r_old
            r_new=j_old2/(q+z)
            g_new=(q+z)/r_new**2
            gn_new=q/r_new**2
            inferred=(g_new*g_new-gn_new*gn_new)/gn_new
            closed=(2*z+z*z/q)/(2*z+z*z)*((q+z)/(1+z))**2
            check(f'assembly_q={q}_m={z}',abs(inferred/closed-1)<1e-12,
                  f'a0_effective/a0={inferred:.8g}')
            assembly.append(dict(baryon_mass_factor=q,dark_mass_over_initial_Mb=z,
                                 radius_old=r_old,radius_new=r_new,a0_effective_ratio=inferred,
                                 torque_log_derivative_at_initial_Mb=1/(1+z)-z/(2*(z+2))))
    numbers['assembly']=assembly
    q2=[row['a0_effective_ratio'] for row in assembly if row['baryon_mass_factor']==2]
    check('pure_adiabatic_assembly_does_not_select_or_maintain_target', min(q2)<0.7 and max(q2)>3,
          f'factor-two growth: a0_eff spans {min(q2):.6g} to {max(q2):.6g}')
    # Gravity alone leaves each j unchanged in exact spherical symmetry.
    # No angular-momentum scalar in the action is permitted to be secretly target-slaved.
    numbers['selection_status']='OPEN: angular-momentum distribution and shell masses were chosen from the target'
    payload=dict(schema=1,checks=checks,numbers=numbers,
                 mutation='drop_centrifugal' if args.mutate_drop_centrifugal else None,
                 environment=dict(python=platform.python_version(),numpy=np.__version__,
                                  scipy=scipy.__version__,sympy=sp.__version__),
                 limitations=['Newtonian, spherical, fixed baryons for radial stability',
                              'No shell crossing; no nonradial or coupled baryon stability theorem',
                              'Target halo initialized; no formation/ownership/cosmology mechanism',
                              'Finite inner cutoff needed for relativistic point-mass application'])
    Path(args.output).write_text(json.dumps(payload,indent=2)+'\n')
    failed=sum(not item['passed'] for item in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; {failed} failures. Theory completion OPEN.')
    return int(failed>0)


if __name__=='__main__':
    raise SystemExit(main())
