"""Evaluate FT-B1 and independently test its inequalities on displaced shells."""
import argparse,itertools,json
from pathlib import Path
import numpy as np
from experiment import Inertial,PROFILES
from diffuse import Diffuse

def bound(m):
    x=2/3;C=m.f*m.f;A=9/16*(1+3*20*C/(2*np.pi*np.pi))-1
    mu=1/m.n;ell=np.sort(m.l2[:m.n]);c=(np.arange(m.n)+.5)*mu/.75
    B=.5*np.sum(mu*c*c/ell)
    E0=m.observe(0,m.initial())['energy'];L=-B*(1+1/A)**2
    ac=1/(np.sqrt(abs(E0)/B)-1) if abs(E0)>B else None
    fc=np.sqrt(((1+ac)/(9/16)-1)*2*np.pi*np.pi/(3*20)) if ac is not None else None
    return dict(A=float(A),energy_lower_bound=float(L),initial_energy=E0,
        exclusion_margin=float(L-E0),excluded=bool(A>0 and L>E0),
        coherence_threshold_at_this_phase=float(fc) if fc is not None else None)

def checks():
    m=Inertial(1e8,1,n=6,nq=512);x=2/3;b=bound(m)
    # Deterministic, deliberately nonhomologous and shell-crossing witnesses.
    minimum_slack=float('inf');visited=0;outside=0
    for sb,sc,reverse in itertools.product([.2,.5,1,3],[.2,.5,1,3],[False,True]):
        r=m.r0.copy();r[:m.n]*=sb;r[m.n:]*=sc
        if reverse:r[:m.n]=r[:m.n][::-1]
        try:E=m.energy(r,x)[0]+.5*np.dot(m.m,m.l2/r**2)
        except ValueError:outside+=1;continue
        minimum_slack=min(minimum_slack,E-b['energy_lower_bound']);visited+=1
    assert minimum_slack>=-1e-7
    # An orthogonal finite permutation check of the rearrangement direction.
    r=np.array([1.,2.,4.,8.]);ell=np.array([.3,.8,2.,7.])
    target=sum(ell/r**2)
    costs=[sum(np.array(p)/r**2) for p in itertools.permutations(ell)]
    assert abs(min(costs)-target)<1e-14
    return dict(admissible_cases=visited,outside_saturation=outside,minimum_energy_slack=minimum_slack,
                rearrangement_permutations=len(costs))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    rows=[]
    for n in [6,12,24]:
        for i,(_,mass,b,_) in enumerate(PROFILES):
            m=Inertial(mass,b,n=n,nq=1024,f=.95)
            rows.append(dict(profile=i,n=n,dark_scale=3,**bound(m)))
    for scale in [10,30]:
        m=Diffuse(1e8,1,n=12,nq=1024,scale=scale)
        rows.append(dict(profile=1,n=12,dark_scale=scale,**bound(m)))
    out=dict(checks=checks(),runs=rows)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    for r in rows:print(r)
