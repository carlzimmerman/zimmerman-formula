#!/usr/bin/env python3
"""Local current roots and transport budgets; not coupled galaxy solutions."""
import json
from pathlib import Path
import sys
import mpmath as mp
import numpy as np
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
from constitutive import Model


def run():
    model=Model(0.);bg=model.background(0.)
    q,H,d,U,ell=(float(bg[k]) for k in ('q','H','d','U','ell'))
    B=U/(2*d);gamma=model.gamma
    rows=[];sign_count=0;min_scaled_gap=float('inf')
    # Broad sign test, not a replacement for the analytic argument.
    for mass in (.001,.1,1.,2.):
        for N in np.geomspace(.02,30.,45):
            for fraction in np.linspace(0.,1.,41):
                Q=q/N;Y=fraction*Q*Q;X=Q*Q-Y;BB=q*q*(1+mass);ll=q*q*mass/2
                if BB-X<=0:continue
                gap=BB/(BB-X)-1/(N*np.sqrt(1+Y/ll))
                if gap<=0:raise AssertionError(('uniform sign counterexample',mass,N,fraction,gap))
                min_scaled_gap=min(min_scaled_gap,float(gap));sign_count+=1
    # Proved weak-lapse gap bound: C0 >= d/2 for m=.1, .99<=N<=1.01.
    # See REPORT for the two-region derivation; check the exact rational margins.
    assert 2*1.01**2*1.1 < 2.5 and 5/3-100/99 > .5
    for N in (.99,1.,1.01):
        Q=q/N
        for radius in (.1,1.,10.):
            for acceleration in (0.,1e-6,1e-3,.01):
                def pieces(u):
                    Y=u*u;X=Q*Q-Y
                    jets=model.jets(0.,X,Y)
                    gap=d*B/(B-X)-float(jets['W_Y'])/N
                    source=(2*Q*H-3*q*H)*u+X*acceleration-2*Y/radius
                    current=-gap*u+gamma*source
                    return gap,source,current
                grid=np.linspace(-Q,Q,2001)
                vals=np.array([pieces(u)[2] for u in grid])
                if min(pieces(u)[0] for u in grid)<d/2:
                    raise AssertionError('weak-lapse gap bound')
                roots=[]
                for i in range(len(grid)-1):
                    if vals[i]==0:roots.append(float(grid[i]))
                    if vals[i]*vals[i+1]<0:
                        roots.append(float(brentq(lambda u:pieces(u)[2],grid[i],grid[i+1],xtol=1e-18)))
                if vals[-1]==0:roots.append(float(grid[-1]))
                roots=sorted(set(roots))
                # Uniform upper bound for all roots in the timelike interval,
                # independent of whether the finite grid misses a pair of roots.
                source_bound=abs(2*Q*H-3*q*H)*Q+Q*Q*abs(acceleration)+2*Q*Q/radius
                bound=2*abs(gamma)*source_bound/d
                if not roots:raise AssertionError('no local control root bracketed')
                for root in roots:
                    C,S,j=pieces(root)
                    if abs(j)>1e-12 or abs(root)>bound+1e-12:raise AssertionError('root/bound check')
                # Independent 60-digit direct formula with exact background
                # constants, not the imported floating constitutive evaluator.
                with mp.workdps(60):
                    qq=mp.mpf(10)/11;dd=mp.mpf(1)/200;bb=mp.mpf(10)/11
                    hh=mp.sqrt(mp.mpf(4)/15);ll=mp.mpf(5)/121;gg=mp.mpf(1)/10**6
                    nn=mp.mpf(str(N));rr=mp.mpf(str(radius));aa=mp.mpf(str(acceleration))
                    def direct(uu):
                        xx=(qq/nn)**2-uu**2
                        cc=dd*bb/(bb-xx)-dd/(nn*mp.sqrt(1+uu**2/ll))
                        return -cc*uu+gg*((2*qq/nn*hh-3*qq*hh)*uu+xx*aa-2*uu**2/rr)
                    high_roots=[mp.findroot(direct,mp.mpf(str(x))) for x in roots]
                    mismatch=max(abs(float(h)-x) for h,x in zip(high_roots,roots))
                    if mismatch>1e-15:raise AssertionError('independent root precision disagreement')
                # A deliberately finite spatial gradient: infer the exact local
                # radial current, rather than silently setting its time source to zero.
                test_u=.1*Q;C,S,j=pieces(test_u)
                flux_floor=max(0.,.5*d*abs(test_u)-abs(gamma*S))
                if abs(j)+1e-14<flux_floor:raise AssertionError('transport bound')
                rows.append(dict(N=N,r=radius,lapse_log_gradient=acceleration,
                    bracketed_roots=roots,root_residuals=[pieces(x)[2] for x in roots],
                    high_precision_root_disagreement=mismatch,
                    all_root_bound=bound,finite_gradient=test_u,normalized_current=j,
                    minimum_normalized_current=flux_floor,
                    cubic_fraction_of_gap_force=abs(gamma*S)/(C*abs(test_u))))
    # Counterexample outside m<=2: near X=0 the sign can change.
    mass=10.;N=.5;Y=(q/N)**2;X=0.
    outside=1-1/(N*np.sqrt(1+Y/(q*q*mass/2)))
    assert outside<0
    return dict(coefficients=dict(q=q,H=H,d=d,B=B,ell=ell,gamma=gamma,m=float(bg['m'])),
        sign_samples=sign_count,minimum_sampled_gap_over_d=min_scaled_gap,
        outside_range_counterexample=dict(m=mass,N=N,X=X,gap_over_d=outside),
        local_controls=rows,full_theory='OPEN',
        interpretation='current budget only; no metric constraints or stationary galaxy solved',
        root_scope='bracketed roots are not certified exhaustive; analytic bound covers every admissible root')


if __name__=='__main__': print(json.dumps(run(),indent=2))
