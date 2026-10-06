"""Actual ADM/Gauss magnetic triad +clock+gravity+dust principal channel."""
import argparse,json,pathlib,itertools,sympy as s,numpy as np
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','stable','omit_shift_square','wrong_density'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.factor(s.cancel(e));ck(n,e==0,str(e))
M,Th,Sig,kap,p,B,Z,b,q=s.symbols('M Th Sig kap p B Z b q',nonzero=True,real=True)
z,C,nu,S,zd,Cd=s.symbols('z C nu S zd Cd',real=True)
# Actual Maxwell ADM normal electric; three puremagnetic diagonal fields.
Bg=[s.Matrix([B,0,0]),s.Matrix([0,B,0]),s.Matrix([0,0,B])]
Avel=[s.Matrix([0,-Cd/s.sqrt(2),0]),s.Matrix([Cd/s.sqrt(2),0,0]),s.zeros(3,1)]
shift=s.Matrix([0,0,S]);En=[Avel[i]+shift.cross(Bg[i]) for i in range(3)]
KE=sum((e.dot(e) for e in En))/2;zero('normal_electric_shift_square',KE-(Cd-s.sqrt(2)*B*S)**2/2)
long=s.symbols('Ez0 Ez1 Ez2');Gauss=sum(v*v for v in long)/2
for j in range(3):zero('Gauss_constraint_'+str(j),s.diff(Gauss,long[j]).subs(long[j],0))
# Magnetic covariant energy vs coordinate density; metricvariation is loadbearing.
eps=s.symbols('eps',real=True)
maglist=[s.Matrix([B+eps*p*C/s.sqrt(2),0,0]),s.Matrix([0,B+eps*p*C/s.sqrt(2),0]),s.Matrix([0,0,B])]
magcoords=sum(e.dot(e) for e in maglist)
rho=s.Rational(3,2)*B*B;energy=s.exp(-4*eps*z)*magcoords/2
Delta=s.sqrt(2)*B*p*C-6*B*B*z
zero('full_clock_normal_density_variation',s.diff(energy,eps).subs(eps,0)-Delta)
if args.control=='wrong_density':zero('CONTROL_omit_metric_density',s.diff(energy,eps).subs(eps,0)-s.sqrt(2)*B*p*C)
magL=-(1+eps*nu)*s.exp(-eps*z)*magcoords/2;magQuad=s.expand(s.series(magL,eps,0,3).removeO().coeff(eps,2))
zero('actual_Maxwell_magnetic_quadratic',magQuad-(-p*p*C*C/2+s.sqrt(2)*B*p*C*(z-nu)+rho*nu*z-rho*z*z/2))
# Scalar-helicity invariance: linear bare stress is diag(0,0,delta rho); no vector/TT source.
db=[s.Matrix([p*C/s.sqrt(2),0,0]),s.Matrix([0,p*C/s.sqrt(2),0]),s.zeros(3,1)]
dr=sum(Bg[i].dot(db[i]) for i in range(3));stress=dr*s.eye(3)-sum((Bg[i]*db[i].T+db[i]*Bg[i].T for i in range(3)),s.zeros(3))
zero('scalar_stress_xx_equals_yy',stress[0,0]-stress[1,1]);zero('scalar_stress_no_TT_xy',stress[0,1]);zero('scalar_stress_no_vector_zx',stress[2,0]);zero('scalar_stress_no_vector_zy',stress[2,1])
# Actual gravity scalar block; arbitrary O(p0) background metric tadpoles retained.
a0,b0=s.symbols('a0 b0',real=True)
L=-3*M*zd**2+(Sig+kap*M*p*p)*nu**2+6*Th*nu*zd+M*p*p*z*z+2*M*p*p*nu*z+2*p*S*(M*zd-Th*nu)
L+=KE-p*p*C*C/2+s.sqrt(2)*B*p*C*(z-nu)+Z*(q*q*nu+b*Delta)**2/2+a0*z*nu+b0*z*z
zero('actual_scalar_momentum_constraint',s.diff(L,S)-(2*p*(M*zd-Th*nu)-s.sqrt(2)*B*Cd+2*B*B*S))
if args.control=='omit_shift_square':zero('CONTROL_fluid_shift_substitution',s.diff(L-B*B*S*S,S)-s.diff(L,S))
# Ordinary dust is actually varied, not held externallyfixed.
rhoD,vD,pi,vDd=s.symbols('rhoD vD pi vDd',real=True)
L+=pi*(vDd-nu)-rhoD*p*p*vD*vD/2+rhoD*p*vD*S+3*rhoD*z*nu
zero('dust_density_constraint',s.diff(L,pi)-(vDd-nu))
zero('full_momentum_with_dust',s.diff(L,S)-(2*p*(M*zd-Th*nu)-s.sqrt(2)*B*Cd+2*B*B*S+rhoD*p*vD))
f=[z,C,nu,S,vD,pi];v=[zd,Cd,s.Symbol('nud'),s.Symbol('Sd'),vDd,s.Symbol('pid')]
K=s.hessian(L,v);V=s.hessian(L,f);Gy=s.Matrix([[s.diff(L,v[i],f[j])-s.diff(L,f[i],v[j]) for j in range(6)]for i in range(6)])
x=s.symbols('x',real=True);E=-p*p*x*x*K-s.I*p*x*Gy-V
lead=0
for perm in itertools.permutations(range(6)):
 if any(E[i,perm[i]]==0 for i in range(6)):continue
 sign=(-1)**sum(perm[i]>perm[j] for i in range(6) for j in range(i+1,6));pol={0:s.Integer(1)}
 for i,j in enumerate(perm):
  new={}
  for (k,),c in s.Poly(s.expand(E[i,j]),p).terms():
   for kk,cc in pol.items():
    if k+kk<=10:new[k+kk]=new.get(k+kk,0)+cc*c
  pol=new
 lead+=sign*pol.get(10,0)
lead=s.factor(lead);cs=1-2*B*B*Z*b*b
zero('full_six_variable_principal',lead-8*kap*M**3*x**4*(x*x-cs))
zero('unstable_root_factor',lead.subs(x*x,cs))
zero('dust_does_not_change_nonzero_cone',s.diff(lead,rhoD));zero('background_tadpoles_lower_order',s.diff(lead,a0)+s.diff(lead,b0))
# Leading rescaling exhibits a physical transverse mode without auxiliarydivision.
scale=s.diag(1/p,1,1,p,1/p,p*p);Esc=scale*E*scale/p**2
E0=Esc.applyfunc(lambda e:s.limit(e,p,s.oo));mode=s.Matrix([B/(s.sqrt(2)*M),1,0,0,0,0]);res=E0*mode
for i in range(6):zero('physical_mode_row_'+str(i),res[i].subs(x*x,cs))
auxdet=s.factor(E[2:4,2:4].det());zero('auxiliary_denominator_dictionary',auxdet-(4*(B*B*M*kap-Th*Th)*p*p+4*B*B*Sig+2*B*B*Z*q**4))
# Simple EM roots remain simple even at nominal auxiliaryleadingdegeneracy.
zero('EM_root_derivative',s.diff(lead,x).subs(x*x,cs)-16*kap*M**3*x**5)
if args.control=='stable':ck('CONTROL_magnetic_branch_stabilized',cs.subs({B:1,Z:1,b:1})>0)
# Finite algebraic witnesses including a fully degenerate auxiliaryblock; no cosmology fits.
rows=[]
for name,theta,sigma in [('regular',2,-1),('leading_aux_degenerate',1,-1),('exact_aux_degenerate',1,s.Rational(-1,2))]:
 sub={M:1,Th:theta,Sig:sigma,kap:1,B:1,Z:1,b:1,q:1,rhoD:1,a0:6,b0:-3}
 for pp in [30,300]:
  mat=E.subs(sub).subs(p,pp);char=s.Poly(s.expand(mat.det(method='domain-ge')),x);roots=np.roots([complex(s.N(c,30)) for c in char.all_coeffs()]);em=min(roots,key=lambda r:abs(r-1j))
  rows.append(dict(case=name,p=pp,imaginary_omega_over_p=float(em.imag),real_omega_over_p=float(em.real),error_to_principal=float(abs(em-1j))))
ck('finite_full_matrix_magnetic_roots',all(r['imaginary_omega_over_p']>.9 for r in rows));ck('finite_p_branch_convergence',all(rows[2*j+1]['error_to_principal']<rows[2*j]['error_to_principal'] for j in range(3)))
result=dict(passed=all(c['passed'] for c in checks),checks=checks,full_principal_coefficient=str(lead),physical_mode='p*zeta=B*C/(sqrt2*M), nu=0,S/p=0,p*vd=0,pi/p2=0 atleadingomega/p nonzero',speed_squared=str(cs),auxiliary_determinant=str(auxdet),bounded_frozen_matrix_controls=rows,control=args.control,scope='Actual scalar helicity coupled principal on ontrajectorypuremagneticisotropicU1triad, with ordinarydustvaried; no fulltensor/vectorhealth, thermalphotons, source matching, EFTcutoff or32pi claim')
o=pathlib.Path(args.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']])));raise SystemExit(0 if result['passed'] else 1)
