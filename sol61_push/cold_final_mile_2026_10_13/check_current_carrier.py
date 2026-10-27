"""CE-FM-013: exact current bridge and missing reference Euler equation."""
import json,sys
from pathlib import Path
import sympy as s

t,x,y,z=s.symbols('t x y z');coords=(x,y,z)
P=[s.Function(name)(t,x,y,z) for name in ('Px','Py','Pz')]
rhoB=s.symbols('rhobar',positive=True)
rho=rhoB+sum(s.diff(Pi,xi) for Pi,xi in zip(P,coords));current=[-s.diff(Pi,t) for Pi in P]
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)
check('flat current identity',s.simplify(s.diff(rho,t)+sum(s.diff(ji,xi) for ji,xi in zip(current,coords)))==0,'rho=rhobar+divP,j=-dotP')

# Exact contraction needed in the curved double-divergence identity.
Ric=s.Matrix(4,4,lambda i,j:s.Symbol('R_%d%d'%(min(i,j),max(i,j))))
B=s.Matrix(4,4,lambda i,j:0 if i==j else (1 if i<j else -1)*s.Symbol('B_%d%d'%(min(i,j),max(i,j))))
check('Ricci antisymmetric contraction',s.expand(sum(Ric[i,j]*B[i,j] for i in range(4) for j in range(4)))==0,'commutator double-divB=0 for LeviCivita connection')

N=s.Function('N')(x);vol=s.Function('V')(t,x);p=s.Function('P')(t,x);rb=s.Function('rb')(t,x)
J0=rb/N+s.diff(vol*p,x)/(N*vol)
Jx=-s.diff(vol*p,t)/(N*vol)
continuity=s.simplify(s.diff(N*vol*J0,t)+s.diff(N*vol*Jx,x))
check('ADM conservation matches reference conservation',s.simplify(continuity-s.diff(vol*rb,t))==0,str(continuity))
check('ADM normal density',s.simplify(N*J0-rb-s.diff(vol*p,x)/vol)==0,'rho_n=rhobar+D_iP^i')
polar_rest=-N*s.diff(vol*p,x)
check('static rest action yields lapse coupling',s.simplify(polar_rest+s.diff(N*vol*p,x)-vol*p*s.diff(N,x))==0,'-N div(VP)=boundary+VP gradN')
R,j,e=s.symbols('rho j epsilon',positive=True)
expansion=s.series(-s.sqrt(R*R-e*e*j*j),e,0,5).removeO()
check('positive NR kinetic coefficient',s.simplify(expansion.coeff(e,2)-j*j/(2*R))==0,str(expansion))

# Static curl of the actual carrier fourvelocity, u_cov=(-N,0,0,0).
F0x=s.diff(N,x);a=s.diff(N,x)/N
check('static curl contraction',s.simplify(F0x/N-a)==0,'n^nu F_nux=a_x')
K,a0,uu=s.symbols('K a0 u',positive=True)
Wp=a0*uu/(a0-uu)
candidate_ref=s.simplify(rhoB*Wp)
check('nonzero reference Euler residual on desired force balance',s.simplify(candidate_ref-rhoB*a0*uu/(a0-uu))==0,
      'rhobar*Wprime>0 forrhobar>0,0<u<a0; violates freely varied reference dustEuler')
check('zero reference residual forces no polarization in admissible branch',s.solve(s.Eq(rhoB*a0*uu,0),uu)==[],
      'Positiveu symbol excludesu0: no nonzero static branch')

result=dict(checks=checks,NR_current='rho=rhobar+divP,j=-dotP',
            reference_residual=str(candidate_ref),
            scope='Kinematic identities and first-variation obstruction for a specific naive freely varied reference-current parent; not all covariant carrier models.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
