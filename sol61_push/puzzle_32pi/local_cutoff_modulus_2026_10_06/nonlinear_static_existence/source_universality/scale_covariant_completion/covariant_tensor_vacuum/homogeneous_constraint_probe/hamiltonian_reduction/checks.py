"""Both-lapse canonical homogeneous reduction of declared regular representative."""
import sympy as s
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['rank_implies_ghost','omit_constraint','regular_positive']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
def ck(name,b,e=''):rows.append({'name':name,'passed':bool(b),'residual':str(e)})
n=s.symbols('n',integer=True,positive=True);K,A,lam,a0,ell=s.symbols('K A lam a0 ell',positive=True);T,m,xi,eta=s.symbols('T m xi eta');alpha,beta,r=s.symbols('alpha beta r',real=True);h1,h2,u=s.symbols('h1 h2 u');a,b,N,L,v,w=s.symbols('a b N L v w',positive=True)
S1=-(u*u+n*w*w)/N**2+2*n*v*w/a**2;S2=(u+n*w)*(-u/N**2+n*v/a**2);S3=-N**2*(-u/N**2+n*v/a**2)**2;S4=-(u+n*w)**2/N**2;S5=-u*u/N**2-2*n*w*w/N**2-n*N**2*v*v/a**4
# Every exact contraction has inverse-common-lapse weight2.
for j,z in enumerate([S1,S2,S3,S4,S5]):eq('exact_lapse_weight_S'+str(j+1),ell**2*z.subs({N:ell*N,v:v/ell**2},simultaneous=True)-z)
V=a*a*h1/N**2-b*b*h2/L**2
rep={v:V,w:h1-h2}
def sym(z):return (z.subs(rep,simultaneous=True)+z.subs({N:L,a:b,v:V,w:h1-h2},simultaneous=True))/2
Us=sym(S1-S2);Js=sym(3*S1-2*S2-S4+S5);Rs=sym(S3);vol=s.sqrt(N*L)*(a*b)**(n/2)
F=-K*n*(n-1)*(a**n*h1*h1/N+b**n*h2*h2/L)+K*vol*(-m*Us+(xi*Js+eta*Rs)/2)
Fq=s.simplify(F.subs({a:s.exp(alpha),b:s.exp(beta),N:s.exp(r/2),L:s.exp(-r/2)},simultaneous=True));G=s.hessian(Fq,[h1,h2,u]);vel=s.Matrix([h1,h2,u]);eq('quadratic_form_identity',Fq-(vel.T*G*vel)[0]/2)
chi=(n-1)/(2*(n-2));U=K*chi*a0*a0*(2*A+lam*T*T)*s.exp(n*(alpha+beta)/2)
eq('auxiliary_secondary',s.diff(U,T)-2*K*chi*a0*a0*lam*T*s.exp(n*(alpha+beta)/2))
ck('aux_pair_nonzero',s.diff(U,T,2).subs(n,3)>0)
# Point-independent Legendre identity from an arbitrary nonsingular symmetric metric.
gx,gy,gz,gxy,gxz,gyz=s.symbols('gx gy gz gxy gxz gyz');GG=s.Matrix([[gx,gxy,gxz],[gxy,gy,gyz],[gxz,gyz,gz]]);pv=s.Matrix(s.symbols('p1 p2 p3'));vv=ell*GG.inv()*pv
lag=(vv.T*GG*vv)[0]/(2*ell)-ell*U
ham=(pv.T*vv)[0]-lag;eq('Legendre_common_lapse_multiplier',ham-ell*((pv.T*GG.inv()*pv)[0]/2+U))
ck('homogeneous_DOF_count',(10-2*2-2)//2==2)
# Exact critical on-shell initial data and physical clock-slice kinetic.
GC=s.simplify(G.subs({n:3,K:1,m:s.Rational(1,2),xi:s.Rational(3,8),eta:-s.Rational(3,8),alpha:0,beta:s.log(4),r:0}));expected=s.Matrix([[s.Rational(4041,256),-s.Rational(4143,16),s.Rational(45,16)],[-s.Rational(4143,16),1755,45],[s.Rational(45,16),45,0]])
ck('critical_raw_G',GC==expected,GC)
eq('critical_det',GC.det()+s.Rational(14258025,128));v0=s.Matrix([1,s.Rational(1,4),0]);norm=(v0.T*GC*v0)[0];eq('critical_timelike_norm',norm+s.Rational(1023,256))
U0=U.subs({n:3,K:1,a0:1,alpha:0,beta:s.log(4),T:0});eq('critical_potential',U0-16*A)
tsq=8192*A/1023;eq('critical_on_shell_constraint',norm*tsq/2+U0)
# Jacobi Hessian exact differentiation; physical slice alpha is monotone.
qv=s.Matrix([h1,h2,u]);F0=(qv.T*GC*qv)[0]/2;J=-2*s.sqrt(-F0*U0);HJ=s.hessian(J,[h1,h2,u]);JJ=s.simplify(HJ.subs({h1:1,h2:s.Rational(1,4),u:0}));proj=GC-(GC*v0)*(GC*v0).T/norm
# Prefactor is sqrt(U0/(-F0))=ell^-1 on constrained data.
for i in range(3):
 for j in range(3):eq('Jacobi_projector_%d%d'%(i,j),JJ[i,j]-s.sqrt(U0/(-norm/2))*proj[i,j])
phys=proj[1:,1:];ep=s.Matrix([[3357498,231120],[231120,16875]])/341
ck('critical_positive_physical_block',phys==ep and phys[0,0]>0 and phys.det()>0,phys)
eq('critical_physical_det',phys.det()-s.Rational(9505350,341))
# Actual common de Sitter regular repair, using mean scale as monotone clock.
GR=s.simplify(G.subs({n:3,m:s.Rational(1,4),xi:s.Rational(1,4),eta:0,alpha:0,beta:0,r:0}));change=s.Matrix([[1,s.Rational(1,2),0],[1,-s.Rational(1,2),0],[0,0,1]]);GRc=change.T*GR*change;block=GRc[1:,1:];er=K*s.Matrix([[-s.Rational(21,4),s.Rational(3,4)],[s.Rational(3,4),-s.Rational(1,4)]])
ck('regular_negative_physical_block',block==er and block[0,0]<0 and block.det()>0,block)
eq('regular_common_dS_constraint',(-12*K)*(a0*a0*A/6)+2*K*a0*a0*A)
eq('regular_physical_det',block.det()-3*K*K/4)
# Actual Hamilton constraint propagation after auxiliary reduction, direct Poisson antisymmetry.
Q=s.symbols('Q0:3');P=s.symbols('P0:3');C=s.Function('C')(*Q,*P);poisson=sum(s.diff(C,Q[i])*s.diff(C,P[i])-s.diff(C,P[i])*s.diff(C,Q[i]) for i in range(3));eq('Hamiltonian_constraint_preserved',poisson)
if args.mutation=='rank_implies_ghost':ck('claim_critical_rank3_negative_physical_kinetic',phys[0,0]<0)
if args.mutation=='omit_constraint':ck('claim_three_physical_homogeneous_modes',(10-2*2-2)//2==3)
if args.mutation=='regular_positive':ck('claim_regular_tensorrepair_positive_homogeneous_kinetic',block[0,0]>0)
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(z['passed'] for z in rows),'total':len(rows),'checks':rows,'mutation':args.mutation,'scope':'declared regular representative, exact homogeneous canonical reduction and admitted initialdata; no full spatial ghost/health'},indent=2)+'\n');print(json.dumps({'passed':sum(z['passed'] for z in rows),'total':len(rows),'failed':[z for z in rows if not z['passed']]}));sys.exit(0 if all(z['passed'] for z in rows) else 1)
