#!/usr/bin/env python3
"""Cubic scalar-metric principal elimination at affine local scalar jets.

Sign convention -+++; X=-grad(chi)^2; L3=+gamma X Box(chi).
Both metric and scalar principal terms are retained. Numerical samples are
local constitutive jets, not solved finite-gradient cosmologies.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sy
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parents[1]
ROOT=HERE.parents[4]
BRIDGE=REPAIR/'cosmological_bridge_2026'
PREVIOUS=REPAIR/'l192_principal_audit_2026'
sys.path.insert(0,str(PREVIOUS))
from principal_audit import jets as gamma0_jets
sys.path.insert(0,str(BRIDGE))
from radiation_probe import ProbeBackground


@lru_cache(maxsize=1)
def derive():
    gamma=sy.Symbol('gamma',real=True)
    M2=sy.Symbol('M2',positive=True)
    eta=sy.diag(-1,1,1,1)
    v=sy.Matrix(sy.symbols('v0 v1 v2 v3',real=True))
    vu=eta*v
    entries={(i,j):sy.Symbol('h%d%d'%(i,j),real=True) for i in range(4) for j in range(i,4)}
    H=sy.Matrix(4,4,lambda i,j:entries[min(i,j),max(i,j)])
    X=-(v.T*vu)[0]
    box=sy.trace(eta*H)
    dX=-2*H*vu
    vHv=(vu.T*H*vu)[0]
    Hnorm=sy.trace(eta*H*eta*H)
    # Inverse-metric variation of sqrt(-g) gamma X Box(chi), after the two
    # connection-variation derivative terms have been integrated by parts.
    sym_vdX=(v*dX.T+dX*v.T)/2
    metric_euler=gamma*(-eta*X*box/2-box*(v*v.T)+X*H
                       -(X*H+sym_vdX)+eta*((vu.T*dX)[0]+X*box)/2)
    stress=2*gamma*box*(v*v.T)+gamma*(v*dX.T+dX*v.T)-gamma*eta*(vu.T*dX)[0]
    stress_hessian=2*gamma*(box*(v*v.T)-(v*(H*vu).T+(H*vu)*v.T)+eta*vHv)
    trace=sy.expand(sy.trace(eta*stress))
    reverse=stress-eta*trace/2
    contracted=sy.expand((vu.T*reverse*vu)[0])
    expected_contraction=gamma*X*(X*box+4*vHv)
    curvature_feedback=sy.expand(-2*gamma*contracted/M2)
    deltaZ=-2*gamma**2*X*(X*eta+4*vu*vu.T)/M2
    deltaZ_H=sum(deltaZ[i,j]*H[i,j] for i in range(4) for j in range(4))
    # Current divergence identity uses the covariant scalar commutator:
    # Box X=-2 H.H-2 v.grad(Box chi)-2 R(v,v).
    grad_box,Rvv=sy.symbols('v_grad_box R_vv',real=True)
    scalar_variation=2*gamma*(box**2+grad_box)+gamma*(-2*Hnorm-2*grad_box-2*Rvv)
    expected_E3=2*gamma*(box**2-Hnorm-Rvv)
    # Linearization of the self-Hessian terms at arbitrary background H.
    directZ=4*gamma*(box*eta-eta*H*eta)
    dh=sy.Matrix(4,4,lambda i,j:sy.Symbol('dh%d%d'%(min(i,j),max(i,j)),real=True))
    eps=sy.Symbol('eps',real=True)
    direct=sy.diff(2*gamma*(sy.trace(eta*(H+eps*dh))**2
                          -sy.trace(eta*(H+eps*dh)*eta*(H+eps*dh))),eps).subs(eps,0)
    direct_expected=sum(directZ[i,j]*dh[i,j] for i in range(4) for j in range(4))
    # Principal source conservation is required by linearized Einstein:
    # replace H_ab by xi_a xi_b sigma; its leading stress divergence vanishes.
    xi=sy.Matrix(sy.symbols('xi0 xi1 xi2 xi3',real=True))
    plane_subs={entries[i,j]:xi[i]*xi[j] for i in range(4) for j in range(i,4)}
    source_div=(xi.T*eta*stress.subs(plane_subs)).applyfunc(sy.expand)
    checks=dict(
        inverse_metric_variation_stress=all(sy.expand(x)==0 for x in -2*metric_euler-stress),
        hessian_stress_form=all(sy.expand(x)==0 for x in stress-stress_hessian),
        scalar_commutator_identity=sy.expand(scalar_variation-expected_E3)==0,
        stress_trace=sy.expand(trace-2*gamma*(-X*box+2*vHv))==0,
        trace_reversed_contraction=sy.expand(contracted-expected_contraction)==0,
        covariant_debraiding_tensor=sy.expand(curvature_feedback-deltaZ_H)==0,
        arbitrary_hessian_linearization=sy.expand(direct-direct_expected)==0,
        principal_einstein_source_divergence=all(x==0 for x in source_div))

    # Anisotropic affine corrections, with chi=Q t+sqrt(Y) x, w=v.n.
    Q,Y,z,p,r,C,d,W,F,s,t=sy.symbols('Q Y z p r C d W F s t',real=True)
    Xlocal=Q**2-Y
    K=2*p+4*Q**2*r
    G=2*p-4*r*z-2*s*C*(W-2*z*d)/F
    quarter0=16*Q**2*r**2*z+K*G
    Knew=K+t*(4*Q**2-Xlocal)
    Gnew=G-t*(Xlocal+4*z)
    # t=2 gamma^2 X/M2; half of the mixed characteristic coefficient.
    quarter_new=(4*Q*r+4*t*Q)**2*z+Knew*Gnew
    linear=32*Q**2*r*z+(4*Q**2-Xlocal)*G-K*(Xlocal+4*z)
    quadratic=Xlocal*(Xlocal-4*Q**2+4*z)
    proxy_s=p*(W-2*Q**2*C)/(W*C)
    Fvalue=W-2*Q**2*C-2*z*d
    quarter_proxy=-8*p*z*(r+K*Q**2*C*d/(W*F))
    linear_proxy=(-8*p*z-2*p*Xlocal-4*r*Xlocal*(Q**2-z)
                  -(4*Q**2-Xlocal)*8*p*Q**2*C*z*d/(W*F))
    checks.update(
        full_gamma_squared_discriminant_polynomial=sy.expand(quarter_new-quarter0-t*linear-t*t*quadratic)==0,
        proxy_zero_discriminant_identity=sy.factor((quarter0.subs(s,proxy_s)-quarter_proxy).subs(F,Fvalue))==0,
        proxy_zero_linear_correction=sy.factor((linear.subs(s,proxy_s)-linear_proxy).subs(F,Fvalue))==0,
        timelike_quadratic_bound_identity=sy.expand(quadratic+3*Xlocal**2+4*Xlocal*(Y-z))==0)
    # Independent homogeneous control matches existing cubic_principal_audit.
    homogeneous_deltaZ=deltaZ.subs({v[0]:Q,v[1]:0,v[2]:0,v[3]:0})
    checks['homogeneous_kinetic_control']=sy.simplify(-homogeneous_deltaZ[0,0]-6*gamma**2*Q**4/M2)==0
    checks['homogeneous_gradient_control']=sy.simplify(homogeneous_deltaZ[1,1]+2*gamma**2*Q**4/M2)==0
    if not all(checks.values()):
        raise AssertionError(checks)
    return dict(checks=checks,expressions=dict(
        stress=str(stress_hessian),trace_reversed_contraction=str(sy.factor(expected_contraction)),
        scalar_E3=str(expected_E3),deltaZ=str(deltaZ),direct_hessian_Z=str(directZ),
        quarter_discriminant=str(quarter_new),quarter_at_proxy=str(quarter_proxy),
        linear_at_proxy=str(linear_proxy),quadratic_correction=str(quadratic)),
        conventions=dict(signature='-+++',X='-v_mu v^mu',H='nabla_mu nabla_nu chi',
                         t='2 gamma^2 (Q^2-Y)/M2'))


def corrected(j,Q,s,Y,mu,gamma=1e-6,M2=1.,hessian_cov=None):
    p,r,W,d,WYY=(j[k] for k in ('PX','PXX','W','WY','WYY'))
    w=np.sqrt(Y)*mu;z=w*w;X=Q*Q-Y
    C=d+2*z*WYY;F=W-2*Q*Q*C-2*z*d
    if F==0 or M2<=0:
        raise ValueError('singular clock block or invalid Planck coefficient')
    K=2*p+4*Q*Q*r
    G=2*p-4*r*z-2*s*C*(W-2*z*d)/F
    linear_coefficient=8*Q*r*w
    t=2*gamma*gamma*X/M2
    deltaK=t*(4*Q*Q-X);deltaB=8*t*Q*w;deltaG=-t*(X+4*z)
    newK=K+deltaK;newB=linear_coefficient+deltaB;newG=G+deltaG
    quarter0=linear_coefficient**2/4+K*G
    affine_quarter=newB**2/4+newK*newG
    linear=32*Q*Q*r*z+(4*Q*Q-X)*G-K*(X+4*z)
    quadratic=X*(X-4*Q*Q+4*z)
    shift=t*linear+t*t*quadratic
    dhK=dhB=dhG=0.
    if hessian_cov is not None:
        hessian_cov=np.asarray(hessian_cov,dtype=float)
        if hessian_cov.shape!=(4,4) or not np.allclose(hessian_cov,hessian_cov.T):
            raise ValueError('background covariant Hessian must be symmetric 4x4')
        eta=np.diag([-1.,1.,1.,1.])
        directZ=4*gamma*(np.trace(eta@hessian_cov)*eta-eta@hessian_cov@eta)
        direction=np.array([mu,np.sqrt(1-mu*mu),0.])
        dhK=-directZ[0,0]
        dhB=2*directZ[0,1:]@direction
        dhG=direction@directZ[1:,1:]@direction
        newK+=dhK;newB+=dhB;newG+=dhG
    quarter=newB**2/4+newK*newG
    speeds=[(-newB/2+sign*np.lib.scimath.sqrt(quarter))/newK for sign in (-1,1)]
    return dict(X=X,z=z,C=C,F=F,K0=K,G0=G,B0=linear_coefficient,
                t=t,deltaK=deltaK,deltaB=deltaB,deltaG=deltaG,
                kinetic=newK,gradient=newG,mixed_coefficient=newB,
                quarter_gamma0=quarter0,quarter_finite_gamma=quarter,
                quarter_with_affine_metric_feedback=affine_quarter,
                quarter_shift_from_exact_polynomial=shift,
                polynomial_roundoff_residual=float(affine_quarter-quarter0-shift),
                linear_correction_coefficient=linear,quadratic_correction_coefficient=quadratic,
                hessian_deltaK=float(dhK),hessian_deltaB=float(dhB),hessian_deltaG=float(dhG),
                background_hessian=None if hessian_cov is None else hessian_cov.tolist(),
                phase_speeds_real=[float(x.real) for x in speeds],
                phase_speeds_imag=[float(x.imag) for x in speeds])


def numerical():
    old=json.loads((PREVIOUS/'run_001/result.json').read_text())
    original=json.loads((BRIDGE/'radiation_002/result.json').read_text())
    samples={r['a']:r for r in original['samples']}
    bg=ProbeBackground(5.)
    rows=[]
    for source in old['rows']:
        if 'coefficient_q_cases' not in source:
            continue
        U,d,ell,s=(source[k] for k in ('U','d','ell','s'))
        old_background=samples[source['a']]
        physical_state=[old_background[k] for k in ('a','H','q','tau','rho_baryon','rho_radiation')]
        rates=bg.evaluate(physical_state)[0]
        for convention,Q,cases in (
            ('coefficient_q',source['coefficient_q'],source['coefficient_q_cases']),
            ('physical_q',source['physical_q'],source['physical_q_recomputed_proxy_roots'])):
            # Both archives list longitudinal zero first, transverse second.
            for case,polarization in zip(cases,('L','T')):
                Y=case['Y']
                pure=gamma0_jets(U,d,ell,Q,Y)
                raw=bg.model.jets(source['tau'],Q*Q-Y,Y)
                finite={key:float(raw[value]) for key,value in
                        dict(PX='P_X',PXX='P_XX',W='W',WY='W_Y',WYY='W_YY').items()}
                directions=[]
                for mu in (0.,1.):
                    directions.append(dict(mu=mu,
                        isolated_metric_feedback=corrected(pure,Q,s,Y,mu),
                        frozen_finite_gamma_action=corrected(finite,Q,s,Y,mu)))
                row=dict(a=source['a'],tau=source['tau'],Q=Q,s=s,Y=Y,
                         q_convention=convention,source_proxy_polarization=polarization,
                         gamma=1e-6,M2=1.,gamma0_jets=pure,finite_gamma_jets=finite,
                         directions=directions)
                if convention=='physical_q':
                    # Kinematic continuation chi=C(t)+b_comoving*x on the
                    # original FLRW geometry at one point, with b_phys²=Y.
                    # The old physical H, Q and Qdot are solved source data;
                    # adding a gradient is NOT asserted to solve constraints.
                    Hubble=old_background['H'];qdot=rates['qd'];b=np.sqrt(Y)
                    hessian=np.diag([qdot,-Hubble*Q,-Hubble*Q,-Hubble*Q])
                    hessian[0,1]=hessian[1,0]=-Hubble*b
                    row['non_affine_physical_fixture']=dict(
                        H=Hubble,qdot=qdot,hessian_cov=hessian.tolist(),
                        scope='chi=C(t)+b_comoving*x kinematic jet on the original physical FLRW geometry; new gradient backreaction not solved',
                        directions=[dict(mu=mu,principal=corrected(finite,Q,s,Y,mu,hessian_cov=hessian))
                                    for mu in (0.,1.)])
                if polarization=='L':
                    # Use the true finite-gamma P/W jets in the proxy-zero
                    # relation, retaining the same action and solving only Y.
                    def finite_proxy(Yvalue):
                        jj=bg.model.jets(source['tau'],Q*Q-Yvalue,Yvalue)
                        cc=jj['W_Y']+2*Yvalue*jj['W_YY']
                        return jj['P_X']*(jj['W']-2*Q*Q*cc)/(jj['W']*cc)-s
                    root=brentq(finite_proxy,0.,8*Y,xtol=1e-16)
                    rr=bg.model.jets(source['tau'],Q*Q-root,root)
                    jj={key:float(rr[value]) for key,value in
                        dict(PX='P_X',PXX='P_XX',W='W',WY='W_Y',WYY='W_YY').items()}
                    row['finite_gamma_proxy_root']=dict(Y=root,
                        principal=corrected(jj,Q,s,root,1.))
                rows.append(row)
    return rows


def run():
    exact=derive()
    rows=numerical()
    longitudinal=[r for r in rows if r['source_proxy_polarization']=='L']
    for row in longitudinal:
        for name in ('isolated_metric_feedback','frozen_finite_gamma_action'):
            if row['directions'][1][name]['quarter_finite_gamma']>=0:
                raise AssertionError('previous longitudinal counterexample changed sign; inspect rather than relabel')
        point=row['finite_gamma_proxy_root']['principal']
        if point['quarter_finite_gamma']>=0 or min(point['X'],point['C'],point['F'],point['kinetic'])<=0:
            raise AssertionError('recomputed finite-gamma proxy root does not meet stated counterexample conditions')
    return dict(exact=exact,rows=rows,
                result='At all ten prior longitudinal proxy zeros, affine cubic metric feedback and the frozen finite-gamma coefficient jets retain a negative discriminant.',
                scope='Covariant Einstein trace-reversal removes the explicit cubic Ricci mixing; affine local chi Hessian for numerical evaluation; tau elliptic block reduced at nonzero spatial wavevector.',
                non_claims=['Not an on-shell finite-gradient cosmology or global stability theorem',
                            'No assumption that gamma small implies negligible corrections',
                            'Nonzero-Hessian numerical cases are specified kinematic FLRW jets, not arbitrary Hessians or solved new backgrounds',
                            'No coefficient reconstruction, CMB map, or extra particle dark matter'])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exact_checks=result['exact']['checks'],result=result['result'],first=result['rows'][0]),indent=2))
