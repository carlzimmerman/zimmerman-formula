#!/usr/bin/env python3
"""Momentum constraint and shift charge of a homogeneous finite-gradient ansatz.

Same fixed EH+P-V+sW+gamma X Box chi action, constant gamma. No new
constitutive functions, matter components, fitted roots, or background solver.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import numpy as np
import sympy as sy

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parent
ROOT=REPAIR.parents[2]


@lru_cache(maxsize=1)
def geometry():
    t=sy.symbols('t',real=True)
    a=[sy.Function(name)(t) for name in ['ax','ay','az']]
    g=sy.diag(-1,*(x*x for x in a));inverse=g.inv()
    def partial(expr,index):return sy.diff(expr,t) if index==0 else sy.S.Zero
    @lru_cache(maxsize=None)
    def connection(i,j,k):
        return sy.simplify(sum(inverse[i,l]*(partial(g[l,k],j)+partial(g[l,j],k)-partial(g[j,k],l))
                               for l in range(4))/2)
    ricci=sy.zeros(4)
    for i in range(4):
        for j in range(4):
            ricci[i,j]=sy.simplify(sum(partial(connection(k,i,j),k)-partial(connection(k,i,k),j)
                +sum(connection(k,i,j)*connection(l,k,l)-connection(l,i,k)*connection(k,j,l)
                     for l in range(4)) for k in range(4)))
    scalar=sy.simplify(sum(inverse[i,j]*ricci[i,j] for i in range(4) for j in range(4)))
    einstein=(ricci-g*scalar/2).applyfunc(sy.simplify)
    expected00=sum(sy.diff(a[i],t)/a[i]*sy.diff(a[j],t)/a[j] for i,j in [(0,1),(0,2),(1,2)])
    rho,p=sy.symbols('rho p',real=True)
    u=sy.Matrix([-1,0,0,0])
    ordinary=(rho+p)*(u*u.T)+p*g
    checks=dict(all_geometry_momentum_components_zero=all(einstein[0,i]==0 for i in [1,2,3]),
                hamiltonian_component=sy.simplify(einstein[0,0]-expected00)==0,
                comoving_perfect_fluid_momentum_zero=all(ordinary[0,i]==0 for i in [1,2,3]))
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,Einstein_0x=str(einstein[0,1]),Einstein_00=str(einstein[0,0]),
                Ricci_0x=str(ricci[0,1]),nonzero_christoffels=sum(connection(i,j,k)!=0
                    for i in range(4) for j in range(4) for k in range(4)))


@lru_cache(maxsize=1)
def derive():
    A,B,C,s0=sy.symbols('A B C s0',positive=True)
    Q,Qd,Qdd,b,gamma=sy.symbols('Q Qd Qdd b gamma',real=True)
    Hx,Hy,Hz,Hxd,Hyd,Hzd=sy.symbols('Hx Hy Hz Hxd Hyd Hzd',real=True)
    P,PX,PXd,V,W,WY,Xstar=sy.symbols('P PX PXd V W WY Xstar',real=True)
    shift,shiftd,lapsejet,lapsejetd=sy.symbols('shift shiftd lapsejet lapsejetd',real=True)
    theta=Hx+Hy+Hz;vol=A*B*C;Y=b*b/A**2;X=Q*Q-Y
    rates={A:A*Hx,B:B*Hy,C:C*Hz,Q:Qd,Qd:Qdd,Hx:Hxd,Hy:Hyd,Hz:Hzd,
           shift:shiftd,lapsejet:lapsejetd,PX:PXd}
    def dt(expr):return sy.expand(sum(sy.diff(expr,z)*rate for z,rate in rates.items()))
    tau=sy.Matrix([s0,0,0,0]);chi=sy.Matrix([Q,b,0,0])
    inverse=sy.Matrix([[-1,shift,0,0],[shift,A**-2,0,0],[0,0,B**-2,0],[0,0,0,C**-2]])
    volume=1/sy.sqrt(-inverse.det())
    scalarX=-(chi.T*inverse*chi)[0]
    clocks=sy.sqrt(-(tau.T*inverse*tau)[0])
    projected=-scalarX+(tau.T*inverse*chi)[0]**2/clocks**2
    # Vary inverse g0x(t) and its time derivative before setting the shift to zero.
    ordinary_density=volume*(P+PX*(scalarX-X)-V+clocks*(W+WY*(projected-Y)))
    box=dt(volume*(inverse[0,0]*Q+inverse[0,1]*b))/volume
    cubic_density=sy.factor(volume*gamma*scalarX*box)
    background={shift:0,shiftd:0}
    ordinary_flux=sy.simplify(-sy.diff(ordinary_density,shift).subs(background)/vol)
    cubic_shift_first=sy.simplify(sy.diff(cubic_density,shift).subs(background))
    cubic_shift_derivative=sy.simplify(sy.diff(cubic_density,shiftd).subs(background))
    # Symmetric off-diagonal metric variation gives delta S=-vol*T0x*delta g0x.
    cubic_flux=sy.simplify(-(cubic_shift_first-dt(cubic_shift_derivative))/vol)
    flux=sy.factor(ordinary_flux+cubic_flux)
    expected_flux=2*b*(PX*Q-gamma*theta*Q**2+gamma*Hx*Y)

    # Independently vary inverse g00(t) to audit the cubic energy sign.
    lapse_inverse=sy.diag(-1+lapsejet,A**-2,B**-2,C**-2)
    lapse_volume=1/sy.sqrt(-lapse_inverse.det())
    lapse_X=-(chi.T*lapse_inverse*chi)[0]
    lapse_box=dt(lapse_volume*lapse_inverse[0,0]*Q)/lapse_volume
    lapse_density=gamma*lapse_volume*lapse_X*lapse_box
    zeros={lapsejet:0,lapsejetd:0}
    lapse_first=sy.simplify(sy.diff(lapse_density,lapsejet).subs(zeros))
    lapse_derivative=sy.simplify(sy.diff(lapse_density,lapsejetd).subs(zeros))
    cubic_energy=sy.simplify(-2*(lapse_first-dt(lapse_derivative))/vol)

    # Generalized momentum for the cyclic scalar C(t), including its second derivative.
    raw=vol*(P+PX*(X-Xstar)-V+s0*W+gamma*X*(-Qd-theta*Q))
    current_density=sy.simplify(sy.diff(raw,Q)-dt(sy.diff(raw,Qd)))
    current=sy.factor(current_density/vol)
    scalar_euler=sy.simplify(-dt(sy.diff(raw,Q))+dt(dt(sy.diff(raw,Qd))))
    energy=2*PX*Q**2-P+V+cubic_energy

    # An independent integration by parts of the cubic homogeneous density.
    boundary=vol*gamma*(-Q**3/sy.Integer(3)+Q*Y)
    integrated_cubic=vol*gamma*(-sy.Rational(2,3)*Q**3*theta+2*Q*Hx*Y)
    raw_cubic=vol*gamma*X*(-Qd-theta*Q)
    checks=dict(gamma0_metric_flux=sy.simplify(ordinary_flux-2*PX*Q*b)==0,
                cubic_metric_flux=sy.simplify(cubic_flux-2*gamma*b*(Hx*Y-theta*Q**2))==0,
                total_flux=sy.simplify(flux-expected_flux)==0,
                flux_equals_gradient_times_shift_current=sy.simplify(flux-b*current)==0,
                scalar_Euler_is_charge_conservation=sy.simplify(scalar_euler+dt(current_density))==0,
                cubic_energy_sign_and_Y_term=sy.simplify(cubic_energy-2*gamma*Q*(Hx*Y-theta*Q**2))==0,
                energy_current_identity=sy.simplify(energy-(Q*current-P+V))==0,
                independent_cubic_integration_by_parts=sy.simplify(raw_cubic-integrated_cubic-dt(boundary))==0,
                projected_gradient_redshifts=sy.simplify(dt(Y)+2*Hx*Y)==0,
                isotropic_zero_gradient_energy=sy.simplify(cubic_energy.subs({b:0,Hy:Hx,Hz:Hx})+6*gamma*Hx*Q**3)==0)
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,gamma0_T0x=str(ordinary_flux),cubic_T0x=str(cubic_flux),
                full_T0x=str(flux),shift_current=str(current),cubic_T00=str(cubic_energy),
                total_T00=str(energy),current_density=str(current_density),
                cubic_action_boundary_term=str(boundary),
                homogeneous_cubic_density_up_to_boundary=str(integrated_cubic),
                cancellation='PX*Q = gamma*(theta*Q^2-Hx*Y), where theta=Hx+Hy+Hz',
                zero_charge_necessity='b!=0 and G0x=0 and ordinary T0x=0 imply Jchi=0 and conserved volume*Jchi=0')


def numerical():
    path=REPAIR/'l192_stress_audit_2026/stress_audit.py'
    spec=importlib.util.spec_from_file_location('background_frozen_coefficients',path)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    archive=json.loads((REPAIR/'cosmological_bridge_2026/radiation_002/result.json').read_text())
    roots=json.loads((ROOT/'fable_independent_2026/L192_results.json').read_text())
    samples=archive['samples'][::23]+[archive['samples'][-1]]
    coeff=helper.Coefficients(archive['parameters']['coefficient_efolds'])
    gamma=archive['parameters']['gamma'];rows=[];charge_errors=[]
    for smp,old in zip(samples,roots):
        if abs(smp['a']-old['a'])>1e-12:raise ValueError('source sample mismatch')
        c=coeff.at(float(smp['tau']));Q=smp['q'];H=smp['H'];a=smp['a']
        def jets(Y,g):
            return dict(zip(coeff.names,coeff.jets(*c['raw'],Q*Q-Y,Y,g)))
        zero=jets(0.,gamma)
        initial_current=2*zero['P_X']*Q-6*gamma*H*Q*Q
        reproduced_charge=a**3*initial_current
        charge_errors.append(abs(reproduced_charge-smp['scalar_charge']))
        if old['Yt']<=0:continue
        Y=old['Yt'];b=a*np.sqrt(Y)
        j=jets(Y,gamma);j0=jets(Y,0.)
        pflux=2*b*j['P_X']*Q
        cubic=2*gamma*b*(H*Y-3*H*Q*Q)
        full=pflux+cubic
        required_H=j['P_X']*Q/(gamma*(3*Q*Q-Y))
        zero_charge_energy=j['V']-j['P']
        hamiltonian_rhs=zero_charge_energy+smp['rho_baryon']+smp['rho_radiation']+.7
        rows.append(dict(a=a,Q=Q,qbar=float(c['qbar']),H=H,Y=Y,b_comoving=float(b),gamma=gamma,
            PX_full=float(j['P_X']),PX_gamma0=float(j0['P_X']),
            T0x_gamma0=float(2*b*j0['P_X']*Q),T0x_Ppart_full=float(pflux),
            T0x_cubic=float(cubic),T0x_total=float(full),
            cubic_over_P_flux=float(cubic/pflux),total_over_P_flux=float(full/pflux),
            shift_current=float(full/b),formal_charge_at_this_distinct_gradient_point=float(a**3*full/b),
            archived_zero_gradient_conserved_charge=smp['scalar_charge'],
            reproduced_zero_gradient_charge=float(reproduced_charge),
            required_isotropic_H_for_momentum_cancellation=float(required_H),
            required_H_over_source_H=float(required_H/H),
            zero_charge_energy=float(zero_charge_energy),
            isotropic_hamiltonian_LHS_at_required_H=float(3*required_H**2),
            isotropic_hamiltonian_RHS_at_frozen_state=float(hamiltonian_rhs),
            isotropic_hamiltonian_LHS_over_RHS=float(3*required_H**2/hamiltonian_rhs),
            inherited_state_fails_momentum=bool(abs(full/pflux)>.9)))
    if max(charge_errors)>1e-10:raise AssertionError('fixed action current does not reproduce archived charge')
    return dict(rows=rows,maximum_archived_charge_reproduction_error=float(max(charge_errors)),
                minimum_archived_charge=float(min(s['scalar_charge'] for s in samples)),
                all_tested_inherited_states_fail_momentum=all(r['inherited_state_fails_momentum'] for r in rows),
                scope='Five pointwise finite-gradient tests using physical Q and original Yt, full fixed gamma and frozen P reference. These are not a single finite-gradient trajectory.',
                warning='Required expansion rates are algebraic diagnostics, not a refit or a solved new branch. A zero-charge Bianchi-I branch is not excluded here.')


def run():
    geometry_result=geometry();action=derive();numbers=numerical()
    return dict(geometry=geometry_result,action=action,numerical=numbers,
       verdict=('The specified inherited nonzero-charge branch cannot be an exactly homogeneous diagonal-Bianchi-I finite-gradient solution with comoving ordinary matter; cubic cancellation requires the distinct zero-shift-charge branch.'
                if numbers['all_tested_inherited_states_fail_momentum'] else
                'The exact zero-charge necessity holds, but at least one sampled momentum test is unresolved.'),
       assumptions=['constant nonzero comoving gradient b','homogeneous tau(t) normal to the spatial slices',
                    'diagonal Bianchi-I metric in proper time','homogeneous coefficients depend on tau, not chi',
                    'constant gamma','no ordinary-matter momentum flux','finite nonzero spatial scale factors'],
       non_claims=['Not a universal no-go for finite gradients or locally uniform WKB patches',
                   'No exclusion or construction of all zero-charge coupled Bianchi-I branches',
                   'No full Einstein/scalar/clock evolution, attractor, CMB, or particle-DM completion',
                   'Tilted matter, a tilted clock, or spatially varying geometry/fields can change the momentum balance'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',required=True,type=Path);args=p.parse_args()
    result=run();args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=result['geometry'],exact_action_checks=result['action']['checks'],
                          verdict=result['verdict'],first_case=result['numerical']['rows'][0]),indent=2))
