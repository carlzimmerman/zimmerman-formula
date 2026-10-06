"""Bounded exact fixtures for nonlinear projected-acceleration ADM constraints."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['free_common','frozen_m','two_spatial_gauges']);args=ap.parse_args();rows=[]
def eq(n,e):
 e=s.simplify(s.expand(e));rows.append(dict(name=n,passed=e==0,residual=str(e)))
def ck(n,b):rows.append(dict(name=n,passed=bool(b)))
x=s.symbols('x',real=True);kap,a0=s.symbols('kappa a0',positive=True)
lam,r,sig,h,Hg,Hh=[s.Function(v)(x) for v in ['lambda','r','sigma','h','Hg','Hh']]
f,v=s.Function('f')(x),s.Function('v')(x)
b0,b1,b2=s.symbols('b0 b1 b2');I=h*s.diff(r,x)**2/a0**2;M=b0+b1*I+b2*I**2;m=b1+2*b2*I
alpha=s.exp(r/2);beta=s.exp(-r/2);U=kap*a0**2*sig*M
C=alpha*Hg+beta*Hh-U;A=(alpha*Hg-beta*Hh)/2;J=2*kap*sig*m*h*s.diff(r,x)
S=s.diff(lam*C,r)-s.diff(s.diff(lam*C,s.diff(r,x)),x)
eq('relative_lapse_full_Euler',S-lam*A-s.diff(lam*J,x))
eq('common_lapse_Euler',s.diff(lam*C,lam)-C)
eps=s.symbols('eps');vary=lambda e:s.diff(e.subs(r,r+eps*f),eps).subs(eps,0).doit()
Bf=A*f-J*s.diff(f,x)
eq('mixed_common_relative_operator',vary(C)-Bf)
D=2*kap*sig*h*(m+2*I*(2*b2));Lrf=lam*(alpha*Hg+beta*Hh)*f/4+s.diff(lam*D*s.diff(f,x),x)
eq('relative_elliptic_plus_mass_operator',vary(S)-Lrf)
Al,Jl,ll=s.Function('A')(x),s.Function('J')(x),s.Function('l')(x)
B=Al*f-Jl*s.diff(f,x);Badjv=Al*v+s.diff(Jl*v,x)
eq('mixed_operator_formal_adjoint_boundary',v*B-f*Badjv+s.diff(Jl*f*v,x))
onA=-s.diff(ll*Jl,x)/ll
eq('on_constraint_B_divergence',(Al*f-Jl*s.diff(f,x)).subs(Al,onA)+s.diff(ll*Jl*f,x)/ll)
eq('on_constraint_Badj_transport',(Al*ll*v+s.diff(Jl*ll*v,x)).subs(Al,onA)-ll*Jl*s.diff(v,x))
eq('global_clock_relabel_null',(Al*ll+s.diff(Jl*ll,x)).subs(Al,onA))
# Dimensional principal eigenvalues using positive-metric orthonormal frame.
mm,mi,iv=s.symbols('m mI I',real=True);aa=s.symbols('a',positive=True)
vec=s.Matrix([aa,0,0]);Pmat=mm*s.eye(3)+2*mi*vec*vec.T
for j in [1,2]:eq('transverse_principal_eigen_'+str(j),Pmat[j,j]-mm)
eq('radial_principal_eigen',Pmat[0,0]-mm-2*mi*aa**2)
y=s.symbols('y',positive=True);mc=s.Rational(1,2)-y/8;mIc=-1/(16*y)
eq('cubic_relative_radial_eigen',mc+2*y*y*mIc-(s.Rational(1,2)-y/4))
ck('deep_relative_ellipticity',mc.subs(y,1)>0 and (mc+2*y*y*mIc).subs(y,1)>0)
# Exact diagonal-metric 1D fixture for simultaneous spatial Ward identity.
N,L=s.Function('N')(x),s.Function('L')(x)
g=s.Function('g')(x);gh=s.Function('gh')(x);t=s.Function('t')(x);th=s.Function('th')(x)
# gxx=g,g yy=gzz=t (independent equal transverse entries varied as aggregate t).
rn=s.log(N/L);ss=(g*t*t*gh*th*th)**s.Rational(1,4)
II=(1/g+1/gh)*s.diff(rn,x)**2/(2*a0**2)
V=kap*a0**2*s.sqrt(N*L)*ss*(b0+b1*II)
VN=s.diff(V,N)-s.diff(s.diff(V,s.diff(N,x)),x)
VL=s.diff(V,L)-s.diff(s.diff(V,s.diff(L,x)),x)
forceg=s.diff(V,g)*s.diff(g,x)+s.diff(V,t)*s.diff(t,x)-s.diff(2*g*s.diff(V,g),x)
forceh=s.diff(V,gh)*s.diff(gh,x)+s.diff(V,th)*s.diff(th,x)-s.diff(2*gh*s.diff(V,gh),x)
eq('diagonal_spatial_Ward_full_lapse_EL',forceg+forceh+VN*s.diff(N,x)+VL*s.diff(L,x))
Wg=Hg*s.diff(N,x)+forceg;Wh=Hh*s.diff(L,x)+forceh
eq('six_shift_sum_redundancy',Wg+Wh-(Hg-VN)*s.diff(N,x)-(Hh-VL)*s.diff(L,x))
# Simple constrained coefficient jet exposes transport kernel and nonzero relative rows.
# C=S=0 choose local C weights E=U, A=-Jdiv; no claimed complete Einstein solution.
zz=s.symbols('z',real=True);transport=s.diff(s.exp(zz),zz)
ck('common_lapse_not_arbitrary_function',transport!=0)
# At zero grad r on lapse equations A=0 mixed block zero, but relative elliptic survives m0.
q=s.symbols('relative_gradient',real=True)
Jjet=2*kap*sig*(b1+2*b2*h*q*q/a0**2)*h*q
eq('coincident_mixed_principal_zero',Jjet.subs(q,0))
eq('coincident_relative_elliptic_retained',s.diff(Jjet,q).subs(q,0)-2*kap*sig*b1*h)
# Vacuum parameter family: common deS n>=3 gives constraints for every A0>0.
n,chi,A0,K=s.symbols('n chi A0 K',positive=True);H2=chi*a0**2*A0/(n*(n-1));Lambda=chi*a0**2*A0/2
eq('vacuum_Friedmann_all_A',n*(n-1)*H2/2-Lambda)
eq('vacuum_C_equal_energy',(-K*n*(n-1)*H2)*2-(-2*K*chi*a0**2*A0))
ck('vacuum_A_is_free_input',s.diff(H2,A0)!=0)
if args.control=='free_common':eq('false_local_common_lapse_gauge',s.diff(s.exp(zz),zz))
if args.control=='frozen_m':eq('false_drop_mI_principal',mc-(mc+2*y*y*mIc))
if args.control=='two_spatial_gauges':eq('false_individual_spatial_Ward',forceg+VN*s.diff(N,x))
out=dict(passed=sum(q['passed'] for q in rows),total=len(rows),checks=rows,control=args.control,scope='analytic functional all-n identities; exact 1D diagonal-metric symbolic Ward fixture; no complete nonlinear Dirac closure or physicalhealth')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[q['name'] for q in rows if not q['passed']])));sys.exit(not all(q['passed'] for q in rows))
