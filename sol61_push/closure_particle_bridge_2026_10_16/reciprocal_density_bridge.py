"""Separately specified local-density carrier/nodal-medium bridge.

Zero-T patch energy, chosen repulsive density interaction; finite annulus
with prescribed cold density and baryon flux. Fermion charge and local force
are solved together. This is not cold transport or a nonlocal band solution.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import roots_legendre
import sympy as sp

out=Path(sys.argv[1]);assert out.is_dir()
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

# Canonical fermion energy from the band determinant, including its
# chemical-potential-dependent constant (essential for carrier feedback).
A,d,q=sp.symbols('A d q',positive=True)
F=A*(d*d+2*q/A)**sp.Rational(3,2)/3
H=sp.hessian(F,(d,q))
check('exact joint fermion Hessian determinant',sp.simplify(H.det()-1)==0)
check('exact canonical charge derivative',sp.simplify(sp.diff(F,q)-sp.sqrt(d*d+2*q/A))==0)
check('exact gap derivative',sp.simplify(sp.diff(F,d)-A*d*sp.sqrt(d*d+2*q/A))==0)
n,z,u,K=sp.symbols('n z u K',real=True)
lhs=K*n*n/2+z*n*q+u*q*q/2
rhs=K*(n+z*q/K)**2/2+(u-z*z/K)*q*q/2
check('exact stabilizing complete square',sp.simplify(lhs-rhs)==0)

def fermion_energy(gap,charge,AA=1.):
    return AA*(gap*gap+2*abs(charge)/AA)**1.5/3
def equilibrium(gap,chemical,repulsion,AA=1.):
    if abs(chemical)<=gap:return 0.,gap
    # E+u A (E^2-gap^2)/2=|chemical|, stable cancellation-free root.
    E=(2*abs(chemical)+repulsion*AA*gap*gap)/(1+math.sqrt(1+2*repulsion*AA*abs(chemical)+(repulsion*AA*gap)**2))
    charge=math.copysign(AA*(E*E-gap*gap)/2,chemical)
    return charge,E

# Differentiate the minimized canonical energy, not just its P derivative.
for gap in (.03,.2,1.):
    for chemical in (-2.,-.1,0.,.1,2.):
        charge,E=equilibrium(gap,chemical,.7)
        if charge:
            check('charge stationarity '+str((gap,chemical)),abs(math.copysign(E,charge)+.7*charge-chemical)<1e-12)
        else:check('gap subgradient '+str((gap,chemical)),abs(chemical)<=gap)
        def reduced(dd):
            qq,_=equilibrium(dd,chemical,.7)
            return fermion_energy(dd,qq)+.7*qq*qq/2-chemical*qq
        step=gap*1e-4
        derivative=(reduced(gap+step)-reduced(gap-step))/(2*step)
        check('envelope gap response '+str((gap,chemical)),abs(derivative-gap*E)<2e-8*(1+gap*E))

rin=.1;S0=1.;n0=2.;Kc=1.;cutoff=1000.
def cold(r):return 1+n0/(1+r*r)
def source(r):return S0*r/(1+r*r)**1.5

def local(r,mu,coupling,repulsion):
    # A=C=h=1. mu measured relative to zeta*n_background.
    S=source(r);gap0=math.sqrt(S)
    chemical=mu-coupling*(cold(r)-1)
    if abs(chemical)<=gap0:return gap0,0.,gap0
    # Coupled field equation gap*E=S and canonical charge relation.
    def eq(E):return E+repulsion*(E*E-(S/E)**2)/2-abs(chemical)
    E=brentq(eq,gap0,abs(chemical),xtol=2e-14,rtol=2e-14)
    gap=S/E
    charge=math.copysign((E*E-gap*gap)/2,chemical)
    return gap,charge,E

def profile(R,coupling,N):
    repulsion=coupling**2/Kc+1.
    nodes,weights=roots_legendre(N)
    # Log-radius grid resolves both the central and compensating outer gas.
    lo,hi=math.log(rin),math.log(R)
    logs=(hi+lo)/2+(hi-lo)*nodes/2
    rr=np.exp(logs);ww=weights*(hi-lo)/2*4*math.pi*rr**3
    def total(mu):return float(ww@np.array([local(r,mu,coupling,repulsion)[1] for r in rr]))
    mu=brentq(total,0.,coupling*n0+1,xtol=2e-13,rtol=2e-13)
    states=[local(r,mu,coupling,repulsion) for r in rr]
    gaps=np.array([s[0] for s in states]);charges=np.array([s[1] for s in states]);energies=np.array([s[2] for s in states])
    pos=float(ww@np.maximum(charges,0));neg=-float(ww@np.minimum(charges,0))
    scale=1+pos+neg
    check('neutral total '+str((R,coupling,N)),abs(pos-neg)/scale<2e-9)
    check('controlled low energy tube '+str((R,coupling,N)),max(energies)/cutoff<.01)
    check('force no larger than neutral branch '+str((R,coupling,N)),np.all(gaps<=np.sqrt([source(r) for r in rr])*(1+1e-13)))
    # Local field equation and charge chemical equilibrium, sampled on all nodes.
    residual=max(abs(g*e-source(r))/(1+source(r)) for r,g,e in zip(rr,gaps,energies))
    check('coupled field equation '+str((R,coupling,N)),residual<2e-12)
    chemical_residual=max((abs(math.copysign(e,qq)+repulsion*qq-(mu-coupling*(cold(r)-1))) if qq else max(0.,abs(mu-coupling*(cold(r)-1))-gg)) for r,gg,qq,e in zip(rr,gaps,charges,energies))
    check('coupled charge equation '+str((R,coupling,N)),chemical_residual<2e-10)
    samples=[]
    for r in np.geomspace(rin,R,101):
        gap,charge,E=local(r,mu,coupling,repulsion);D=source(r)
        samples.append(dict(r=float(r),cold_density=cold(r),gap=gap,fermion_charge=charge,
            relative_fermion_chemical_potential=mu-coupling*(cold(r)-1),
            carrier_chemical_feedback=coupling*charge,
            total_scalar_force=D+gap,scalar_force_over_neutral=(D+gap)/(D+math.sqrt(D))))
    return dict(R=R,coupling=coupling,repulsion=repulsion,Kc=Kc,quadrature_nodes=N,
        chemical_potential_relative_background=mu,positive_charge=pos,negative_charge_magnitude=neg,
        net_charge=pos-neg,max_energy_over_cutoff=float(max(energies)/cutoff),
        minimum_force_over_neutral=min(s['scalar_force_over_neutral'] for s in samples),
        cold_number_in_annulus=4*math.pi*((R**3-rin**3)/3+n0*((R-math.atan(R))-(rin-math.atan(rin)))),
        samples=samples)

coarse=[];fine=[];refinement=[]
for coupling in (.3,1.,3.):
    for R in (10.,30.,100.):
        a=profile(R,coupling,384);b=profile(R,coupling,768)
        for key in ('chemical_potential_relative_background','positive_charge','negative_charge_magnitude'):
            error=abs(a[key]-b[key])/(1+abs(b[key]))
            check('radial refinement '+key+str((R,coupling)),error<.003)
            refinement.append(dict(R=R,coupling=coupling,quantity=key,normalized_difference=error))
        coarse.append({k:v for k,v in a.items() if k!='samples'});fine.append(b)
        print(json.dumps({k:v for k,v in b.items() if k!='samples'}),flush=True)

result=dict(model='Dated reciprocal NR density-energy bridge; low-energy zero-T nodal canonical energy; u=zeta^2/Kc+1; prescribed cold density and Plummer baryon flux on reflecting finite annulus; fixed total fermion charge0',
    conventions='A=C=h=1; n_background=1;n_excess=2/(1+r^2);source D=r/(1+r^2)^(3/2);r_inner=.1;cutoff1000; all units dimensionless',
    checks=checks,coarse=coarse,runs=fine,refinement=refinement,
    non_claims=['No cold-density transport, source selection or derived halo profile','No full nonlocal or dynamical fermion band solution, finite-temperature history, vacuum magnitude or metric/lensing','Contact repulsion and bridge coefficients are new inputs, not matched to protected MeV action','No transfer of classical coldness bounds to this extension; no unique/global novelty claim'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed %d bounded controls.'%len(checks))
