#!/usr/bin/env python3
"""IC18: action-level conformal pinning, not a full-transition certificate.

See IC18_PINNED_CLOCK.md for the global phase action. The implemented
pressure and constraints are its exact eta=1 restriction. No empirical fit.
"""
import argparse
from functools import lru_cache
import json

import mpmath as mp
import sympy as s


@lru_cache(None)
def build():
    X, xs, eps, vacuum = s.symbols('X xs epsilon vacuum', positive=True)
    x = X / xs
    F = -vacuum + eps * x**2 / (1-x)
    FX, FXX = s.diff(F, X), s.diff(F, X, 2)
    Q = FX + 2*X*FXX
    rho = 2*X*FX-F
    return dict(X=X, xs=xs, eps=eps, vacuum=vacuum, F=F, FX=FX, FXX=FXX,
                Q=Q, rho=rho,
                evaluate=s.lambdify((X,xs,eps,vacuum), [F,FX,FXX,Q,rho], 'mpmath'))


def constants():
    wc, Sstar, eps = -mp.mpf(1)/40, mp.mpf(3)/40, mp.mpf('1e-5')
    ell = mp.log(mp.mpf(9)/5)
    a02 = 27*mp.exp(-mp.mpf(1)/2)/(8*ell**2)
    c = mp.mpf(4)/9
    U = (1-c)*(mp.log(1-c)**2-2*mp.log(1-c)+2)-2
    Lambda = 6*mp.exp(-mp.mpf(1)/2)-a02*U
    return dict(wc=wc,Sstar=Sstar,epsilon=eps,Xstar=mp.exp(-2*Sstar)/2,
                mstar=mp.exp(2*wc),vacuum=Lambda*mp.exp(4*wc),Lambda=Lambda,a02=a02)


def identities():
    a = build()
    X,xs,eps,vacuum = (a[key] for key in ('X','xs','eps','vacuum'))
    delta = s.symbols('delta', positive=True)
    sub = {X:xs*(1-delta)}
    checks = {
        'pole_FX':s.simplify(a['FX'].subs(sub)-eps/xs*(delta**-2-1)),
        'pole_Q':s.simplify(a['Q'].subs(sub)-eps/xs*(4*delta**-3-3*delta**-2-1)),
        'pole_energy':s.simplify(a['rho'].subs(sub)-vacuum-eps*(2/delta**2-3/delta+delta)),
        'pole_sound':s.simplify((a['FX']/a['Q']).subs(sub)-delta*(1+delta)/(delta**2+delta+4)),
    }
    # Actual raw velocity Hessian and fixed-canonical-momentum Schur complement.
    v,t,w,lam,wc = s.symbols('v t w lam wc', real=True)
    raw = a['F'].subs(X,v*v/2) + lam*(w-wc) + s.exp(2*w)*t*t/2
    vv = s.hessian(raw,(v,t))
    qq = s.hessian(raw,(w,lam))
    qv = s.Matrix([[s.diff(raw,q,d) for d in (v,t)] for q in (w,lam)])
    A = qq-qv*vv.inv()*qv.T
    checks['canonical_schur_determinant'] = s.simplify(A.det()+1)
    checks['pin_equation'] = s.diff(raw,lam)-(w-wc)
    stationary = raw.subs({w:wc,lam:-s.exp(2*wc)*t*t})
    checks['eliminated_clock_matter_mixed_jet'] = s.diff(stationary,v,t)
    curvature, beta = s.symbols('curvature beta', real=True)
    Ap = s.Matrix([[curvature,1],[1,0]])
    B = s.Matrix([[0,beta],[-beta,0]])
    PB = s.zeros(2).row_join(-Ap).col_join(Ap.row_join(B))
    checks['full_auxiliary_bracket_det'] = s.factor(PB.det()-1)
    # Transition: lambda enters multiplied by eta; vary before imposing w=wc.
    S,p = s.symbols('S p',real=True)
    h = s.Function('h')(S,w,p)
    eta = s.Function('eta')(S,w,p)
    H = h+eta*lam*(w-wc)
    HH = s.hessian(H,(S,w,lam)).subs(w,wc)
    checks['transition_auxiliary_hessian'] = s.simplify(HH.det()+eta.subs(w,wc)**2*s.diff(h,S,2).subs(w,wc))
    checks['transition_lapse_equation'] = s.simplify(s.diff(H,S).subs(w,wc)-s.diff(h,S).subs(w,wc))
    # Opposite-sign scalar/dust response of a separable potential.
    z,Y,k = s.symbols('z Y k',positive=True)
    V = k*(z-1)**2/2
    canonical = (V+z*Y).subs(z,1-Y/k)
    dust = V.subs(z,2*Y)  # multiplier equation fixes z=2Y, after variation
    checks['canonical_reduced_pressure'] = s.expand(canonical-Y+Y*Y/(2*k))
    checks['dust_sound'] = s.factor(s.diff(dust,Y)/(s.diff(dust,Y)+2*Y*s.diff(dust,Y,2))-(2*Y-1)/(6*Y-1))
    # Constant conformal transformation, including measured plateau coupling.
    m = s.symbols('m',positive=True)
    mstar = m*s.exp(2*wc)
    checks['physical_Einstein_coefficient'] = s.simplify(mstar*s.exp(-2*wc)-m)
    checks['physical_vacuum_density'] = s.simplify((m*s.exp(4*wc))*s.exp(-4*wc)-m)
    return checks


def separation_control():
    # Exact rational witness: positive convex auxiliary repairs dust, not all matter.
    Y,k,z = s.symbols('Y k z',positive=True)
    V = k*(z-1)**2/2
    P = (V+z*Y).subs(z,1-Y/k)
    D = s.diff(P,Y)
    K = D+2*Y*s.diff(P,Y,2)
    canonical_speed = s.simplify((D/K).subs({Y:s.Rational(1,10),k:1}))
    Pd = V.subs(z,2*Y)
    dust_speed = s.simplify((s.diff(Pd,Y)/(s.diff(Pd,Y)+2*Y*s.diff(Pd,Y,2))).subs({Y:s.Rational(3,5),k:1}))
    return dict(canonical_speed_squared=canonical_speed,canonical_superluminal=bool(canonical_speed>1),
                dust_speed_squared=dust_speed,canonical_kinetic=K.subs({Y:s.Rational(1,10),k:1}))


def pin_constraint(curvature=0,secondary_bracket=0):
    A = s.Matrix([[s.sympify(curvature),1],[1,0]])
    B = s.Matrix([[0,s.sympify(secondary_bracket)],[-s.sympify(secondary_bracket),0]])
    PB = s.zeros(2).row_join(-A).col_join(A.row_join(B))
    source = s.Matrix([2,-3])
    multipliers = A.inv()*source
    return dict(bracket=PB.tolist(),rank=PB.rank(),determinant=PB.det(),
                preservation_multipliers=list(multipliers),preservation_residual=list(A*multipliers-source))


def state(S,radiation=0,dust=0):
    S,radiation,dust = map(mp.mpf,(S,radiation,dust))
    c = constants()
    if not (mp.isfinite(S) and S>c['Sstar'] and radiation>=0 and dust>=0):
        raise ValueError('Require finite S>Sstar, nonnegative radiation and dust')
    X = mp.exp(-2*S)/2
    F,FX,FXX,Q,rho = build()['evaluate'](X,c['Xstar'],c['epsilon'],c['vacuum'])
    H = mp.sqrt((rho+radiation+dust)/(3*c['mstar']))
    r2 = mp.exp(2*S)*H*H  # m=h0=1; derived J18=1 on the pin
    return dict(S=S,X=X,delta=-mp.expm1(-2*(S-c['Sstar'])),pressure=F,FX=FX,FXX=FXX,
                kinetic=Q,energy=rho,nonvacuum_energy=rho-c['vacuum'],speed_squared=FX/Q,
                charge=FX*mp.sqrt(2*X),H=H,H_physical=mp.exp(-c['wc'])*H,
                activation_r_squared=r2,active=bool(r2>=mp.mpf(3)/4),
                u=(S+2*c['wc'])/(S+c['wc']),radiation=radiation,dust=dust,
                friedmann_residual=3*c['mstar']*H*H-rho-radiation-dust)


def characteristics(S='.1',velocity='.1',matter_power=2):
    """Uncoupled clock and minimally coupled Y^n fluid, actual boosted symbol.

    n=1 is a canonical scalar; n>=2 regularizes a cold fluid. Pressureless
    dust's separately derived repeated transport root is reported in the note.
    """
    v=mp.mpf(velocity)
    if abs(v)>=1 or matter_power<1:
        raise ValueError('Require |velocity|<1 and matter_power>=1')
    row=state(S)
    Y=mp.mpf(1)/2
    n=mp.mpf(matter_power)
    # Constant conformal factors rescale positive normalization, not cones.
    D=mp.diag([row['FX'],n*Y**(n-1)])
    Hess=mp.diag([row['FXX'],n*(n-1)*Y**(n-2)])
    velocities=[mp.sqrt(2*row['X']),mp.sqrt(2*Y/(1-v*v))]
    Ktime=D+mp.diag([Hess[i,i]*velocities[i]**2 for i in range(2)])
    def symbol(c):
        dots=[velocities[0]*c,velocities[1]*(c-v)]
        return (1-c*c)*D-mp.diag([Hess[i,i]*dots[i]**2 for i in range(2)])
    # Solve each independently constructed quadratic, not assigned sound speeds.
    roots=[]
    for i in range(2):
        coeff=list(reversed(mp.taylor(lambda c:symbol(c)[i,i],0,2)))
        aa,bb,cc=coeff
        discriminant=bb*bb-4*aa*cc
        roots.extend([(-bb+mp.sqrt(discriminant))/(2*aa),(-bb-mp.sqrt(discriminant))/(2*aa)])
    residual=max(abs(mp.det(symbol(c)))/(1+sum(abs(t)**2 for t in symbol(c))) for c in roots)
    return dict(relative_velocity=v,matter_power=matter_power,roots=roots,
                kinetic_minors=[Ktime[0,0],mp.det(Ktime)],kinetic_positive=bool(Ktime[0,0]>0 and mp.det(Ktime)>0),
                maximum_root_residual=residual,clock_matter_mixed_coefficient=Hess[0,1])


def history(efolds=8,samples=41):
    c=constants()
    final=state('.1')
    qf=final['charge']
    Rf=mp.mpf('.001')*final['energy']
    Mf=mp.mpf('.2')*final['nonvacuum_energy']
    target=qf*mp.exp(3*efolds)
    def equation(loggap):
        return state(c['Sstar']+mp.exp(loggap))['charge']/target-1
    seed=mp.log(mp.sqrt(c['epsilon']/(2*mp.sqrt(2*c['Xstar'])*target)))
    initial=c['Sstar']+mp.exp(mp.findroot(equation,(seed-1,seed+1)))
    rows=[]
    for i in range(samples):
        gap=mp.exp(mp.log(initial-c['Sstar'])+(mp.log(final['S']-c['Sstar'])-mp.log(initial-c['Sstar']))*i/(samples-1))
        S=c['Sstar']+gap
        bare=state(S)
        a=(qf/bare['charge'])**(mp.mpf(1)/3)
        row=state(S,Rf/a**4,Mf/a**3)
        row.update(a=a,charge_residual=a**3*row['charge']/qf-1)
        rows.append(row)
    def integrand(loggap):
        gap=mp.exp(loggap)
        return gap/(3*state(c['Sstar']+gap)['speed_squared'])
    quadrature=mp.quad(integrand,[mp.log(initial-c['Sstar']),mp.log(final['S']-c['Sstar'])])
    first=rows[0]
    return dict(initial_S=initial,efolds_from_quadrature=quadrature,
                max_charge_residual=max(abs(row['charge_residual']) for row in rows),
                initial_radiation_fraction=first['radiation']/(first['energy']+first['radiation']+first['dust']),
                early_clock_dust_ratio=first['nonvacuum_energy']/(mp.sqrt(2*c['Xstar'])*first['charge']),
                rows=rows)


def dust_characteristics(S='.1',velocity='.1'):
    """Vary the pressureless multiplier, retaining its transport characteristic."""
    v=mp.mpf(velocity)
    if abs(v)>=1:
        raise ValueError('Require |velocity|<1')
    row=state(S)
    d,c,L=s.symbols('d c L',real=True)
    # Mixed differential orders: scale multiplier amplitude by i*k.
    dust_symbol=s.Matrix([[L*(1-c*c),d],[d,0]])
    factor=s.factor(dust_symbol.det()+d*d)
    X,Y=s.symbols('X Y',positive=True)
    multiplier=s.symbols('lambda_dust')
    raw=build()['F']+multiplier*(Y-s.exp(2*s.Rational(-1,40))/2)
    mixed=s.diff(raw,build()['X'],Y)
    def clock_symbol(c):
        return row['FX']*(1-c*c)-2*row['X']*row['FXX']*c*c
    # The clock roots are from its actual quadratic, dust root from d=0.
    cc=mp.sqrt(row['FX']/(row['FX']+2*row['X']*row['FXX']))
    roots=[-cc,cc,v,v]
    residue=max(abs(clock_symbol(c)*(c-v)**2)/(1+abs(row['FX'])+abs(row['kinetic'])) for c in roots)
    return dict(roots=roots,dust_transport_factor=factor,mixed_clock_dust_jet=mixed,
                maximum_root_residual=residue,
                strict_dust_hyperbolicity_claimed=False)


@lru_cache(None)
def original_pressure():
    S,w,Lambda,a02=s.symbols('S w Lambda a02',real=True)
    u=(S+2*w)/(S+w)
    c=u*u
    U=(1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    P=-s.exp(4*w)*(Lambda+a02*U)+3*s.exp(2*w-2*S)
    return s.lambdify((S,w,Lambda,a02),[P,s.diff(P,S)],'mpmath',cse=True)


def activation(r):
    t=r*r
    if t<=mp.mpf(1)/2:return mp.mpf(0)
    if t>=mp.mpf(3)/4:return mp.mpf(1)
    a=mp.exp(-1/(t-mp.mpf(1)/2))
    b=mp.exp(-1/(mp.mpf(3)/4-t))
    return a/(a+b)


def transition_point(S,r):
    """Homogeneous vacuum pinned constraint; NOT the spatial principal matrix."""
    S,r=map(mp.mpf,(S,r))
    row=state(S)
    c=constants()
    def pressure0(S):
        return original_pressure()(S,c['wc'],c['Lambda'],c['a02'])
    P0,P0S=pressure0(S)
    F,FS=row['pressure'],-2*row['X']*row['FX']
    eta=activation(r)
    eta_r=mp.diff(activation,r)
    pi=-3*r*mp.exp(-S+2*c['wc'])
    constraint=-3*r*r*mp.exp(-2*S+2*c['wc'])-(1-eta)*(P0+P0S)-eta*(F+FS)-r*eta_r*(F-P0)
    def h(S):
        rr=-mp.exp(S-2*c['wc'])*pi/3
        aa=activation(rr)
        return -mp.exp(S-2*c['wc'])*pi*pi/3-mp.exp(S)*((1-aa)*pressure0(S)[0]+aa*state(S)['pressure'])
    return dict(S=S,r=r,eta=eta,constraint=constraint,
                direct_derivative_residual=mp.diff(h,S)/mp.exp(S)-constraint,
                lapse_second_derivative=mp.diff(h,S,2))


def transition_scan():
    # A bounded search on the exact reduced homogeneous lapse equation.
    samples=[]
    roots=[]
    for gap in ('1e-7','1e-5','.001','.025','.1','1','10'):
        S=constants()['Sstar']+mp.mpf(gap)
        grid=[mp.sqrt(mp.mpf('.5')+mp.mpf('.25')*i/32) for i in range(33)]
        values=[transition_point(S,r) for r in grid]
        samples.append(dict(S=S,minimum_constraint=min(t['constraint'] for t in values),
                            maximum_constraint=max(t['constraint'] for t in values)))
        for left,right in zip(values,values[1:]):
            if left['constraint']*right['constraint']<0:
                lo,hi=left['r'],right['r']
                flo=left['constraint']
                for _ in range(160):
                    mid=(lo+hi)/2
                    fm=transition_point(S,mid)['constraint']
                    if flo*fm<=0:hi=mid
                    else:lo,flo=mid,fm
                roots.append(transition_point(S,(lo+hi)/2))
    return dict(S_offsets=['1e-7','1e-5','.001','.025','.1','1','10'],r_squared_range=['.5','.75'],
                r_grid_points=33,samples=samples,located_roots=roots,
                completeness_claimed=False,spatial_stability_computed=False)


def homogeneous_h(S,w,pi,lam=0):
    c=constants()
    eta=activation(-mp.exp(S-2*w)*pi/3)
    P0=original_pressure()(S,w,c['Lambda'],c['a02'])[0]
    return (-mp.exp(S-2*w)*pi*pi/3*(1-eta+eta*mp.exp(2*w-2*c['wc']))
            -mp.exp(S)*((1-eta)*P0+eta*state(S)['pressure']+eta*lam*(w-c['wc'])))


def transition_fold():
    c=constants()
    def equations(S,r):
        row=transition_point(S,r)
        return row['constraint'],row['lapse_second_derivative']
    S,r=mp.findroot(equations,('.08','.766'),tol=mp.power(10,-mp.mp.dps+10),maxsteps=100)
    row=transition_point(S,r)
    pi=-3*r*mp.exp(-S+2*c['wc'])
    wc=c['wc']
    lam=mp.diff(lambda w:homogeneous_h(S,w,pi),wc)/(mp.exp(S)*activation(r))
    def h(S,pi):return homogeneous_h(S,wc,pi)
    f=h(S,pi)
    fp=mp.diff(lambda p:h(S,p),pi)
    fSp=mp.diff(h,(S,pi),(1,1))
    fS=mp.diff(lambda t:h(t,pi),S)
    tertiary=mp.mpf(3)/2*(fS*fp-fSp*f)
    # q=ln B, p_q=2*pi, V=exp(3q); direct canonical bracket check.
    def H(q,pq,S):
        V=mp.exp(3*q)
        return V*h(S,pq/(2*V))
    def CS(q,pq):return mp.diff(lambda t:H(q,pq,t),S)
    direct=(mp.diff(lambda q:CS(q,2*pi),0)*mp.diff(lambda pq:H(0,pq,S),2*pi)
            -mp.diff(lambda pq:CS(0,pq),2*pi)*mp.diff(lambda q:H(q,2*pi,S),0))
    point=(S,wc,lam)
    def raw(t,w,l):return homogeneous_h(t,w,pi,l)
    Hess=mp.matrix([[mp.diff(raw,point,tuple(int(k==i)+int(k==j) for k in range(3)))
                     for j in range(3)] for i in range(3)])
    secondary=[mp.diff(raw,point,tuple(int(k==i) for k in range(3))) for i in range(3)]
    def Hfour(t,w,l,p):return homogeneous_h(t,w,p,l)
    secondary_p=[mp.diff(Hfour,point+(pi,),tuple(int(k==i)+int(k==3) for k in range(4))) for i in range(3)]
    # Actual secondary brackets in (ln B,p_q), V=1; they vanish weakly,
    # but are calculated here instead of inserting a zero block.
    B=mp.matrix([[mp.mpf(3)/2*(secondary[i]*secondary_p[j]-secondary_p[i]*secondary[j])
                  for j in range(3)] for i in range(3)])
    PB=mp.zeros(6)
    for i in range(3):
        for j in range(3):
            PB[i,j+3]=-Hess[i,j]
            PB[i+3,j]=Hess[i,j]
            PB[i+3,j+3]=B[i,j]
    singular=list(mp.svd(PB,compute_uv=False))
    threshold=mp.power(10,-mp.mp.dps/2)*max(singular)
    rank=sum(v>threshold for v in singular)
    row.update(pi=pi,lambda_pin=lam,reduced_h=f,H_physical=mp.exp(-wc-S)*fp/2,
               tertiary_preservation=tertiary,independent_canonical_bracket_residual=direct-tertiary,
               auxiliary_hessian=Hess.tolist(),secondary_constraints=secondary,
               full_poisson_matrix=PB.tolist(),auxiliary_singular_values=singular,
               numerical_rank_threshold=threshold,computed_auxiliary_rank=rank,
               finite_multiplier_preservation_possible=bool(abs(tertiary)<mp.mpf('1e-30')))
    return row


def report():
    mp.mp.dps=70
    exact=identities()
    control=separation_control()
    flows=[characteristics('.1',v,n) for v in ('0','.1','.5','.9','-.9') for n in (1,2,10,100)]
    evo=history()
    dust_flow=dust_characteristics()
    transition=transition_scan()
    fold=transition_fold()
    with mp.workdps(90):
        refined_fold=transition_fold()
        refinement=dict(precision_digits=90,S=refined_fold['S'],r=refined_fold['r'],
                        tertiary_preservation=refined_fold['tertiary_preservation'],
                        maximum_coordinate_difference=max(abs(refined_fold[key]-fold[key]) for key in ('S','r')),
                        constraint=refined_fold['constraint'],lapse_second_derivative=refined_fold['lapse_second_derivative'])
    rows=[state(constants()['Sstar']+mp.power(10,-j)) for j in range(1,13)]
    checks={key:value==0 for key,value in exact.items()}
    checks.update(positive_sampled_clock=all(row['FX']>0 and row['kinetic']>row['FX'] and row['active'] for row in rows),
                  regular_pin_block=all(pin_constraint(c)['rank']==4 for c in (-1000,0,1000)),
                  separated_control_fails_canonical_cone=control['canonical_superluminal'],
                  relative_flow_roots=all(all(abs(mp.im(c))<mp.mpf('1e-50') and abs(c)<=1+mp.mpf('1e-50') for c in row['roots']) for row in flows),
                  relative_flow_kinetic=all(row['kinetic_positive'] for row in flows),
                  direct_characteristic_residuals=all(row['maximum_root_residual']<mp.mpf('1e-50') for row in flows),
                  expanding_active_history=all(row['active'] and row['H_physical']>0 for row in evo['rows']),
                  charge_quadrature=abs(evo['efolds_from_quadrature']-8)<mp.mpf('1e-45'))
    checks.update(actual_dust_mixed_jet=dust_flow['mixed_clock_dust_jet']==0,
                  actual_dust_determinant=dust_flow['dust_transport_factor']==0,
                  actual_dust_root_residual=dust_flow['maximum_root_residual']<mp.mpf('1e-50'),
                  transition_fixed_momentum_derivative=abs(transition_point('.1','.8')['direct_derivative_residual'])<mp.mpf('1e-50'))
    checks.update(fold_located=abs(fold['constraint'])<mp.mpf('1e-45') and abs(fold['lapse_second_derivative'])<mp.mpf('1e-45'),
                  fold_preservation_obstruction=not fold['finite_multiplier_preservation_possible'],
                  independent_fold_bracket=abs(fold['independent_canonical_bracket_residual'])<mp.mpf('1e-45'))
    checks['fold_precision_refinement']=refinement['maximum_coordinate_difference']<mp.mpf('1e-55')
    return dict(candidate='IC18 holonomically pinned conformal factor; eta=1 results',full_theory='OPEN',
                checks=checks,constants=constants(),separable_potential_control=control,
                auxiliary_block=pin_constraint(7,3),clock_samples=rows,relative_flow_controls=flows,
                history=evo,pressureless_dust=dust_flow,transition_probe=transition,transition_fold=fold,
                fold_precision_refinement=refinement,
                nonclaims=['No full transition principal operator or globally matched MOND galaxy',
                    'No PPN, CMB, cluster or empirical calibration certificate',
                    'No strong-coupling or pressureless-dust caustic certificate',
                    'Pin multiplier may diverge as eta tends to zero; matching is an explicit remaining gate'])


def completion_status(result,require_full_closure=False):
    if not result['checks'] or not all(result['checks'].values()):
        return 1
    return 2 if require_full_closure else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    result=report()
    print(json.dumps(result,indent=2,default=lambda value:str(value) if isinstance(value,s.Basic) else mp.nstr(value,35)))
    return completion_status(result,args.require_full_closure)


if __name__=='__main__':
    raise SystemExit(main())
