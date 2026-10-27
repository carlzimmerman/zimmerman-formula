"""One flux scale for a specified finite-cutoff nodal medium.

This tests the scaling hypothesis, not its dynamical origin or a covariant
UV completion. Filled-sea reference energy is explicitly kept separately.
"""
import json
import math
import sys
from pathlib import Path
import mpmath as mp
from scipy.integrate import quad

out=Path(sys.argv[1]);assert out.is_dir();checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
mp.mp.dps=60
N=2;v=.5;cm=2*math.sqrt(2);ck=2.;cL=.5;ch=.5
Astar=N*cm/(2*math.pi*v)
alpha=Astar*ch**3/3
sea_coefficient=-Astar*cL**3/3
electric_curvature_empty=1+2*sea_coefficient
counterterm_P_squared=Astar*cL*ch*ch/2
tube_ceiling=ck*ck/(2*cm)
max_radial_group=math.sqrt(ck*ck+2*cm*cL)/cm
check('full circular tube condition',cL<tube_ceiling)
check('bounded-band radial group speed',max_radial_group<1)
check('bounded-band axial group speed',v<1)
check('filled-sea empty electric curvature positive',electric_curvature_empty>0)
check('chosen normalization kappa half',abs(1/(6*math.sqrt(2)*math.pi*alpha)/.5-1)<1e-14)

rows=[]
for Q in (.01,1.,100.):
    mu=math.sqrt(Q);AA=Astar*mu;cutoff=cL*mu
    for y in (.001,.01,.1):
        p=Q*y;gap=ch*p/mu
        # Cancellation-free physical radial integral, with physical cutoff.
        value=AA*quad(lambda t:gap**4/(2*(math.sqrt(t*t+gap*gap)+t)**2),
                      0,cutoff,epsabs=AA*gap**3*1e-13,epsrel=1e-11,limit=300)[0]
        # Independent high-precision closed determinant, not same quadrature.
        aa,dd,ll=map(lambda z:mp.mpf(str(z)),(AA,gap,cutoff))
        exact=-aa*((ll*ll+dd*dd)**mp.mpf('1.5')-ll**3-dd**3)/3+aa*ll*dd*dd/2
        exact=float(exact)
        check('direct finite-cutoff determinant '+str((Q,y)),abs(value/exact-1)<2e-10)
        leading=alpha*p**3/Q
        ratio=value/leading
        rows.append(dict(Q=Q,p_over_Q=y,gap_over_cutoff=gap/cutoff,
            determinant_over_Q_squared=value/(Q*Q),finite_determinant_over_leading_cubic=ratio,
            A_over_sqrtQ=AA/mu,fermion_gap=gap))
for y in (.001,.01,.1):
    values=[r['determinant_over_Q_squared'] for r in rows if r['p_over_Q']==y]
    check('one scale exact determinant collapse '+str(y),max(values)/min(values)-1<1e-12)

reference=(2.25e-12)**4
Qphysical=math.sqrt(2*reference);muPhysical=math.sqrt(Qphysical)
result=dict(hypothesis='muQ=sqrt(Q);mstar=cm*muQ;k0=ck*muQ;Lambda=cL*muQ;h=ch/muQ; all dimensionful medium inputs scale with one flux scale',
    constants=dict(N=N,v=v,cm=cm,ck=ck,cLambda=cL,ch=ch,Astar=Astar,alpha=alpha),
    filled_sea_energy_over_Q_squared=sea_coefficient,
    empty_electric_curvature_including_only_this_sea=electric_curvature_empty,
    Q_independent_quadratic_counterterm_coefficient=counterterm_P_squared,
    maximum_radial_group_speed_within_tube=max_radial_group,
    reference=dict(vacuum_energy_GeV4=reference,Q_GeV2=Qphysical,muQ_GeV=muPhysical,
        original_cold_mass_over_muQ=.002/muPhysical),
    rows=rows,checks=checks,non_claims=['One-scale parameter origin, critical tuning protection and kappa half are not derived','Group speeds checked only inside stated cutoff tube, not causal UV front propagation','Other sea/UV/loop vacuum functions may change electric convexity','No covariant occupied-frame state, actual dark temperature, cold-medium transport, halo, lensing or full closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
