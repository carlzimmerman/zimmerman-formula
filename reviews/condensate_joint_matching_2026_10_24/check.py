"""Condensate pressure and sourced MOND normalization; no fitted inputs."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
n1,n2,O,J,l1,l2,l12,l3=s.symbols('n1 n2 Omega J l1 l2 l12 l3',positive=True)
delta=s.symbols('delta',real=True)
checks=[]
def ck(name,e):
 z=s.factor(s.simplify(e));checks.append(dict(name=name,passed=z==0,residual=str(z)))
def pressure(U):return n1*s.diff(U,n1)+n2*s.diff(U,n2)-U
UR=-2*O*s.sqrt(n1*n2)*s.cos(delta)
UP=J*(1-s.cos(delta))
ck('ordinary_Rabi_pressure',(-UR if args.mutate else pressure(UR)))
ck('phase_only_pressure',pressure(UP)+UP)
ck('Rabi_density_degree',n1*s.diff(UR,n1)+n2*s.diff(UR,n2)-UR)
U2=l1*n1*n1/2+l2*n2*n2/2+l12*n1*n2
U3=l3*(n1+n2)**3/3
ck('repulsive_quartic_pressure',pressure(U2)-U2)
ck('repulsive_sextic_pressure',pressure(U3)-2*U3)
b=s.symbols('scale_factor',positive=True)
ck('fixed_fraction_Rabi_dilution',UR.subs({n1:n1/b**3,n2:n2/b**3})-UR/b**3)
a,c,k,t=s.symbols('a c k t',real=True)
D=s.Matrix([[a,-k],[-k,c]])
eplus=(a+c+s.sqrt((a-c)**2+4*k*k))/2
eminus=(a+c-s.sqrt((a-c)**2+4*k*k))/2
ck('mixing_mass_plus',(D-t*s.eye(2)).det().subs(t,eplus))
ck('mixing_mass_minus',(D-t*s.eye(2)).det().subs(t,eminus))
ck('mixing_mass_product',eplus*eminus-(a*c-k*k))
C,q,G,m,r,z,Sn=s.symbols('C q G m r z sphere_area',positive=True)
dim=s.symbols('n',positive=True)
qe=q*(2 if args.mutate else 1)
grad=s.sqrt(qe*m/(Sn*C*r**(dim-1)))
ck('general_dimension_flux',Sn*r**(dim-1)*C*grad**2-q*m)
acc=qe*grad.subs({dim:3,Sn:4*s.pi})
a0=acc**2/(G*m/r**2)
ck('operational_MOND_scale',a0-q**3/(4*s.pi*G*C))
ck('field_normalization_invariance',a0.subs({q:q/z,C:C/z**3})-a0)
ck('source_charge_cubic_sensitivity',a0.subs(q,2*q)-8*a0)
L,MP,c0,c3,cb=s.symbols('Lambda Mpl c0 c3 cb',positive=True)
eps=c0*L**4
single=s.simplify(a0.subs({C:c3*L,q:cb*L/MP,G:1/(8*s.pi*MP**2)})/s.sqrt(eps/(8*s.pi*MP**2)))
target=2*s.sqrt(8*s.pi)*cb**3/(c3*s.sqrt(c0))
ck('single_scale_matching_ratio',single-target)
ck('transmutation_scale_cancels',s.diff(single,L))
ck('Planck_scale_cancels',s.diff(single,MP))
ck('portal_sensitivity',cb*s.diff(single,cb)-3*single)
ck('cubic_sensitivity',c3*s.diff(single,c3)+single)
ck('vacuum_amplitude_sensitivity',c0*s.diff(single,c0)+single/2)
alpha=s.symbols('alpha',positive=True)
ck('superfluid_convention_match',a0.subs({q:alpha*L/MP,C:2*L,G:1/(8*s.pi*MP**2)})-alpha**3*L**2/MP)
result=dict(mutated=args.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,scope='NR stable-mass mixing pressure and conditional MOND operator matching; no microscopic joint selector or UV health proof')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
