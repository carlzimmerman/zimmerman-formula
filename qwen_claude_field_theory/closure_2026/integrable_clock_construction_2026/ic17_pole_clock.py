#!/usr/bin/env python3
"""Activated pole clock: new pressure, finite early-radiation witnesses.

The pole is evaluated only on its explicit active domain 0<2Xtilde<1.
Inactive static neighborhoods are defined directly with zero correction.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic10_local_clock as original


EPSILON='0.00001'


def eta_up(r):
    r2=r*r
    if r2<=mp.mpf(1)/2:return mp.mpf(0)
    if r2>=mp.mpf(3)/4:return mp.mpf(1)
    a=mp.exp(-1/(r2-mp.mpf(1)/2))
    b=mp.exp(-1/(mp.mpf(3)/4-r2))
    return a/(a+b)


def phase_delta(Xphysical,w,r,epsilon=EPSILON):
    x=2*mp.exp(2*w)*Xphysical
    if not (mp.isfinite(x) and x>0 and mp.isfinite(r)):
        raise ValueError('Require finite positive Xtilde and finite r')
    if not (r*r<mp.mpf(1)/2 or x<1):
        raise ValueError('Outside the open static-or-active pole action domain')
    activation=eta_up(r)
    if activation==0:return mp.mpf(0)
    return -activation*mp.exp(-4*w)*(mp.mpf(5)/64*x**16+mp.mpf(epsilon)*x*x/(1-x))


@lru_cache(None)
def build():
    old=original.build()
    S,w,X=old['S'],old['w'],old['X']
    epsilon=s.symbols('epsilon',positive=True)
    f=s.Rational(5,64)*(2*X)**16+epsilon*(2*X)**2/(1-2*X)
    P=old['P']+f
    expressions=s.Matrix([P,s.diff(P,w),s.diff(P,S),s.diff(P,w,2),s.diff(P,S,w),s.diff(P,S,2)])
    return dict(evaluate=s.lambdify((S,w,epsilon),expressions,'mpmath',cse=True))


def root(S):
    """Solve the unchanged root in u, using its derived small-S scale."""
    if S>mp.mpf('.001'):
        return original.state(S)['w']
    ell=mp.log(mp.mpf(9)/5)
    a02=27*mp.exp(-mp.mpf(1)/2)/(8*ell*ell)
    c=mp.mpf(4)/9
    U=(1-c)*(mp.log(1-c)**2-2*mp.log(1-c)+2)-2
    Lambda=6*mp.exp(-mp.mpf(1)/2)-a02*U
    scale=((4*Lambda-6)*S/(8*a02))**(mp.mpf(1)/5)
    equation=lambda u:original.build()['evaluate'](S,S*(u-1)/(2-u))[1]
    u=mp.findroot(equation,(scale*mp.mpf('.8'),scale*mp.mpf('1.2')),tol=mp.power(10,-mp.mp.dps+10))
    if not 0<u<1:raise ValueError('Auxiliary root left 0<u<1')
    return S*(u-1)/(2-u)


def state(S,radiation=0,epsilon=EPSILON):
    S,radiation,epsilon=map(mp.mpf,(S,radiation,epsilon))
    if S<=0 or radiation<0 or epsilon<=0:raise ValueError('Require S>0, radiation>=0, epsilon>0')
    w=root(S)
    P,Pw,PS,Pww,PSw,PSS=build()['evaluate'](S,w,epsilon)
    X=mp.exp(-2*S)/2
    eff=PSS-PSw*PSw/Pww
    FX,Q,Qbare=-PS/(2*X),(eff+PS)/(2*X),(PSS+PS)/(2*X)
    rho=-PS-P
    cs2=FX/Q
    wS=-PSw/Pww
    H=mp.sqrt((rho+radiation)/(3*mp.exp(-mp.mpf(1)/6))) if rho+radiation>0 else mp.nan
    Hphys=mp.exp(-w)*H*(1+3*cs2*wS)
    r=mp.exp(S-2*w-mp.mpf(1)/6)*H
    Acan=Pww-PSw*PSw/(PSS+PS)
    bracket=mp.matrix([[0,Acan],[-Acan,0]])
    sv=list(mp.svd(bracket,compute_uv=False))
    rank=sum(v>mp.mpf('1e-60') for v in sv)
    eta=eta_up(r)
    healthy=bool(FX>0 and Q>=FX and rho>0 and Hphys>0 and Qbare!=0 and rank==2)
    return dict(S=S,w=w,u=(S+2*w)/(S+w),X=X,delta=-mp.expm1(-2*S),P=P,PS=PS,
                PSS_effective=eff,FX=FX,kinetic=Q,bare_kinetic=Qbare,speed_squared=cs2,
                energy=rho,H=H,physical_H=Hphys,wS=wS,activation_r=r,eta=eta,
                constraint=Pw,auxiliary_schur=Acan,auxiliary_singular_values=sv,auxiliary_rank=rank,
                canonical_identity_residual=Acan-Pww*Q/Qbare,
                clock_charge_density=FX*mp.exp(-S),radiation=radiation,
                radiation_fraction=radiation/(rho+radiation),equation_of_state=P/rho,
                friedmann_residual=3*mp.exp(-mp.mpf(1)/6)*H*H-rho-radiation,
                admissible=healthy and eta==1)


def scan(samples=241):
    return [state(mp.exp(mp.log(mp.mpf('1e-12'))+(mp.log(mp.mpf('.3'))-mp.log(mp.mpf('1e-12')))*i/(samples-1))) for i in range(samples)]


def late_scan(samples=81):
    condensate=mp.findroot(lambda S:state(S)['FX'],('.5','.54'))
    end=condensate-mp.mpf('1e-10')
    return condensate,[state(mp.mpf('.3')+(end-mp.mpf('.3'))*i/(samples-1)) for i in range(samples)]


def history(efolds=8,final_S='.1',final_radiation_ratio='.001',samples=81):
    final=state(final_S)
    N=mp.mpf(efolds)
    qf=final['clock_charge_density']
    Rf=mp.mpf(final_radiation_ratio)*final['energy']
    C=Rf/qf**(mp.mpf(4)/3)
    # Solve in ln S, avoiding a numerical step outside the active pole domain.
    def solve_n(n):
        target=qf*mp.exp(-3*final['w']+3*n)
        equation=lambda logS:state(mp.exp(logS))['clock_charge_density']*mp.exp(-3*state(mp.exp(logS))['w'])/target-1
        seed=mp.log(mp.sqrt(mp.mpf(EPSILON)/(2*target)))
        logS=mp.findroot(equation,(seed-mp.mpf('.2'),seed+mp.mpf('.2')),tol=mp.power(10,-mp.mp.dps+12))
        return mp.exp(logS)
    initial_S=solve_n(N)
    # A log S grid resolves the approach to the pole; e-folds are recomputed.
    states=[]
    for i in range(samples):
        S=mp.exp(mp.log(initial_S)+(mp.log(final['S'])-mp.log(initial_S))*i/(samples-1))
        vacuum=state(S)
        q=vacuum['clock_charge_density']
        b=state(S,C*q**(mp.mpf(4)/3))
        abar=(qf/q)**(mp.mpf(1)/3)
        b.update(barred_a_relative_final=abar,
                 physical_a_relative_final=abar*mp.exp(b['w']-final['w']),
                 charge_ratio=abar**3*q/qf,
                 radiation_charge_ratio=abar**4*b['radiation']/Rf)
        states.append(b)
    physical=-mp.log(states[0]['physical_a_relative_final'])
    def physical_integrand(logS):
        b=state(mp.exp(logS))
        return b['S']*(1/(3*b['speed_squared'])+b['wS'])
    quadrature=mp.quad(physical_integrand,[mp.log(initial_S),mp.log(mp.mpf('.001')),mp.log(final['S'])])
    return dict(initial_S=initial_S,final_S=final['S'],physical_efolds=physical,
                physical_efolds_quadrature=quadrature,
                radiation_constant=C,final_radiation_ratio=mp.mpf(final_radiation_ratio),states=states)


def identities():
    X,eps,delta=s.symbols('X eps delta',positive=True)
    pole=eps*(2*X)**2/(1-2*X)
    FX=s.diff(pole,X)
    Q=FX+2*X*s.diff(pole,X,2)
    rho=2*X*FX-pole
    sub={X:(1-delta)/2}
    return dict(FX=s.simplify(FX.subs(sub)-2*eps*(delta**-2-1)),
                kinetic=s.simplify(Q.subs(sub)-eps*(8*delta**-3-6*delta**-2-2)),
                energy=s.simplify(rho.subs(sub)-eps*(2*delta**-2-3/delta+delta)),
                fluid_w=s.simplify((pole/rho).subs(sub)-delta/(2+delta)),
                sound=s.simplify((FX/Q).subs(sub)-delta*(1+delta)/(delta*delta+delta+4)))


def report():
    mp.mp.dps=80
    rows=scan()
    evolution=history()
    condensate,late=late_scan()
    show=lambda b:{k:mp.nstr(b[k],30) for k in ('S','u','w','FX','kinetic','speed_squared','energy','equation_of_state','physical_H','activation_r','eta','auxiliary_schur','constraint','canonical_identity_residual','radiation','radiation_fraction')}
    return dict(candidate='IC17 positive pole pressure with one-sided activation',epsilon=EPSILON,full_theory='OPEN',
                exact_checks={k:str(v) for k,v in identities().items()},
                scan=dict(S_min='1e-12',S_max='.3',samples=len(rows),unhealthy_samples=sum(not b['admissible'] for b in rows),
                          minimum_FX=mp.nstr(min(b['FX'] for b in rows),30),minimum_kinetic=mp.nstr(min(b['kinetic'] for b in rows),30),
                          maximum_cs_squared=mp.nstr(max(b['speed_squared'] for b in rows),30),minimum_r_squared=mp.nstr(min(b['activation_r']**2 for b in rows),30),
                          computed_auxiliary_ranks=sorted(set(b['auxiliary_rank'] for b in rows)),rows=list(map(show,rows))),
                late_FX_zero=mp.nstr(condensate,35),
                late_scan=dict(samples=len(late),S_start='.3',S_end=mp.nstr(late[-1]['S'],35),
                               unhealthy_samples=sum(not b['admissible'] for b in late),
                               final_state=show(late[-1])),
                radiation_history=dict(physical_efolds=mp.nstr(evolution['physical_efolds'],35),
                                       physical_efolds_quadrature=mp.nstr(evolution['physical_efolds_quadrature'],35),
                                       quadrature_minus_charge=mp.nstr(evolution['physical_efolds_quadrature']-evolution['physical_efolds'],10),
                                       initial_S=mp.nstr(evolution['initial_S'],35),final_S='.1',final_radiation_ratio='.001',
                                       radiation_constant=mp.nstr(evolution['radiation_constant'],35),
                                       samples=len(evolution['states']),unhealthy_samples=sum(not b['admissible'] for b in evolution['states']),
                                       max_charge_error=mp.nstr(max(abs(b['charge_ratio']-1) for b in evolution['states']),10),
                                       max_radiation_charge_error=mp.nstr(max(abs(b['radiation_charge_ratio']-1) for b in evolution['states']),10),
                                       rows=list(map(show,evolution['states']))),
                nonclaims=['Finite 80-digit witnesses, no interval theorem on the entire positive S domain',
                           'Pole boundary S=0 is excluded and energy diverges there',
                           'No baryon/recombination, strong-coupling, sourced MOND, or global-transition certificate'])


def verification_ok(result):
    return (all(value=='0' for value in result['exact_checks'].values())
            and result['scan']['unhealthy_samples']==0
            and result['late_scan']['unhealthy_samples']==0
            and result['radiation_history']['unhealthy_samples']==0
            and abs(mp.mpf(result['radiation_history']['quadrature_minus_charge']))<mp.mpf('1e-55')
            and mp.mpf(result['radiation_history']['max_charge_error'])<mp.mpf('1e-55')
            and mp.mpf(result['radiation_history']['max_radiation_charge_error'])<mp.mpf('1e-55'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    result=report()
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if not verification_ok(result) else 2 if args.require_full_closure else 0)
