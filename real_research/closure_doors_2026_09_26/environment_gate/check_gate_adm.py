#!/usr/bin/env python3
"""Global activation and isotropic ADM principal-sector check.

This verifies exact symbolic identities and rational sufficient bounds, not a
full covariant constraint closure or an observationally normalized MOND model.
The associated report derives the global estimates used in the bounds.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = {'checks': {}, 'expressions': {}, 'witnesses': {}, 'non_claims': [
        'No nonlinear well-posedness or full covariant constraint count',
        'No empirical normalization or likelihood pass',
        'Isotropic frozen-coefficient quadratic principal sector only',
        'B is a constant b*M2*Lambda in the explicit ADM test sector; L361 auxiliary variations remain to be added']}

    def exact(name, expr):
        residual = s.simplify(expr)
        out['checks'][name] = {'residual': str(residual), 'pass': residual == 0}
        assert residual == 0, (name, residual)

    def truth(name, condition, measured):
        value = bool(condition)
        out['checks'][name] = {'measured': str(measured), 'pass': value}
        assert value, (name, measured)

    t = s.symbols('t', positive=True)
    W = 1/(1+s.exp(1/t-1/(1-t)))
    derivatives = [s.simplify(s.diff(W, t, n).subs(t, s.Rational(1,2))) for n in range(4)]
    for n, expected in enumerate([s.Rational(1,2), 2, 0, -16]):
        exact('step_midpoint_derivative_' + str(n), derivatives[n]-expected)
    exact('step_reflection', W + W.subs(t, 1-t)-1)

    R, K = s.symbols('R K', real=True)
    L, eps, xc, M2, eta = s.symbols('Lambda epsilon x_c M2 eta', positive=True)
    B = s.symbols('B', real=True)
    d = K**4+eps*L**2
    a = s.Rational(27,4)*L
    tRK = a*R/(2*xc*d)
    tR, tK = s.diff(tRK,R), s.diff(tRK,K)
    tRR, tKK, tRKmixed = s.diff(tRK,R,2), s.diff(tRK,K,2), s.diff(tRK,R,K)
    exact('argument_K', tK + 4*tRK*K**3/d)
    exact('argument_KK', tKK - 4*tRK*K**2*(5*K**4-3*eps*L**2)/d**2)
    exact('argument_RK', tRKmixed + 4*K**3*tR/d)
    exact('argument_RR', tRR)
    w1,w2=s.symbols('Wprime Wsecond', real=True)
    fR=w1*tR
    fK=w1*tK
    fRR=w2*tR**2
    fKK=w2*tK**2+w1*tKK
    fRK=w2*tR*tK+w1*tRKmixed
    center={R:xc*d/a,w1:2,w2:0}
    exact('center_fR', fR.subs(center)-a/(xc*d))
    exact('center_fK', fK.subs(center)+4*K**3/d)
    exact('center_fKK', fKK.subs(center)-4*K**2*(5*K**4-3*eps*L**2)/d**2)
    exact('center_fRK', fRK.subs(center)+4*a*K**3/(xc*d**2))
    exact('center_fRR', fRR.subs(center))
    truth('global_denominator', d.is_positive, d)
    exact('jointzero_argument', tRK.subs({R:0,K:0}))
    exact('half_activation_threshold', tRK.subs(R,xc*d/a)-s.Rational(1,2))
    exact('regulator_threshold_cost', (xc*d/a)/(xc*K**4/a)-(1+eps*L**2/K**4))

    # Bounded-slope, concave, shear-completed spatial-curvature continuation.
    Ccorr=-eta*M2*(R*s.atan(R/L)-L*s.log(1+(R/L)**2)/2)
    CR=s.diff(Ccorr,R); CRR=s.diff(Ccorr,R,2)
    exact('concave_first_derivative', CR+eta*M2*s.atan(R/L))
    exact('concave_second_derivative', CRR+eta*M2*L/(R**2+L**2))
    exact('concave_flat_background_value', Ccorr.subs(R,0))
    exact('concave_flat_background_slope', CR.subs(R,0))

    # Independent exact spatial Ricci scalar for one TT polarization.
    z=s.symbols('z',real=True)
    h=s.Function('h')(z)
    metric=s.diag(s.exp(h),s.exp(-h),1)
    inv=metric.inv()
    def deriv(e,i):
        return s.diff(e,z) if i==2 else s.S.Zero
    gam={}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                gam[i,j,k]=s.simplify(sum(inv[i,l]*(deriv(metric[l,k],j)+deriv(metric[l,j],k)-deriv(metric[j,k],l))/2 for l in range(3)))
    ric=s.zeros(3)
    for i in range(3):
        for j in range(3):
            ric[i,j]=s.simplify(sum(deriv(gam[k,i,j],k)-deriv(gam[k,i,k],j)+sum(gam[k,k,l]*gam[l,i,j]-gam[k,j,l]*gam[l,i,k] for l in range(3)) for k in range(3)))
    ricci=s.simplify(sum(inv[i,j]*ric[i,j] for i in range(3) for j in range(3)))
    exact('TT_spatial_Ricci',ricci+s.diff(h,z)**2/2)
    hd,K0=s.symbols('h_dot K0',real=True)
    Kmat=s.diag(K0/3+hd/2,K0/3-hd/2,K0/3)
    shear=Kmat-s.eye(3)*s.trace(Kmat)/3
    exact('TT_trace_no_linear_or_quadratic_shift',s.trace(Kmat)-K0)
    exact('TT_shear_norm',s.trace(shear*shear)-hd**2/2)
    FR,FK,FRR,FKK,FRK=s.symbols('f_R f_K f_RR f_KK f_RK',real=True)
    CRsym,CRRsym=s.symbols('C_R C_RR',real=True)
    Z=M2+2*(B*FR+CRsym)
    exact('TT_equal_kinetic_gradient',M2/4+(B*FR+CRsym)/2-Z/4)
    wrong_cT=(M2+2*(B*FR+CRsym))/(M2+2*CRsym)
    truth('negative_control_omit_gate_shear',wrong_cT.subs({M2:1,B:1,FR:1,CRsym:0})!=1,wrong_cT)

    # Direct lapse/trace Taylor expansion, including cancellation from N.
    n,v,qexp=s.symbols('n zeta_dot expansion',real=True)
    Kfull=(K0+3*qexp*v)/(1+qexp*n)
    deltaK=s.series(Kfull-K0,qexp,0,3).removeO()
    expanded=(1+qexp*n)*(FK*deltaK+FKK*deltaK**2/2)
    quad=s.expand(s.series(expanded,qexp,0,3).removeO()).coeff(qexp,2)
    exact('trace_lapse_Hessian',quad-FKK*(3*v-K0*n)**2/2)
    db,F0=s.symbols('deltaB f0',real=True)
    with_db=(1+qexp*n)*(B+qexp*db)*(F0+FK*deltaK+FKK*deltaK**2/2)
    qdb=s.expand(s.series(with_db,qexp,0,3).removeO()).coeff(qexp,2)
    exact('deltaB_gate_mixing',qdb-(B*FKK*(3*v-K0*n)**2/2+db*FK*(3*v-K0*n)+n*db*F0))
    truth('negative_control_prescribed_gate_drops_trace', (B*FKK*(3*v-K0*n)**2/2).subs({B:1,FKK:1,v:1,K0:1,n:0})!=0, '9/2 omitted')

    # Exact algebraic shift and lapse reductions of the declared principal block.
    ZZ,alpha,kk=s.symbols('Z alpha k2',positive=True)
    CC,DD,EE=s.symbols('C D E',real=True)
    sh,rr,X,zz=s.symbols('s r X zeta',real=True)
    Delta=CC+2*ZZ/3
    F=CC*(2*ZZ/3)/Delta
    J=DD*(2*ZZ/3)/Delta
    Ee=EE-DD**2/Delta
    pre=ZZ*sh**2/3+CC*(X-sh)**2/2+DD*rr*(X-sh)+EE*rr**2/2
    sol_sh=s.solve(s.diff(pre,sh),sh)[0]
    exact('shift_solution',sol_sh-(CC*X+DD*rr)/Delta)
    exact('shift_reduced_block',pre.subs(sh,sol_sh)-(F*X**2/2+J*rr*X+Ee*rr**2/2))
    after=F*(3*v-K0*n)**2/2+J*(4*kk*zz)*(3*v-K0*n)+8*Ee*kk**2*zz**2+ZZ*kk*zz**2+2*ZZ*kk*n*zz+alpha*M2*kk*n**2/2
    denom=F*K0**2+alpha*M2*kk
    sol_n=s.solve(s.diff(after,n),n)[0]
    exact('lapse_solution',sol_n-(3*F*K0*v+(4*J*K0-2*ZZ)*kk*zz)/denom)
    red=s.factor(after.subs(n,sol_n))
    kin=s.simplify(s.diff(red,v,2))
    potential=s.simplify(red.subs(v,0)/zz**2)
    exact('reduced_scalar_kinetic',kin-9*F*alpha*M2*kk/denom)
    exact('reduced_scalar_potential',potential-(ZZ*kk+8*Ee*kk**2-(4*J*K0-2*ZZ)**2*kk**2/(2*denom)))
    omega2=s.simplify(-2*potential/kin)
    speed2=((4*J*K0-2*ZZ)**2-2*ZZ*alpha*M2-16*Ee*F*K0**2)/(9*F*alpha*M2)
    d4=-16*Ee/(9*F)
    exact('scalar_dispersion',omega2-(-2*ZZ*K0**2/(9*alpha*M2)+speed2*kk+d4*kk**2))
    cs,yy=s.symbols('sound_speed_squared y',positive=True)
    ycut=(1-4*cs+s.sqrt(1+8*cs))/8
    exact('massless_group_speed_cutoff', (cs+2*yy)**2-(cs+yy)- (4*yy**2+(4*cs-1)*yy+cs**2-cs))
    exact('massless_group_speed_cutoff_root', (4*yy**2+(4*cs-1)*yy+cs**2-cs).subs(yy,ycut))
    out['expressions'].update({'Z':str(Z),'C':'-M2*(2/3+c2)+B*f_KK','D':'B*f_RK','E':'B*f_RR+C_RR',
        'Delta':str(Delta),'F':str(F),'J':str(J),'E_effective':str(Ee),
        'scalar_kinetic':str(9*F*alpha*M2*kk/denom),
        'scalar_potential':str(ZZ*kk+8*Ee*kk**2-(4*J*K0-2*ZZ)**2*kk**2/(2*denom)),
        'f_mid_R':str(s.simplify(fR.subs(center))),'f_mid_KK':str(s.simplify(fKK.subs(center))),
        'f_mid_RK':str(s.simplify(fRK.subs(center))),'C_correction':str(Ccorr),
        'omega_squared':str(omega2),'high_k_coefficient_d4':str(d4),
        'massless_group_speed_cutoff_y_equals_d4k2':str(ycut)})

    # Global analytic bounds are derived in REPORT.md. Use strict rational
    # overestimates pi<4,sqrt(3)<2 rather than floating-point sign checks.
    b=s.Rational(1,10**10); et=s.Rational(1,10**6)
    c2=s.Rational(1,50); al=s.Rational(1,10**6)
    ep=xx=s.S.One; gap=c2/2
    C0=1+s.Rational(729,64)/(xx**2*ep**2)
    derivative_bound=1056/s.sqrt(ep)+36/(xx*ep)
    trace_perturb_bound=b*derivative_bound+s.Rational(8,3)*et
    tensor_lower=1-4*et
    curvature_upper=160*C0*b+169344*C0*b**2/(s.sqrt(ep)*gap)-et
    mixing_bound=378*b/(xx*ep*gap)
    truth('uniform_tensor_positive',tensor_lower>0,tensor_lower)
    truth('uniform_trace_gap',trace_perturb_bound<c2-gap,trace_perturb_bound)
    truth('uniform_effective_curvature_negative',curvature_upper<0,curvature_upper)
    truth('uniform_mixed_term_bound',mixing_bound<s.Rational(1,4),mixing_bound)
    truth('uniform_lapse_gradient_condition',tensor_lower>2*al,tensor_lower-2*al)
    out['witnesses']['global_coefficient_window']={'epsilon':'1','x_c':'1','b':str(b),'eta':str(et),'c2':str(c2),'alpha':str(al),
        'Delta_upper_over_M2':str(-gap),'tensor_lower_over_M2':str(tensor_lower),
        'Eeff_upper_times_(R2+Lambda2)_over_(M2Lambda)':str(curvature_upper),
        'abs_JK_over_Z_upper':str(mixing_bound),
        'scope':'All real R,K; isotropic frozen-coefficient principal sector. Scalar high-frequency stability only, no full mode-count assertion.'}

    # A concrete transition where the uncorrected gate has the wrong k^4 sign.
    mid={L:1,eps:1,xc:1,K:1,R:s.Rational(8,27),w1:2,w2:0,M2:1,B:b,eta:et}
    fr, fkk, frk, frr=[s.simplify(e.subs(mid)) for e in [fR,fKK,fRK,fRR]]
    Zbare=1+2*b*fr; Cbare=-s.Rational(2,3)-c2+b*fkk
    Dbare=b*frk; gapbare=Cbare+2*Zbare/3
    Ebare=b*frr-Dbare**2/gapbare
    truth('bare_gate_has_positive_k4_coefficient',Ebare>0,Ebare)
    # Corrected midpoint evaluation is informational high precision; the global
    # sign theorem above uses exact rational inequalities and controls its sign.
    zcorr=Zbare+2*CR.subs(mid)
    dcorr=Cbare+2*zcorr/3
    ecorr=b*frr+CRR.subs(mid)-Dbare**2/dcorr
    fcorr=Cbare*(2*zcorr/3)/dcorr
    jcorr=Dbare*(2*zcorr/3)/dcorr
    qthreshold=s.simplify(2*zcorr*fcorr/((4*jcorr-2*zcorr)**2-2*zcorr*al))
    out['witnesses']['midpoint']={'R_over_Lambda':'8/27','K_over_sqrtLambda':'1','bare_Eeff':str(Ebare),
        'corrected_Z':str(s.N(zcorr,35)),'corrected_Delta':str(s.N(dcorr,35)),
        'corrected_Eeff':str(s.N(ecorr,35)),'corrected_F':str(s.N(fcorr,35)),
        'sufficient_k2_over_Lambda_threshold':str(s.N(qthreshold,35))}

    # Causal price: a K=0 positive-curvature midpoint has no frozen Jeans term.
    # alpha=0.1 is an explicit second witness, not a PPN-compatible choice.
    static={L:1,eps:1,xc:1,K:0,R:s.Rational(4,27),w1:2,w2:0,M2:1,B:b,eta:et}
    zstatic=1+2*b*fR.subs(static)+2*CR.subs(static)
    cstatic=-s.Rational(2,3)-c2
    fstatic=cstatic*(2*zstatic/3)/(cstatic+2*zstatic/3)
    estatic=CRR.subs(static)
    alpha_static=s.Rational(1,10)
    sstatic=2*zstatic*(2*zstatic-alpha_static)/(9*fstatic*alpha_static)
    dstatic=-16*estatic/(9*fstatic)
    cutoff=s.simplify(ycut.subs(cs,sstatic)/dstatic)
    out['witnesses']['finite_group_speed_band']={'K':'0','R_over_Lambda':'4/27','alpha':'1/10',
        'sound_speed_squared':str(s.N(sstatic,35)),'d4_times_Lambda':str(s.N(dstatic,35)),
        'k_max_over_sqrtLambda':str(s.N(s.sqrt(cutoff),35)),
        'scope':'Group speed at most 1 in this frozen massless branch below the displayed k cutoff; fourth-order PDE has no all-k metric light cone. alpha=0.1 is not advertised as PPN-compatible.'}
    fast_static=2*zstatic*(2*zstatic-al)/(9*fstatic*al)
    out['witnesses']['small_alpha_causal_failure']={'alpha':str(al),'sound_speed_squared':str(s.N(fast_static,35)),
        'scope':'Original positive-coefficient small-alpha witness is already superluminal on this patch.'}

    # Kappa remains adjustable under an allowed additive four-form constant.
    flux,Za,beta,bp,Cvac,G=s.symbols('q Zflux beta bprimitive Cvac G',positive=True)
    P=(Za/2+bp*beta**2)*flux**2+Cvac
    energy=flux*s.diff(P,flux)-P
    ratio=beta**2*flux**2/energy
    exact('fourform_legendre_energy',energy-((Za/2+bp*beta**2)*flux**2-Cvac))
    exact('fourform_charge_unchanged_by_constant',s.diff(P,flux)-s.diff(P-Cvac,flux))
    truth('kappa_not_counterterm_invariant',s.diff(ratio,Cvac)!=0,s.diff(ratio,Cvac))
    exact('kappa_without_counterterm',ratio.subs(Cvac,0)-2*beta**2/(Za+2*bp*beta**2))
    out['expressions']['kappa_squared_with_counterterm']=str(ratio)
    out['result']='Exact identities and declared global sufficient coefficient bounds verified; see report for principal-sector scope.'
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
