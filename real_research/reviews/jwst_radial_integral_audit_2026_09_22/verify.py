"""Finite exact-one-scatter quadrature for quadratic radial opacity.

No assumed small-delay exponent is used to generate a probability.
"""
import json
import math
from pathlib import Path
import sys
from scipy.integrate import quad


def optical_depth(r, mu, k0, k2):
    length = -r*mu + math.sqrt(1-r*r+r*r*mu*mu)
    incoming = k0*r+k2*r**3/3
    outgoing = k0*length+k2*(r*r*length+r*mu*length**2+length**3/3)
    return incoming+outgoing


def joint(e, k0, k2, tol, isotropic=False):
    def radial(r):
        def angular(mu):
            phase = .5 if isotropic else .375*(1+mu*mu)
            return (k0+k2*r*r)*phase*math.exp(-optical_depth(r,mu,k0,k2))
        return quad(angular,max(-1,1-e/r),1,epsabs=tol,epsrel=tol)[0]
    return (quad(radial,0,e/2,epsabs=tol,epsrel=tol)[0]
            +quad(radial,e/2,1,epsabs=tol,epsrel=tol)[0])


def density(e, k0, k2, tol):
    def delay(x):
        d=e*x
        span=math.log(2/d)
        def radius(u):
            r=(d/2)*math.exp(u*span)
            mu=1-d/r
            return e*span*(k0+k2*r*r)*.375*(1+mu*mu)*math.exp(-optical_depth(r,mu,k0,k2))
        return quad(radius,0,1,epsabs=tol,epsrel=tol)[0]
    return quad(delay,0,1,epsabs=tol,epsrel=tol)[0]


def main():
    rows=[]
    checks={}
    for k0,k2 in [(1,0),(1,1),(0,1)]:
        for e in [.001,.0001]:
            j=joint(e,k0,k2,1e-9); f=density(e,k0,k2,1e-9)
            jr=joint(e,k0,k2,1e-11); fr=density(e,k0,k2,1e-11)
            neg=joint(e,k0,k2,1e-11,True)
            tolerance=1e-10+1e-6*max(abs(jr),abs(fr))
            tag=f'{k0}_{k2}_{e}'
            checks[tag+'_coordinates']=abs(j-f)<=tolerance
            checks[tag+'_refinement']=max(abs(j-jr),abs(f-fr))<=tolerance
            checks[tag+'_kernel_control']=abs(neg-fr)>tolerance
            coefficient=.75*k0*math.exp(-k0-k2/3)
            rows.append(dict(k0=k0,k2=k2,epsilon=e,joint=j,density=f,
                joint_refined=jr,density_refined=fr,negative_isotropic=neg,
                tolerance=tolerance,probability_over_e=fr/e,
                ratio_to_conjectured_leading=fr/(coefficient*e*math.log(1/e)) if coefficient else None))
        for r,mu in [(.2,-.8),(.4,.1),(.9,.9)]:
            length=-r*mu+math.sqrt(1-r*r+r*r*mu*mu)
            direct=quad(lambda x:k0+k2*x*x,0,r,epsabs=1e-12)[0]
            direct+=quad(lambda s:k0+k2*(r*r+2*r*mu*s+s*s),0,length,epsabs=1e-12)[0]
            checks[f'{k0}_{k2}_ray_{r}']=abs(direct-optical_depth(r,mu,k0,k2))<1e-12
    reference=json.loads((Path(__file__).resolve().parents[3]/'real_research/reviews/jwst_small_delay_leaf_2026_09_22/certified/result.json').read_text())
    old=next(r['density_refined'] for r in reference['rows'] if r['tau']==1 and r['epsilon']==.001)
    checks['uniform_prior_reference']=abs(rows[0]['density_refined']-old)<1e-11
    result=dict(rows=rows,checks=checks,scope='Finite one-scatter probabilities, not an asymptotic theorem. Shared analytic optical depth, checked against direct ray integration. Tolerances are not rigorous interval errors.')
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks))))
    assert all(checks.values())


if __name__=='__main__':
    main()
