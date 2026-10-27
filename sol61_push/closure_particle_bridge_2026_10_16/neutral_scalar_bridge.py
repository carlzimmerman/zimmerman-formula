"""Charge-even scalar bridge: exact potential bound and vacuum tree controls.

The medium is the specified canonical density functional; this is not a
quantum/UV completion of nodal bands or a completed production history.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
import sympy as s

out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
parent=json.loads((base/'thermal_charge_run_002/results.json').read_text())
p=next(x['parameters'] for x in parent['phase_rows'] if x['parameters']['m']==.002)
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

I,q,sigma=s.symbols('I q sigma',real=True)
a,b,mu,lam,uR=s.symbols('a b mu lam uR',nonzero=True,real=True)
zeta=-a*b/mu**2
original=lam*I**2+a*a*I**2/(2*mu**2)+mu**2*sigma**2/2+sigma*(a*I+b*q)+(b*b/mu**2+uR)*q*q/2
squared=mu**2*(sigma+(a*I+b*q)/mu**2)**2/2+lam*(I+zeta*q/(2*lam))**2+(uR-zeta*zeta/(2*lam))*q*q/2
check('exact full scalar-density square identity',s.simplify(original-squared)==0)
reduced=s.expand(original.subs(sigma,-(a*I+b*q)/mu**2))
check('exact eliminated scalar contact',s.simplify(reduced-(lam*I**2+zeta*I*q+uR*q*q/2))==0)
re,im,dre,dim,m0=s.symbols('re im dre dim m',real=True)
j=2*(im*dre-re*dim)
check('positive-charge kinetic square sign',s.expand((dre-m0*im)**2+(dim+m0*re)**2-(dre*dre+dim*dim+m0*m0*(re*re+im*im)-m0*j))==0)

def dot(v):return v[0]*v[0]-float(v[1:]@v[1:])
pairings=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
def scalar_amplitude(charges,momenta,aa,ms):
    # Independently enumerate the allowed cubic sigma Phi*Phi trees.
    value=0.;channels=[]
    for left,right in pairings:
        if sum(charges[i] for i in left)!=0 or sum(charges[i] for i in right)!=0:continue
        inv=dot(momenta[left[0]]+momenta[left[1]])
        assert abs(inv-ms*ms)>1e-20,'resonant point excluded'
        value-=aa*aa/(inv-ms*ms);channels.append(inv)
    assert len(channels)==2
    return value,channels

m=p['m'];g=p['g'];M=p['M'];lr=p['rep'];rows=[]
for ratio in (3.,5.,10.,100.):
    ms=ratio*m;aa=.02*ms;bb=-.01
    extra=aa*aa/(2*ms*ms);zi=-aa*bb/(ms*ms)
    minimum=zi*zi/(2*lr);ur=2*minimum;u0=bb*bb/(ms*ms)+ur
    knr=lr/(2*m*m);znr=zi/(2*m)
    check('strict positive residual density matrix '+str(ratio),ur>znr*znr/knr)
    # Hessian in (I,q,sigma), which is positive independent of backgrounds.
    HH=np.array([[2*(lr+extra),0.,aa],[0.,u0,bb],[aa,bb,ms*ms]])
    check('full algebraic Hessian positive '+str(ratio),np.linalg.eigvalsh(HH)[0]>0)
    channel_rows=[]
    for velocity in (0.,.1,.5):
        energy=m/math.sqrt(1-velocity*velocity);momentum=energy*velocity
        angle=.7
        p1=np.array([energy,0.,0.,momentum]);p2=np.array([energy,0.,0.,-momentum])
        p3=np.array([energy,momentum*math.sin(angle),0.,momentum*math.cos(angle)])
        p4=np.array([energy,-p3[1],0.,-p3[3]])
        momenta=[p1,p2,-p3,-p4]
        sv,tv,uv=dot(p1+p2),dot(p1-p3),dot(p1-p4)
        check('on-shell Mandelstam identity '+str((ratio,velocity)),abs((sv+tv+uv)/(4*m*m)-1)<1e-13)
        plus,_=scalar_amplitude([1,1,-1,-1],momenta,aa,ms)
        opposite,_=scalar_amplitude([1,-1,-1,1],momenta,aa,ms)
        plus-=4*extra;opposite-=4*extra
        independent_plus=-aa*aa*(1/(tv-ms*ms)+1/(uv-ms*ms))-4*extra
        independent_opposite=-aa*aa*(1/(sv-ms*ms)+1/(tv-ms*ms))-4*extra
        check('same-charge enumerated trees '+str((ratio,velocity)),abs(plus-independent_plus)<1e-16)
        check('opposite-charge enumerated trees '+str((ratio,velocity)),abs(opposite-independent_opposite)<1e-16)
        if velocity==0.:
            check('same-charge compensated threshold '+str(ratio),abs(plus)<1e-16)
            threshold=4*m*m*aa*aa/(ms*ms*(ms*ms-4*m*m))
            check('opposite-charge finite threshold remainder '+str(ratio),abs(opposite/threshold-1)<1e-11)
            base_amplitude=-4*(p['total']-g*g/(M*M))
            cross_change=(1+opposite/base_amplitude)**2-1
        channel_rows.append(dict(CM_speed=velocity,s=sv,t=tv,u=uv,
            delta_same_charge_amplitude=plus,delta_opposite_charge_amplitude=opposite))
    width=aa*aa*math.sqrt(1-4*m*m/(ms*ms))/(16*math.pi*ms)
    rows.append(dict(mediator_mass_over_m=ratio,mediator_mass_GeV=ms,
        a_GeV=aa,b=bb,extra_bare_quartic=extra,zeta_I_GeVminus1=zi,
        zeta_NR_GeVminus2=znr,K_NR_lower_bound_GeVminus2=knr,
        u_R_GeVminus2=ur,bare_u0_GeVminus2=u0,
        opposite_charge_threshold_cross_section_fractional_change=cross_change,
        sigma_to_Phi_PhiStar_width_GeV=width,rest_lifetime_seconds=6.582119569e-25/width,
        vacuum_range_m=1.973269804e-16/ms,amplitude_rows=channel_rows))

result=dict(parameters=p,rows=rows,checks=checks,
    scope='Exact polynomial potential identity; conditional positive-density-functional carrier bound; tree soft-density and finite-momentum scalar matching; chosen mediator family',
    non_claims=['No full regulated-band quantum/UV energy bound','NR K is a lower-bound translation, not a derived neutral-mixture equation of state','No actual mediator population, freeze-in or medium-temperature solution','No protected coefficient relation under radiative corrections, physical galaxy law, vacuum magnitude, lensing or novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),rows=rows),indent=2))
