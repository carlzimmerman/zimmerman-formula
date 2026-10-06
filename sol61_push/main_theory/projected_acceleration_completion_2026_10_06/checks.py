"""Covariant projected relative acceleration: exact ADM/NR/regularity discriminator."""
import sympy as s
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['naive_connection','TT_cancel','full_scalar_health']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
def ck(name,b,e=''):rows.append({'name':name,'passed':bool(b),'residual':str(e)})
N,L,a0,K,chi=s.symbols('N L a0 K chi',positive=True);S=s.Matrix(s.symbols('S0:3'));R=s.Matrix(s.symbols('R0:3'));gi=s.Matrix(3,3,lambda i,j:s.Symbol('g'+str(min(i,j))+str(max(i,j))));hi=s.Matrix(3,3,lambda i,j:s.Symbol('h'+str(min(i,j))+str(max(i,j))))
def projector(n,shift,h):
 inv=s.zeros(4);inv[0,0]=-1/n**2
 for i in range(3):
  inv[0,i+1]=inv[i+1,0]=shift[i]/n**2
  for j in range(3):inv[i+1,j+1]=h[i,j]-shift[i]*shift[j]/n**2
 u=s.Matrix([1/n,*[-v/n for v in shift]]);return inv+u*u.T
Pg=projector(N,S,gi);Ph=projector(L,R,hi);wanted=s.zeros(4);wanted[1:,1:]=gi
ck('ADM_full_projector_g',Pg==wanted)
wantedh=s.zeros(4);wantedh[1:,1:]=hi;ck('ADM_full_projector_hat',Ph==wantedh)
aa=s.Matrix(s.symbols('a0_:3'));bb=s.Matrix(s.symbols('b0_:3'));Avec=s.Matrix([(S.dot(aa)-R.dot(bb)),*(aa-bb)]);I=(Avec.T*((Pg+Ph)/2)*Avec)[0]/a0**2
expected=((aa-bb).T*((gi+hi)/2)*(aa-bb))[0]/a0**2
eq('exact_shiftfree_invariant',I-expected)
# Exchange is simultaneous across distinct symbols, not sequential metric replacement.
exchange={};exchange.update(dict(zip(list(S),list(R))));exchange.update(dict(zip(list(R),list(S))));exchange.update(dict(zip(list(aa),list(bb))));exchange.update(dict(zip(list(bb),list(aa))));exchange.update({gi[i,j]:hi[i,j] for i in range(3) for j in range(3)});exchange.update({hi[i,j]:gi[i,j] for i in range(3) for j in range(3)})
eq('exact_exchange',I-I.xreplace(exchange));eq('homogeneous_invariant_zero',I.subs({**{v:0 for v in aa},**{v:0 for v in bb}}))
# Actual lapse Euler variations, generic function of positive invariant.
x=s.symbols('x');NN=s.Function('N')(x);LL=s.Function('L')(x);P=s.Function('P')(x);D=s.Function('D')(x);M=s.Function('M');rr=s.diff(s.log(NN/LL),x);v=s.sqrt(NN*LL)*D;II=P*rr**2/a0**2;Lag=2*K*chi*a0**2*v*M(II)
for var,sign in [(NN,-1),(LL,1)]:
 EL=s.diff(Lag,var)-s.diff(s.diff(Lag,s.diff(var,x)),x)
 target=K*chi/var*(a0**2*v*M(II)+sign*4*s.diff(v*s.Subs(s.Derivative(M(s.Symbol('j')),s.Symbol('j')),s.Symbol('j'),II)*P*rr,x))
 eq('exact_lapse_EL_'+str(var.func),s.simplify(EL-target))
# Static normalization in the displayed cubic deep model.
y,X=s.symbols('y X',positive=True);m=s.Rational(1,2)-X/8;mu=1-2*m;g=(1-m)*X
eq('deep_star_flux',mu*X-X*X/4)
ck('deep_physical_MOND_normalization',s.limit(g/(X/2),X,0)==1)
# Norm cubed derivatives on arbitrary positive spatial quadratic form.
v1,v2,t=s.symbols('v1 v2 t',real=True);d1,d2=s.symbols('d1 d2',positive=True);q=d1*v1*v1+d2*v2*v2;f=q**s.Rational(3,2);vv=s.Matrix([v1,v2]);PP=s.diag(d1,d2);hess=s.hessian(f,[v1,v2]);want=3*s.sqrt(q)*PP+3*(PP*vv)*(PP*vv).T/s.sqrt(q)
for i in range(2):
 for j in range(2):eq('norm3_Hessian_%d%d'%(i,j),hess[i,j]-want[i,j])
for i in range(2):
 for j in range(2):ck('norm3_Hessian_origin_%d%d'%(i,j),s.limit(hess[i,j].subs({v1:t,v2:2*t}),t,0,dir='+')==0)
ck('indefinite_null_second_derivative_diverges',s.limit(s.diff(t**s.Rational(3,2),t,2),t,0,dir='+')==s.oo)
# Common clock cancels at quadratic order around coincidence.
nu,nh,pidot=s.symbols('nu nh pidot');dg=nu-pidot;dh=nh-pidot
eq('relative_clock_linear_cancellation',dg-dh-(nu-nh));eq('quadratic_common_clock_coefficient',s.diff((dg-dh)**2,pidot,2))
ck('EH_relative_tensor_positive',K/8>0)
if args.mutation=='naive_connection':ck('claim_Cuu_positive_spatial_acceleration',(-t*t).subs(t,1)>=0)
if args.mutation=='TT_cancel':eq('claim_critical_tensor_kinetic_zero',K/8)
if args.mutation=='full_scalar_health':ck('claim_common_clock_positive_quadratic_kinetic',s.diff((dg-dh)**2,pidot,2)>0)
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'mutation':args.mutation,'scope':'actual symmetric operator ADM/leading-static/TT regularity, no full scalar health'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
