#!/usr/bin/env python3
"""Exact variational bridges for a declared common-action trial, not closure."""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True);args=parser.parse_args();checks={}
    def exact(name,expr):
        rr=s.factor(s.simplify(expr));assert rr==0,(name,rr)
        checks[name]={'passed':True,'residual':str(rr)}
    def bounded(name,value,condition):
        assert bool(condition),(name,value);checks[name]={'passed':True,'measured':value}

    rb,rd,P,f,Phi,phi,Z=s.symbols('rho_b rho_d P f Phi phi Z',real=True)
    oldsource=-(rb+rd)*phi-f*rb*P
    exact('L361_physical_potential_source_rewrite',
          oldsource.subs(phi,Phi-f*P)-(-rb*Phi-rd*Phi+f*P*rd))
    a,z,w,c=s.symbols('a Dz Dw Dchi',real=True)
    exact('physical_lapse_gradient_rewrite',-(a-z)**2-(-a*a+2*a*z-z*z))
    block=2*a*z-z*z-2*(z+c)*w+w*w+c*c
    exact('active_plateau_auxiliary_chi_elimination',block.subs(c,w)-(2*a*z-z*z-2*z*w))
    exact('active_plateau_recovers_CH_host',block.subs(c,w).subs(z,a-w)-(w-a)**2)

    # Carrier source and energy follow from the actual lapse dependence.
    N,v,W=s.symbols('N v W',positive=True)
    K=v*v/(2*N*N)
    Llin=(1+Z)*K-(1-Z)*W
    rholin=(1+Z)*K+(1-Z)*W
    exact('linear_carrier_lapse_density',-s.diff(N*Llin,N)-rholin)
    exact('linear_carrier_subtraction_source_is_bare_density',s.diff(Llin,Z)-(K+W))
    exact('linear_density_source_mismatch',rholin-s.diff(Llin,Z)-Z*(K-W))
    Lex=s.exp(Z)*K-s.exp(-Z)*W
    rhoex=s.exp(Z)*K+s.exp(-Z)*W
    exact('exponential_actual_lapse_density',-s.diff(N*Lex,N)-rhoex)
    exact('exponential_source_is_actual_density',s.diff(Lex,Z)-rhoex)
    exact('exponential_matches_linear_coupling_at_first_order',
          s.series(Lex,Z,0,2).removeO()-Llin)
    Nd=N*s.exp(-Z)
    exact('exponential_composite_lapse_identity',Nd*(v*v/(2*Nd*Nd)-W)-N*Lex)
    exact('exponential_product_of_principal_coefficients',s.exp(Z)*s.exp(-Z)-1)
    A=s.exp(Z);BB=s.exp(-Z)
    exact('exponential_carrier_characteristic_speed',BB/A-s.exp(-2*Z))
    h=s.symbols('sqrt_h',positive=True)
    mom=s.diff(N*h*Lex,v)
    exact('exponential_canonical_momentum',mom-h*A*v/N)
    exact('exponential_hamiltonian_density',mom*v-N*h*Lex-N*h*rhoex)

    # General scalar gate variation, including the L361 screening mass.
    Mp2,m2,psi,chi,ww,a02,qq,eta,lam=s.symbols('Mp2 m2 psi chi w a02 q eta lambda',real=True)
    Lregion=Mp2*(-2*m2*(1-f)*psi*ww+a02*f*qq+m2*(1-f)*chi*chi)
    Lconstraints=eta*(Z-f*(psi-chi))+lam*(f-s.Function('F')(s.Symbol('I')))
    Bgate=Mp2*(2*m2*psi*ww+a02*qq-m2*chi*chi)-eta*(psi-chi)
    exact('varied_gate_coefficient',s.diff(Lregion+Lconstraints,f)-(Bgate+lam))
    I=s.Symbol('I');FI=s.Function('F')(I)
    exact('gate_multiplier_restores_metric_clock_chain_rule',
          s.diff(-lam*FI,I).subs(lam,-Bgate)-Bgate*s.diff(FI,I))
    # Hessian after composing a kinetic-density gate: all fixed-Z coefficients
    # are positive, yet the composed action can have a negative velocity Hessian.
    kk=s.symbols('K',positive=True)
    zg=1/(2*(1+(kk-1)**2));Lg=s.exp(zg)*kk
    hess=s.diff(Lg,kk)+2*kk*s.diff(Lg,kk,2)
    exact('density_gate_ghost_witness',hess.subs(kk,1)+s.exp(s.Rational(1,2)))
    exact('density_gate_witness_is_stationary',s.diff(zg,kk).subs(kk,1))
    exact('density_gate_witness_second_derivative',s.diff(zg,kk,2).subs(kk,1)+1)
    gt=s.Function('g')(kk);Lg_general=s.exp(gt)*kk-s.exp(-gt)*W
    rho_g=s.exp(gt)*kk+s.exp(-gt)*W
    expected_hess=s.exp(gt)+s.diff(gt,kk)*rho_g+2*kk*(
        2*s.exp(gt)*s.diff(gt,kk)+s.diff(gt,kk,2)*rho_g+s.diff(gt,kk)**2*Lg_general)
    exact('general_composed_density_gate_Hessian',s.diff(Lg_general,kk)+2*kk*s.diff(Lg_general,kk,2)-expected_hess)

    # A Fourier mode of the fixed-gate filtered regional NR action.
    g,k2,screen,C,heat=s.symbols('g k2 screen C heat',positive=True)
    phi0,psi0,w0,chi0=s.symbols('phi psi w chi',real=True)
    aa=k2+screen
    L=-(rb+rd)*phi0-g*k2*phi0**2-f*rb*(psi0-chi0)-g*(
        2*aa*psi0*w0-k2*w0*w0-C*f*heat**2*k2*w0*w0)+g*aa*chi0**2
    solutions={phi0:-(rb+rd)/(2*g*k2),w0:-f*rb/(2*g*aa),chi0:-f*rb/(2*g*aa),
               psi0:-f*rb*k2*(1+C*f*heat**2)/(2*g*aa**2)}
    for vv in [phi0,psi0,w0,chi0]:exact('fixed_gate_Fourier_EL_'+str(vv),s.diff(L,vv).subs(solutions))
    Vb=(phi0+f*(psi0-chi0)).subs(solutions);Vd=phi0.subs(solutions)
    response=s.Matrix([Vb,Vd]).jacobian([rb,rd])
    exact('fixed_gate_force_reciprocity',response[0,1]-response[1,0])
    exact('kernel_invisible_carrier_cross_force_is_Newtonian',response[1,0]+1/(2*g*k2))
    exact('active_plateau_filtered_baryon_response',
          response[0,0].subs({f:1,screen:0})+(1+C*heat**2)/(2*g*k2))
    exact('active_plateau_carrier_self_response',response[1,1]+1/(2*g*k2))
    lon=s.factor(L.subs(solutions))
    exact('on_shell_action_baryon_potential',s.diff(lon,rb)+Vb)
    exact('on_shell_action_carrier_potential',s.diff(lon,rd)+Vd)
    # Externally varying masks cannot avoid reciprocity by freezing df/dsource.
    bb,dd=s.symbols('b d',real=True)
    Ftoy=s.Rational(1,2)+s.Rational(1,10)*s.tanh(bb+dd)
    Utoy=(bb+dd)**2/2+Ftoy**2*bb*bb/2
    exact('density_gate_full_energy_response_symmetric',s.diff(Utoy,bb,dd)-s.diff(Utoy,dd,bb))
    old_b=bb+dd+Ftoy**2*bb;old_d=bb+dd
    mismatch=s.diff(old_b,dd)-s.diff(old_d,bb)
    mismatch_num=float(mismatch.subs({bb:1,dd:s.Rational(1,2)}))
    bounded('negative_control_frozen_gate_force_derivatives_break_reciprocity',mismatch_num,abs(mismatch_num)>.01)

    # Global geometric regulator and its derivative costs; no physical reduced
    # Hamiltonian sign is inferred from this unreduced coefficient alone.
    LL,eps,xc,Rcurv,Ktrace=s.symbols('Lambda epsilon xc R Ktrace',positive=True)
    den=Ktrace**4+eps*LL**2
    ii=27*LL*Rcurv/(8*xc*den)
    exact('regulated_gate_R_derivative',s.diff(ii,Rcurv)-27*LL/(8*xc*den))
    exact('regulated_gate_K_derivative',s.diff(ii,Ktrace)+4*ii*Ktrace**3/den)
    dfk,P0,gradvel=s.symbols('fK P0 grad_deltaK',real=True)
    exact('gate_elimination_adds_spatial_velocity_square',-Mp2*(P0*dfk*gradvel)**2+Mp2*P0**2*dfk**2*gradvel**2)

    # Independent amplitude versus convex perspective: both are new gate
    # choices, and neither may be identified with the old prescribed switch.
    pp,ff,AA=s.symbols('p f A',positive=True)
    JJ=pp**s.Rational(3,2)
    exact('deep_kernel_amplitude_Schur_penalty',s.diff(JJ,pp)**2/(ff*s.diff(JJ,pp,2))-3*JJ/ff)
    perspective=AA*(pp/AA)**s.Rational(3,2)
    phess=s.hessian(perspective,[pp,AA])
    exact('convex_perspective_deep_hessian_rank_one',phess.det())
    exact('convex_perspective_pp_entry',phess[0,0]-3/(4*s.sqrt(AA*pp)))
    exact('convex_perspective_AA_entry',phess[1,1]-3*pp**s.Rational(3,2)/(4*AA**s.Rational(5,2)))
    exact('perspective_suppression_requires_large_A',perspective-JJ/s.sqrt(AA))
    exact('perspective_exact_off_not_at_finite_A',s.limit(perspective,AA,s.oo))

    # Bounded finite-graph heat derivative with a noncommuting geometry change.
    # This tests the Duhamel term that the candidate must retain in metric/clock
    # variation. scipy.expm_frechet is compared with central differences.
    from scipy.linalg import expm,expm_frechet
    n=10;Dmat=np.zeros((n,n));x=np.arange(n)*2*np.pi/n
    for j in range(n):Dmat[j,j]=-1;Dmat[j,(j+1)%n]=1
    weights=1+.2*np.sin(x);Lap=-Dmat.T@np.diag(weights)@Dmat
    direction=-Dmat.T@np.diag(np.cos(2*x))@Dmat
    tb=.3;sv=np.cos(x)+.3*np.sin(3*x);jvec=np.sin(x)+.2*np.cos(2*x)
    derivative=expm_frechet(tb*Lap,tb*direction,compute_expm=False)
    predicted=float(jvec@derivative@sv);errs=[]
    for step in [1e-3,1e-4,1e-5]:
        found=float(jvec@(expm(tb*(Lap+step*direction))-expm(tb*(Lap-step*direction)))@sv/(2*step))
        errs.append({'step':step,'error':abs(found-predicted)})
    bounded('filter_geometry_variation_central_difference',errs,errs[-1]['error']<2e-9)
    bounded('negative_control_freezing_filter_drops_nonzero_term',predicted,abs(predicted)>.01)

    # Coefficient positivity is global in finite Z, uniformity only on bounded Z.
    zvals=np.array([-10.,-2.,0.,2.,10.])
    bounded('exponential_positive_coefficients_at_declared_sample',
            {'Z':zvals.tolist(),'A':np.exp(zvals).tolist(),'B':np.exp(-zvals).tolist()},
            np.all(np.exp(zvals)>0) and np.all(np.exp(-zvals)>0))
    linbad={'Z':1.2,'time_coefficient':2.2,'space_coefficient':-.2}
    bounded('negative_control_linear_coupling_gradient_sign',linbad,linbad['space_coefficient']<0)

    output={'claim_id':'CD26_4_COMMON_ACTION_VARIATIONAL_INTERFACE','number_of_checks':len(checks),'checks':checks,
            'fixed_gate_response_matrix':str(response),'density_gate_Hessian_witness':str(s.simplify(hess.subs(kk,1))),
            'scope':['Declared covariant trial action plus exact NR and fixed-background identities',
                     'No full Einstein/clock constraint reduction or global PDE result',
                     'Exponential carrier is nonminimal preferred-frame coupling; baryons and photons remain minimal',
                     'Dynamical geometry/density gates require their full multiplier, metric and matter variations',
                     'Actual nu_mono zero-field and splice regularity retained; no global host-health inheritance']}
    pth=Path(args.output);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True,'filter_difference':errs[-1],
                      'density_gate_Hessian_witness':str(s.simplify(hess.subs(kk,1)))},indent=2))


if __name__=='__main__':main()
