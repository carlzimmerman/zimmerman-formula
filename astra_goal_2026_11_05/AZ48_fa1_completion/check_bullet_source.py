#!/usr/bin/env python3
"""Signed-source, normalization and analytic selector checks; no 3D solve."""
import argparse,json,math
from fractions import Fraction
from pathlib import Path
import numpy as np
import bullet_source as B
import audit_inputs as A
parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args();checks=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
rows=B.components();expected=np.array([[2e14,565,190,90,0],[1.5e13,505,525,120,0],[1.5e13,90,670,170,0],[-6.8e12,70,670,170,0],[1.196e13,470,0,0,0],[4e12,245,820,220,0]])
check('exact_inherited_components',np.array_equal(rows,expected));check('total_signed_mass',float(rows[:,0].sum())==2.3916e14)
ratio=Fraction(68,150)*Fraction(90,70)**3
check('signed_pair_positive_global_bound',ratio<1 and np.array_equal(rows[2,2:],rows[3,2:]),float(ratio))
# For common-centre Plummers with a_minus<a_plus the magnitude ratio is
# maximal at r=0; all remaining components have positive masses.
r=np.r_[0.,np.geomspace(1e-6,1e7,1000)];positive=3*1.5e13/(4*math.pi*90**3)*(1+(r/90)**2)**-2.5;negative=3*6.8e12/(4*math.pi*70**3)*(1+(r/70)**2)**-2.5
check('sampled_pair_bound',np.max(negative/positive)<=float(ratio)*(1+1e-12))
check('remaining_components_positive',np.all(rows[[0,1,4,5],0]>0))
masses=[]
for n in [16384,32768]:
    x=np.geomspace(1e-6,1e5,n);integrand=3*x*x/(1+x*x)**2.5
    value=float(np.trapz(integrand,x));truth=float(x[-1]**3/(1+x[-1]**2)**1.5-x[0]**3/(1+x[0]**2)**1.5)
    check('Plummer_mass_integral_'+str(n),abs(value/truth-1)<=1e-6,abs(value/truth-1));masses.append(value)
check('mass_quadrature_pair',abs(masses[0]/masses[1]-1)<=1e-6)
for name,H,target in [('isotropic',np.eye(3),1.),('planar',np.diag([1.,0,0]),0.),('rank_two',np.diag([1.,2.,0]),0.),('deep_point',np.diag([-.5,1.,1.]),-.769800358919501)]:
    value=float(B.selector(H,args.mutate));check('selector_'+name,abs(value-target)<=1e-12,value)
feet={}
for foot,a0 in B.A0.items():
    normal=B.normalization(foot);scaled=B.normalization(foot,4*B.RHO_REF);eps=normal['epsilon'];rho=normal['rho_ref_SI']
    direct=math.sqrt(3*a0*a0/(8*math.pi*B.G*rho*B.C*B.C));check(foot+'_epsilon_independent',abs(eps/direct-1)<=1e-12)
    check(foot+'_unit_rescaling',abs(scaled['epsilon']/(eps/2)-1)<=1e-12 and abs(scaled['pi_per_phi_SI']/(2*normal['pi_per_phi_SI'])-1)<=1e-12)
    S=.7;y=2*S/(3*eps+math.sqrt(9*eps*eps+24*S));rr=np.geomspace(1e-4,10,300);Q=S*rr**3/3;dp=B.positive_root(rr,Q,eps)
    check(foot+'_uniform_spherical_root',np.max(abs(dp/(y*rr)-1))<=1e-12)
    check(foot+'_spherical_equation',np.max(abs((eps*rr**2*dp+2*rr*dp**2)/Q-1))<=1e-12)
    H=np.array([[1.,.1,.2],[.1,2.,.3],[.2,.3,3.]])
    lhs=lambda h,e:e*np.trace(h)+np.trace(h)**2-np.sum(h*h)
    check(foot+'_normalized_equation_rescaling',abs(lhs(H/2,eps/2)/(lhs(H,eps)/4)-1)<=1e-12)
    check(foot+'_selector_unit_invariance',abs(float(B.selector(H/2,args.mutate))-float(B.selector(H,args.mutate)))<=1e-12)
    feet[foot]=normal
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),mutate=args.mutate,components=rows.tolist(),total_mass_msun=float(rows[:,0].sum()),centroid_kpc=B.centroid().tolist(),
 signed_pair_density_ratio_upper_bound=dict(exact=str(ratio),value=float(ratio),proof='Common centre and smaller negative scale: ratio decreases with radius; central ratio<1. All other components positive.'),footings=feet,
 source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(B.__file__).resolve(),B.SOURCE,A.HERE/'FROZEN_BULLET.md']},
 scope='Source and analytic normalization checks only; no 3D numerical field or Bullet classification; retired sector, adopts nothing; kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/('mutate/bullet_source_checks.json' if args.mutate else 'bullet_source_checks.json'),obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']],physical_epsilon={k:v['epsilon'] for k,v in feet.items()}),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
