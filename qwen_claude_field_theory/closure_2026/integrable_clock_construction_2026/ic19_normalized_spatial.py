#!/usr/bin/env python3
"""IC19 normalized pinned action: expanding domain and spatial lapse variation.

No runtime replacement of IC18 parameters. This module defines a distinct
action revision; see IC19_NORMALIZED_SPATIAL.md for its global Hamiltonian.
"""
import argparse
import json
import mpmath as mp
import sympy as s
import ic18_pinned_clock as legacy


def constants():
    c=legacy.constants().copy()
    c['a02']=c['Lambda']/(32*mp.pi)
    return c


def pressure(S):
    c=constants()
    S=mp.mpf(S)
    if not (mp.isfinite(S) and S>c['Sstar']):
        raise ValueError('Require finite S>Sstar')
    X=mp.exp(-2*S)/2
    F,FX,FXX,Q,rho=legacy.build()['evaluate'](X,c['Xstar'],c['epsilon'],c['vacuum'])
    return dict(S=S,X=X,F=F,FX=FX,FXX=FXX,Q=Q,rho=rho)


def switch_argument(S,q,lapse_switch=False):
    wc=constants()['wc']
    return -q*mp.exp(S-2*wc)/3 if lapse_switch else -q*mp.exp(-3*wc)/3


def homogeneous_h(S,q,lapse_switch=False):
    c=constants()
    r=switch_argument(S,q,lapse_switch)
    eta=legacy.activation(r)
    P0=legacy.original_pressure()(S,c['wc'],c['Lambda'],c['a02'])[0]
    return (-mp.exp(S-2*c['wc'])*q*q/3
            -mp.exp(S)*((1-eta)*P0+eta*pressure(S)['F']))


def spatial_coefficients(S,q,lapse_switch=False):
    c=constants()
    r=switch_argument(S,q,lapse_switch)
    u=(S+2*c['wc'])/(S+c['wc'])
    A=mp.exp(S+2*c['wc'])/2
    B=(1-legacy.activation(r))*mp.exp(S+2*c['wc'])*(1-u*u)
    return A,B


def identities():
    S,w,eta,p,m,a02,R,F,J=s.symbols('S w eta p m a02 R F J',real=True)
    u=(S+2*w)/(S+w)
    us=s.diff(u,S)
    checks={'pinned_gradient_reduction':s.factor(2*u*(S+w)*us+(S+w)**2*us**2-(1-u*u))}
    old=-m*R/2-(1-eta)*p*p*(F*R+J)/(2*m*a02)
    correction=(1-eta)*p*p*(F*R+J)/(2*m*a02)
    checks['removed_curvature_stiffness']=s.simplify(s.diff(old+correction,R)+m/2)
    checks['removed_momentum_gradient']=s.simplify(s.diff(old+correction,J))
    checks['unchanged_static_value']=correction.subs(p,0)
    checks['unchanged_static_momentum_jet']=s.diff(correction,p).subs(p,0)
    # Independent Euler differentiation in a local spatial coordinate;
    # covariance replaces the total divergence by D_i on the leaf.
    q,Sx,Sxx,qx,R=s.symbols('q Sx Sxx qx R',real=True)
    f=s.Function('f')(S,q)
    A=s.Function('A')(S)
    B=s.Function('B')(S,q)
    density=f-A*R-B*Sx*Sx
    def Dx(g):return s.diff(g,S)*Sx+s.diff(g,Sx)*Sxx+s.diff(g,q)*qx
    EL=s.diff(density,S)-Dx(s.diff(density,Sx))
    expected=s.diff(f,S)-s.diff(A,S)*R+s.diff(B,S)*Sx*Sx+2*s.diff(B,q)*qx*Sx+2*B*Sxx
    checks['spatial_lapse_Euler']=s.simplify(EL-expected)
    k,dS=s.symbols('k dS',real=True)
    linear=s.diff(EL,S).subs({Sx:0,Sxx:0,qx:0})*dS+s.diff(EL,Sxx).subs({Sx:0,qx:0})*(-k*k*dS)
    target=(s.diff(f,S,2)-s.diff(A,S,2)*R-2*B*k*k)*dS
    checks['lapse_principal_multiplier']=s.simplify(linear-target)
    # Normalized local TT Hamiltonian H=2N pi_T²/m+mN k² gamma²/8.
    N,piT,gamma=s.symbols('N piT gamma',positive=True)
    HT=2*N*piT*piT/m+m*N*k*k*gamma*gamma/8
    gamma_dot=s.diff(HT,piT)
    gamma_ddot=s.diff(gamma_dot,piT)*(-s.diff(HT,gamma))
    checks['TT_metric_cone']=s.simplify(gamma_ddot+N*N*k*k*gamma)
    dq=s.symbols('dq',real=True)
    momentum=s.diag(0,dq/2,dq/2)
    trace=s.trace(momentum)
    TF=momentum-s.eye(3)*trace/3
    checks['scalar_shift_constraint']=momentum[0,0]
    checks['scalar_tracefree_norm']=s.simplify(s.trace(TF*TF)-dq*dq/6)
    E=s.symbols('E',positive=True)
    P0,P1=s.symbols('P0 P1',real=True)
    switch=s.Function('eta')(q)
    h=-E*q*q/3-s.exp(S)*((1-switch)*P0+switch*P1)
    checks['trace_switch_UV_coefficient']=s.simplify(E/3+s.diff(h,q,2)/2+s.exp(S)*(P1-P0)*s.diff(switch,q,2)/2)
    c=s.symbols('c',positive=True)
    U=(1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    checks['primitive_monotonicity_identity']=s.simplify(s.diff(U,c)+s.log(1-c)**2)
    d=s.symbols('d',positive=True)
    exponent=-1/d+1/(s.Rational(1,4)-d)
    td,tdd=s.diff(exponent,d),s.diff(exponent,d,2)
    # e^exponent is super-algebraically small as d -> 0+; this is the
    # remaining rational coefficient in eta_rr*d^4/e^exponent.
    leading=d**4*(-4*(s.Rational(3,4)-d)*(td*td+tdd)+2*td)
    checks['switch_tail_negative_second_derivative']=s.limit(leading,d,0,dir='+')+3
    # Curved homogeneous constraint bracket in q_metric,p_q, V=exp(3q_metric).
    fp,fS,fSp,A0,R0=s.symbols('fp fS fSp A0 R0',real=True)
    f0=s.symbols('f0',real=True)
    Cq=3*(fS-q*fSp)-A0*R0
    Cp=fSp/2
    Hq=3*(f0-q*fp)-A0*R0
    Hp=fp/2
    checks['curved_canonical_preservation']=s.expand(Cq*Hp-Cp*Hq-((3*fS-A0*R0)*fp-(3*f0-A0*R0)*fSp)/2)
    return checks


def plateau_domain():
    c=constants()
    lower=c['Lambda']/3
    rows=[]
    for gap in ('1e-10','1e-6','.001','.025','.1','1','10','100'):
        b=pressure(c['Sstar']+mp.mpf(gap))
        H=mp.sqrt(b['rho']/(3*c['mstar']))
        b.update(H=H,r_squared=mp.exp(-2*c['wc'])*H*H)
        rows.append(b)
    return dict(analytic_r_squared_lower_bound=lower,activation_upper_edge=mp.mpf(3)/4,
                samples=rows,nonnegative_dust_and_radiation_only_increase_bound=True)


def curved_point(S,r,lapse_switch=False):
    S,r=map(mp.mpf,(S,r))
    c=constants()
    pressure(S)
    if not mp.mpf('.5')<r*r<mp.mpf('.75'):
        raise ValueError('Require a strictly transitional r²')
    q=-3*r*mp.exp(-S+2*c['wc']) if lapse_switch else -3*r*mp.exp(3*c['wc'])
    A,B=spatial_coefficients(S,q,lapse_switch)
    h=lambda S,q:homogeneous_h(S,q,lapse_switch)
    f=h(S,q)
    fS=mp.diff(lambda t:h(t,q),S)
    fSS=mp.diff(lambda t:h(t,q),S,2)
    fq=mp.diff(lambda p:h(S,p),q)
    fSq=mp.diff(h,(S,q),(1,1))
    Rbar=fS/A  # solves the actual lapse secondary with constant S,q
    M0=fSS-A*Rbar
    def curved_h(t):
        return h(t,q)-spatial_coefficients(t,q,lapse_switch)[0]*Rbar
    # S^3 has -Delta eigenvalues ell(ell+2) Rbar/6 when Rbar>0.
    spectral=[M0-2*B*ell*(ell+2)*Rbar/6 for ell in range(5)]
    brackets=[mp.matrix([[0,-v],[v,0]]) for v in spectral]
    ranks=[sum(v>mp.mpf('1e-40') for v in mp.svd(pb,compute_uv=False)) for pb in brackets]
    source=((3*fS-A*Rbar)*fq-(3*f-A*Rbar)*fSq)/2
    def H(Q,P,t):
        V=mp.exp(3*Q)
        return V*(h(t,P/(2*V))-spatial_coefficients(t,P/(2*V),lapse_switch)[0]*Rbar*mp.exp(-2*Q))
    def CS(Q,P):return mp.diff(lambda t:H(Q,P,t),S)
    direct=(mp.diff(lambda Q:CS(Q,2*q),0)*mp.diff(lambda P:H(0,P,S),2*q)
            -mp.diff(lambda P:CS(0,P),2*q)*mp.diff(lambda Q:H(Q,2*q,S),0))
    return dict(S=S,r=r,q=q,eta=legacy.activation(r),u=(S+2*c['wc'])/(S+c['wc']),
                A=A,B=B,Rbar=Rbar,f=f,fS=fS,fSS=fSS,fq=fq,fSq=fSq,M0=M0,
                H_physical=mp.exp(-c['wc']-S)*fq/2,
                secondary_residual=mp.diff(curved_h,S),
                direct_lapse_hessian_residual=mp.diff(curved_h,S,2)-M0,
                mode_operator=spectral,mode_ranks=ranks,preservation_source=source,
                Sdot_coordinate=-source/M0 if M0!=0 else mp.nan,
                direct_preservation_residual=direct-source,
                continuous_symbol_zero_k_squared=M0/(2*B),
                genuine_discrete_kernel_established=False)


def scalar_kinetic(S,r,k_squared):
    """Frozen high-frequency scalar momentum coefficient, not full dispersion.

    Momentum-constraint principal part gives pi_TF²=(delta q)²/6.
    Eliminating the linearized lapse gives the displayed Schur coefficient.
    Curvature corrections to the shift constraint are omitted: only its UV
    limit is used to diagnose a ghost, never a low-k physical certification.
    """
    row=curved_point(S,r)
    S,q=row['S'],row['q']
    k_squared=mp.mpf(k_squared)
    fqq=mp.diff(lambda p:homogeneous_h(S,p),q,2)
    a=mp.exp(S-2*constants()['wc'])/3+fqq/2
    M=row['M0']-2*row['B']*k_squared
    if M==0:raise ValueError('Singular frozen lapse operator')
    cross=row['fSq']
    full=mp.matrix([[2*a,cross],[cross,M]])
    schur=full[0,0]-full[0,1]*full[1,1]**-1*full[1,0]
    reduced=a-cross*cross/(2*M)
    return dict(S=S,r=row['r'],k_squared=k_squared,UV_momentum_coefficient=a,
                lapse_operator=M,reduced_momentum_coefficient=reduced,
                schur_identity_residual=schur/2-reduced,
                curvature_wavelength_ratio=k_squared/(1+abs(row['Rbar'])),
                full_dispersion_computed=False)


def curvature_completion():
    """Necessary UV compatibility, plus an exact local Hessian construction.

    Not substituted into IC19; no low-frequency or global health is inferred.
    """
    a,cross,RR,k=s.symbols('a HqR HRR k',real=True)
    matrix=s.Matrix([[a,2*cross*k*k],[2*cross*k*k,8*RR*k**4]])
    leading=s.factor(matrix.det()/k**4)
    q,R,T,beta,ell,A0=s.symbols('q R T beta ell A0',real=True)
    H=-T*q*q/6+beta*(q+ell*R)**2/2-A0*R
    Hqq,HqR,HRR=s.diff(H,q,2),s.diff(H,q,R),s.diff(H,R,2)
    compatibility=s.factor((Hqq+T/3)*HRR-HqR*HqR)
    return dict(leading_hamiltonian_determinant=leading,
                uncompleted_control=leading.subs({a:1,cross:1,RR:0}),
                completed_hessian_residual=compatibility,
                completed_scalar_UV_coefficient=s.factor(T/6+Hqq/2),
                completed_example=str(H),
                not_a_global_theory=True)


def report():
    mp.mp.dps=70
    domain=plateau_domain()
    rows=[curved_point(S,r) for S in ('.076','.1','.175','1.075') for r in ('.73','.75','.77','.8','.82','.84','.86')]
    witness=curved_point('.1','.82')
    uv=[scalar_kinetic('.1','.82',k) for k in ('1','100','1e4','1e8','1e12')]
    old_switch=[curved_point('.1',r,lapse_switch=True) for r in ('.75','.77','.8')]
    completion=curvature_completion()
    checks={key:value==0 for key,value in identities().items()}
    checks.update(normalization=abs(32*mp.pi*constants()['a02']/constants()['Lambda']-1)<mp.mpf('1e-60'),
                  invariant_plateau_margin=domain['analytic_r_squared_lower_bound']>mp.mpf('.75'),
                  positive_plateau_samples=all(b['FX']>0 and b['Q']>b['FX'] for b in domain['samples']),
                  actual_curved_secondary=all(abs(b['secondary_residual'])<mp.mpf('1e-55') for b in rows),
                  independent_curved_Hessian=all(abs(b['direct_lapse_hessian_residual'])<mp.mpf('1e-55') for b in rows))
    checks.update(independent_curved_preservation=all(abs(b['direct_preservation_residual'])<mp.mpf('1e-50') for b in rows),
                  expanding_ghost_background=witness['H_physical']>0 and witness['Rbar']>0 and witness['M0']<0,
                  scalar_Schur_identity=all(abs(b['schur_identity_residual'])<mp.mpf('1e-50') for b in uv),
                  negative_UV_scalar_coefficient=uv[-1]['UV_momentum_coefficient']<0 and uv[-1]['reduced_momentum_coefficient']<0)
    checks.update(curvature_completion_identity=completion['completed_hessian_residual']==0,
                  uncompleted_curvature_counterexample=completion['uncompleted_control']<0)
    return dict(candidate='IC19: normalized pinned clock with obsolete momentum-curvature/gradient terms removed',
                full_theory='OPEN',checks=checks,constants=constants(),expanding_domain=domain,
                curved_transition_points=rows,old_lapse_switch_controls=old_switch,
                expanding_curved_witness=witness,scalar_UV_controls=uv,
                scalar_stability_status='FAIL: negative constrained scalar momentum coefficient in the UV at the expanding curved witness',
                next_curvature_compatibility=completion,
                nonclaims=['No full spatial metric evolution or matched MOND galaxy',
                           'A real zero of a continuous symbol is not automatically an eigenvalue of a bounded spatial problem',
                           'No complete PPN, strong-coupling, endpoint or empirical certificate'])


def completion_status(result,strict=False):
    if not result['checks'] or not all(result['checks'].values()):return 1
    return 2 if strict else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    result=report()
    print(json.dumps(result,indent=2,default=lambda value:str(value) if isinstance(value,s.Basic) else mp.nstr(value,35)))
    raise SystemExit(completion_status(result,args.require_full_closure))
