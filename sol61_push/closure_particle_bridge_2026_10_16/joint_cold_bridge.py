"""Local-density benchmark with both cold and fermion densities varied.

Prescribed static external Plummer trap/baryon scalar flux. No self-gravity,
full band gradients, metric, formation, temperature or particle matching.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import roots_legendre

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent;parent=base/'reciprocal_density_bridge.py'
text=parent.read_text();marker='\ncoarse=[]';assert text.count(marker)==1
ns={'__file__':str(parent),'__name__':'joint_bridge_definitions'}
exec(compile(text.split(marker)[0],str(parent),'exec'),ns)
check=ns['check'];source=ns['source'];ri=.1;V0=2.;Kc=1.;background=1.;margin=1.
def potential(r):return -V0/math.sqrt(1+r*r)
def local(r,mu,z):
    S=source(r);gap0=math.sqrt(S);chemical=mu+z*potential(r)/Kc
    if abs(chemical)<=gap0:gap,q,E=gap0,0.,gap0
    else:
        def eq(E):return E+margin*(E*E-(S/E)**2)/2-abs(chemical)
        E=brentq(eq,gap0,abs(chemical),xtol=2e-14,rtol=2e-14)
        gap=S/E;q=math.copysign((E*E-gap*gap)/2,chemical)
    n=background-potential(r)/Kc-z*q/Kc
    return n,q,gap,E

def integrals(R,mu,z):
    def edge(r):return abs(mu+z*potential(r)/Kc)-math.sqrt(source(r))
    grid=np.geomspace(ri,R,257);points=[ri,R]
    for l,r in zip(grid[:-1],grid[1:]):
        if edge(l)*edge(r)<0:points.append(brentq(edge,l,r,xtol=1e-12,rtol=1e-13))
    points=sorted(points);pos=neg=0.;neutral=[]
    for l,r in zip(points[:-1],points[1:]):
        if edge(math.sqrt(l*r))<=0:neutral.append([l,r]);continue
        value=quad(lambda rr:4*math.pi*rr*rr*local(rr,mu,z)[1],l,r,epsabs=1e-10,epsrel=2e-9,limit=200)[0]
        if value>0:pos+=value
        else:neg-=value
    return pos,neg,neutral

rows=[]
for z in (.3,1.,3.):
    for R in (10.,30.,100.):
        u=z*z/Kc+margin
        def balance(mu):
            p,n,_=integrals(R,mu,z);return p-n
        mu=brentq(balance,0.,z*V0/Kc+1,xtol=1e-13,rtol=1e-13)
        pos,neg,neutral=integrals(R,mu,z)
        check('joint fermion charge conservation '+str((z,R)),abs(pos-neg)/(pos+neg)<1e-7)
        def primitive(r):return (r*math.sqrt(1+r*r)-math.asinh(r))/2
        Ntarget=4*math.pi*(background*(R**3-ri**3)/3+V0/Kc*(primitive(R)-primitive(ri)))
        gn,gw=roots_legendre(1024)
        logs=(math.log(R)+math.log(ri))/2+(math.log(R)-math.log(ri))*gn/2
        rr=np.exp(logs);weights=gw*(math.log(R)-math.log(ri))/2*4*math.pi*rr**3
        states=[local(r,mu,z) for r in rr]
        Nnumerical=float(weights@np.array([s[0] for s in states]))
        # Gauss cross-check has occupation edges; compare with declared
        # finite tolerance rather than claiming exact number from nodes.
        check('joint cold inventory quadrature '+str((z,R)),abs(Nnumerical/Ntarget-1)<2e-6)
        check('positive cold density active-set consistency '+str((z,R)),min(s[0] for s in states)>0)
        check('patch energy range '+str((z,R)),max(s[3] for s in states)/1000<.01)
        cold_res=max(abs(n+z*q+potential(r)-background) for r,(n,q,d,E) in zip(rr,states))
        fermi_res=max((abs(math.copysign(E,q)+u*q+z*n-(mu+z*background)) if q else max(0.,abs(mu+z*background-z*n)-d)) for n,q,d,E in states)
        force_res=max(abs(d*E-source(r)) for r,(n,q,d,E) in zip(rr,states))
        check('cold stationarity '+str((z,R)),cold_res<1e-12)
        check('fermion stationarity original coefficients '+str((z,R)),fermi_res<2e-10)
        check('scalar stationarity '+str((z,R)),force_res<2e-12)
        samples=[]
        for r in np.geomspace(ri,R,151):
            n,q,gap,E=local(r,mu,z);D=source(r);nbase=background-potential(r)/Kc
            samples.append(dict(r=float(r),cold_density=n,cold_density_without_bridge=nbase,
                cold_density_fractional_change=n/nbase-1,fermion_charge=q,gap=gap,
                scalar_force=D+gap,scalar_force_over_neutral=(D+gap)/(D+math.sqrt(D))))
        row=dict(coupling=z,R=R,repulsion=u,cold_chemical_potential_minus_rest_mass=background*Kc,
            relative_fermion_chemical_potential=mu,fermion_chemical_potential=mu+z*background,
            positive_charge=pos,negative_charge_magnitude=neg,neutral_cubic_intervals=neutral,
            fixed_cold_number=Ntarget,cold_number_quadrature_relative_error=Nnumerical/Ntarget-1,
            max_cold_density_enhancement=max(s['cold_density_fractional_change'] for s in samples),
            min_cold_density_change=min(s['cold_density_fractional_change'] for s in samples),samples=samples)
        rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='samples'}),flush=True)
result=dict(model='Both cold n and fermion q varied; local zero-T nodal-density functional; reflecting annulus; QF=0 and cold number fixed; prescribed external trap U=-2/sqrt(1+r^2), scalar fluxD=r/(1+r^2)^1.5; no cold self-gravity',
    conventions='A=C=h=Kc=n_background=1; u=zeta^2/Kc+1; r_inner=.1; energies/gaps<<cutoff1000; dimensionless',
    checks=ns['checks'],runs=rows,non_claims=['No derived physical halo, MeV-action matching, full band gradients, phase kinetics, temperature, self-gravity or metric/lensing','No added coldness proof, vacuum prediction or global novelty claim'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed %d controls.'%len(ns['checks']))
