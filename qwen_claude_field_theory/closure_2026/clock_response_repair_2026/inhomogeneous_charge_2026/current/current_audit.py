#!/usr/bin/env python3
"""Same-action shift current, charge balance, and bounded radial root audit.

No Einstein solution or coefficient reconstruction is performed. A static
metric is deliberately NOT assumed to imply a stationary shift density.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
from scipy.optimize import brentq
import sympy as s

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parent.parent


@lru_cache(maxsize=1)
def covariant():
    """Derive the current in a normal frame; metric compatibility covariantizes it."""
    PX,s0,WY,gamma,Xstar,Ystar=s.symbols('PX s0 WY gamma Xstar Ystar',real=True)
    grad=s.Matrix(s.symbols('c0:4',real=True))
    H=s.Matrix(4,4,lambda i,j:s.Symbol('h%d%d'%tuple(sorted((i,j))),real=True))
    eta=s.diag(-1,1,1,1)
    X=-(grad.T*eta*grad)[0];Y=sum(grad[k]**2 for k in (1,2,3))
    box=sum(eta[k,k]*H[k,k] for k in range(4))
    density=PX*(X-Xstar)+s0*WY*(Y-Ystar)+gamma*X*box
    # Generalized Noether momentum: dL/d chi_mu - partial_nu dL/d chi_mu_nu.
    current=s.Matrix([s.expand(s.diff(density,grad[mu])-sum(
        gamma*eta[mu,nu]*s.diff(X,grad[k])*H[nu,k]
        for nu in range(4) for k in range(4))) for mu in range(4)])
    return dict(symbols=dict(PX=PX,s0=s0,WY=WY,gamma=gamma,gradient=grad,hessian=H),
        current=current,
        formula='J^mu=-2(P_X+gamma Box chi) nabla^mu chi + 2 s W_Y h^{mu nu} chi_nu - gamma nabla^mu X')


@lru_cache(maxsize=1)
def radial():
    """Independent radial reduced-action and covariant-current evaluations.

Metric -N(r)^2 dt^2+dr^2/F(r)+R(r)^2 dSigma^2. R=r for a
sphere, R=constant for a plane; tau=t, chi=Q*t+psi(r).
"""
    N,F,R=s.symbols('N F R',positive=True)
    p,Q,gamma,PX,WY,Np,Fp,Rp,pp,PXtau=s.symbols('p Q gamma PX WY Np Fp Rp pp PXtau',real=True)
    Xstar,Ystar,P,V,W=s.symbols('Xstar Ystar P V W',real=True)
    K=s.symbols('K',real=True)
    D=N*R**2/s.sqrt(F);X=Q**2/N**2-F*p**2;Y=F*p**2
    rates={N:Np,F:Fp,R:Rp,p:pp}
    def dr(expr):return s.expand(sum(s.diff(expr,z)*rate for z,rate in rates.items()))
    box=s.simplify(dr(D*F*p)/D)
    raw=D*(P+PX*(X-Xstar)-V+(W+WY*(Y-Ystar))/N+gamma*X*box)
    # Per unit solid angle: dL/d psi' - d_r[dL/d psi''] = D J^r.
    reduced=s.simplify((s.diff(raw,p)-dr(s.diff(raw,pp)))/D)
    direct=s.simplify(-2*(PX+gamma*box)*F*p+2*WY*F*p/N-gamma*F*dr(X))
    replace={Rp:R*(K-Np/N)/2}
    reduced=s.factor(reduced.subs(replace));direct=s.factor(direct.subs(replace))
    jt=2*Q*(PX+gamma*box)/N**2
    symbols=dict(N=N,F=F,R=R,p=p,Q=Q,gamma=gamma,PX=PX,WY=WY,Np=Np,Fp=Fp,
                 Rp=Rp,pp=pp,PXtau=PXtau,K=K)
    return dict(symbols=symbols,Jr_reduced=reduced,Jr_covariant=direct,Jt=jt,
        dJt_dt=s.diff(jt,PX)*PXtau,box=box,volume_per_unit_angle=D,
        K_definition='K=Nprime/N+2Rprime/R; R=r for spheres, R=constant for planes',
        reduced_action_warning='The reduced radial momentum gives J^r, but its radial derivative alone is NOT the full chi Euler equation when partial_t(D J^t) is nonzero.')


@lru_cache(maxsize=1)
def continuity():
    charge_rate,center_flux=s.symbols('charge_rate center_flux',real=True)
    r,N0,j0=s.symbols('r N0 j0',positive=True)
    # Integrating partial_t(D Jt)+partial_r(D Jr)=0 over a ball.
    outward_flux=center_flux-charge_rate
    return dict(symbols=dict(charge_rate=charge_rate,center_flux=center_flux),
        outward_flux=outward_flux,regular_center_limit=s.limit(4*s.pi*N0*r**2*j0,r,0),
        local_law='partial_t[(N R^2/sqrt(F)) J^t]+partial_r[(N R^2/sqrt(F)) J^r]=0',
        spherical_charge='C(<r,t)=4 pi integral_0^r (N u^2/sqrt(F)) J^t du',
        regularity='A smooth center has N finite positive, F->1 and finite physical radial current, hence center flux=0.',
        stationarity='Only partial_t C=0 plus no center flux implies zero outer flux. A decreasing C permits positive outward flux.')


@lru_cache(maxsize=1)
def root_algebra():
    p,N,d,D,S,H=s.symbols('p N d D S H',real=True)
    polynomial=N**2*S*H**2-d**2*p**2*D**2
    A0,AY,gamma,r,k1,k3=s.symbols('A0 AY gamma r k1 k3',real=True)
    center_p=k1*r+k3*r**3
    expansion=s.expand(r*(A0+AY*center_p**2)+2*gamma*center_p)
    solution=s.solve([expansion.coeff(r,1),expansion.coeff(r,3)],(k1,k3),dict=True)[0]
    residual=s.expand(expansion.subs(solution))
    return dict(symbols=dict(p=p,N=N,d=d,D=D,S=S,H=H),polynomial=polynomial,
        center_symbols=dict(A0=A0,AY=AY,gamma=gamma),center_slope=solution[k1],center_cubic=solution[k3],
        center_residual_through_cubic=s.expand(residual.coeff(r,1)*r+residual.coeff(r,3)*r**3),
        definitions=dict(A='d U/[U-2d(Q^2/N^2-Fp^2)]+3gamma qbar Hbar-d/[N sqrt(1+Fp^2/ell)]',
            D='U-2d Q^2/N^2+2d Fp^2',S='1+Fp^2/ell',
            a='gamma F (Nprime/N+2Rprime/R)',c='3gamma qbar Hbar',
            e='gamma Q^2 Nprime/N^3',H='(a p^2+c p-e)D+d U p'),
        all_roots='Exactly the real p with D>0, S>0, polynomial=0 and p H>=0, for N,d>0. The last condition rejects roots introduced by squaring.',
        maximum_degree=10,
        special_cases=['gamma=0: p=0 or A(p^2,t)=0; A nonzero is an additional hypothesis.',
            'gamma!=0 and Nprime!=0 and Q!=0: p=0 is not even a zero-current root.',
            'flat sphere: p=0 or A(p^2,t)+2gamma p/r=0.',
            'flat plane: p=0 or A(p^2,t)=0; the one-dimensional cubic radial current cancels exactly.'])


def accept_squared_candidate(p,H,D):
    """For a polynomial candidate with N,d,S positive, enforce domain and sign."""
    return bool(D>0 and p*H>=0)


@lru_cache(maxsize=1)
def frozen_slice():
    """Isolate every real root of one exact rationalized source snapshot.

The geometry is a flat spherical *test slice*, r=1 in source units, not an
Einstein solution or galaxy model. Coefficients come from the source function
at (a,m,v)=(1,.1,.5), physical Q from the archived background, gamma unchanged.
The exact polynomial uses decimal serialization of those binary64 evaluations;
its all-roots statement is confined to that recorded polynomial.
"""
    path=REPAIR/'nonlinear_evolution_2026/constitutive.py'
    spec=importlib.util.spec_from_file_location('unchanged_current_constitutive',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    bg,flow,names,jets=module.functions()
    raw=bg(1.,.1,.5)
    archive=json.loads((REPAIR/'cosmological_bridge_2026/radiation_002/result.json').read_text())
    sample=archive['samples'][0]
    values=dict(qbar=float(raw[0]),U=float(raw[1]),d=float(raw[2]),Hbar=float(raw[3]),
                ell=float(raw[4]),Q=float(sample['q']),gamma=float(archive['parameters']['gamma']))
    qbar,U,d,Hbar,ell,Q,gamma=(s.Rational(str(values[k])) for k in ('qbar','U','d','Hbar','ell','Q','gamma'))
    p=s.symbols('p',real=True);D=U-2*d*Q**2+2*d*p**2;S=1+p**2/ell
    c=3*gamma*qbar*Hbar;A=d*U/D+c-d/s.sqrt(S)
    H=(2*gamma*p**2+c*p)*D+d*U*p
    poly=s.Poly(s.expand(S*H**2-d**2*p**2*D**2),p)
    intervals=poly.intervals(eps=s.Rational(1,10**32))
    candidates=[];accepted=[]
    for (lohi,multiplicity) in intervals:
        lo,hi=lohi;point=(lo+hi)/2
        domain=bool(D.subs(p,point)>0)
        sign_ok=accept_squared_candidate(point,H.subs(p,point),D.subs(p,point))
        # Exact Sturm counts prevent a midpoint sign from misclassifying a root.
        sign_certified=(bool(H.subs(p,point)*point>=0) if lo==hi else
            bool(lo*hi>0 and s.Poly(H,p).count_roots(lo,hi)==0
                 and s.Poly(D,p).count_roots(lo,hi)==0))
        residual=s.N(-2*(A*point+2*gamma*point**2).subs(p,point),60)
        keep=domain and sign_ok
        row=dict(p=float(point),interval=[str(lo),str(hi)],multiplicity=multiplicity,
            domain=domain,unsquared_sign=sign_ok,sign_certified=sign_certified,current=float(residual),accepted=keep,
            X=float(Q**2-point**2),chi_timelike=bool(Q**2-point**2>0),
            coefficient_A=float(s.N(A.subs(p,point),30)))
        candidates.append(row)
        if keep:accepted.append(row)
    qjets=dict(zip(names,jets(*raw,float(Q**2),0.,float(gamma))))
    time_rows=[]
    for Y in [0.,.0001,.001,values['ell'],.9*values['Q']**2]:
        source=dict(zip(names,jets(*raw,values['Q']**2-Y,Y,values['gamma'])))
        time_rows.append(dict(Y=Y,X=values['Q']**2-Y,P_Xtau=float(source['P_Xt']),
            dJt_dt=float(2*values['Q']*source['P_Xt'])))
    classified=all(r['sign_certified'] and (abs(r['current'])<1e-20 if r['accepted'] else
                    (not r['domain'] or not r['unsquared_sign'])) for r in candidates)
    if not classified:raise AssertionError('Root classification residual failed')
    # Independent float64 source comparison at every accepted root.
    for row in accepted:
        source=dict(zip(names,jets(*raw,float(Q**2)-row['p']**2,row['p']**2,float(gamma))))
        source_A=float(source['P_X']-source['W_Y'])
        row['source_float64_current']=-2*(source_A*row['p']+2*float(gamma)*row['p']**2)
        if abs(row['source_float64_current'])>1e-9:raise AssertionError('Source current mismatch')
    radius=1e-8
    def source_at(gradient):
        return dict(zip(names,jets(*raw,values['Q']**2-gradient**2,gradient**2,values['gamma'])))
    def center_equation(gradient):
        original=source_at(gradient)
        return radius*(original['P_X']-original['W_Y'])+2*values['gamma']*gradient
    center_p=brentq(center_equation,-.001,-1e-12,xtol=1e-17,rtol=1e-14)
    original=source_at(center_p);original_A=float(original['P_X']-original['W_Y'])
    Ap=-2*center_p*float(original['P_XX']+original['W_YY'])
    center_pp=-original_A/(2*values['gamma']+radius*Ap)
    original_box=center_pp+2*center_p/radius
    original_Xprime=-2*center_p*center_pp
    covariant_current=(-2*(original['P_X']+values['gamma']*original_box)*center_p
                       +2*original['W_Y']*center_p-values['gamma']*original_Xprime)
    reduced_current=-2*(original_A*center_p+2*values['gamma']*center_p**2/radius)
    witness=dict(r=radius,p=center_p,pp=center_pp,X=values['Q']**2-center_p**2,Y=center_p**2,
        bracket=[-.001,-1e-12],xtol=1e-17,rtol=1e-14,
        reduced_original_current=float(reduced_current),covariant_original_current=float(covariant_current),
        Jt=float(2*values['Q']*(original['P_X']+values['gamma']*original_box)),
        dJt_dt=float(2*values['Q']*original['P_Xt']),
        warning='An instantaneous regular-center zero-current branch on a prescribed flat test slice, not stationary Einstein data.')
    if not (witness['X']>0 and abs(covariant_current)<1e-16 and abs(reduced_current)<1e-16):
        raise AssertionError('Timelike center witness failed')
    return dict(coefficients=values,geometry=dict(N=1,F=1,Nprime=0,r=1),
        PXtau_at_p_zero=float(qjets['P_Xt']),dJt_dt_at_p_zero=float(2*float(Q)*qjets['P_Xt']),
        time_dependence_rows=time_rows,
        small_radius_witness=witness,
        polynomial_degree=poly.degree(),polynomial=str(poly.as_expr()),
        polynomial_coefficients_descending=[str(x) for x in poly.all_coeffs()],
        real_polynomial_roots=len(intervals),real_polynomial_roots_with_multiplicity=sum(k for _,k in intervals),
        candidates=candidates,accepted_roots=accepted,all_roots_classified=classified,
        scope='Exhaustive real-root isolation of one recorded rationalized polynomial; no assertion of global branch, Einstein constraints, timelike chi, stability, or persistent stationarity.',
        coefficient_policy='All coefficients are unchanged source evaluations. Exact rationals serialize this binary64 slice only; they are not new constitutive functions or fitted coefficients.')


def run():
    cov=covariant();rad=radial();balance=continuity();roots=root_algebra();numbers=frozen_slice()
    checks=dict(radial_action_matches_covariant=s.simplify(rad['Jr_reduced']-rad['Jr_covariant'])==0,
        radial_second_derivative_cancels=rad['symbols']['pp'] not in rad['Jr_reduced'].free_symbols,
        regular_center_has_zero_flux=balance['regular_center_limit']==0,
        all_snapshot_roots_classified=numbers['all_roots_classified'],
        nonzero_zero_flux_root_exists=any(abs(r['p'])>1e-6 for r in numbers['accepted_roots']),
        actual_clock_dependence_nonzero=abs(numbers['dJt_dt_at_p_zero'])>1e-10)
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,covariant_current=cov['formula'],
        radial_current=str(rad['Jr_reduced']),time_current=str(rad['Jt']),explicit_time_derivative=str(rad['dJt_dt']),
        geometric_convention=rad['K_definition'],reduced_action_warning=rad['reduced_action_warning'],
        continuity={k:v for k,v in balance.items() if k not in ('symbols','outward_flux','regular_center_limit')},
        root_algebra={k:v for k,v in roots.items() if k not in ('symbols','polynomial','center_symbols','center_slope','center_cubic','center_residual_through_cubic')},
        center_series=dict(slope=str(roots['center_slope']),cubic_coefficient=str(roots['center_cubic']),
            checked_residual_through_cubic=str(roots['center_residual_through_cubic']),
            scope='Flat spherical instantaneous zero-current branch. If gamma and A0 are nonzero, p=-(A0/2gamma)r+O(r^3) is nontrivial and regular; no time-stationarity or Einstein solution follows.'),
        frozen_slice=numbers,
        verdict=('Regular stationary charge with no center source cannot carry nonzero net outward shift flux. Charge depletion need not be stationary. Zero flux does not imply zero scalar gradient for this action.' if all(checks.values()) else 'Audit unresolved.'),
        non_claims=['No galaxy or full Einstein/scalar/clock solution has been constructed.',
            'No stability or physical admissibility follows from any isolated zero-current root.',
            'The polynomial root count is only for the recorded rationalized source snapshot.',
            'Time-varying charge, sources, singular centers, horizons, or nonstationary geometry alter the stationary-flux conclusion.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=run()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],verdict=result['verdict'],
        accepted_roots=result['frozen_slice']['accepted_roots'],
        dJt_dt_at_p_zero=result['frozen_slice']['dJt_dt_at_p_zero']),indent=2))
