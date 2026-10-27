import sympy as s,json,sys
from pathlib import Path
x,y,z=s.symbols('x y z',real=True); coords=(x,y,z);pt={x:1,y:1,z:0};checks=[]
def eq(name,expr,expected=0):
 diff=s.simplify(expr-expected);assert diff==0,(name,diff);checks.append(name)
def yes(name,expr):
 assert expr is True,(name,expr);checks.append(name)
Phi=-1/s.sqrt((x-1)**2+y*y+z*z)-1/s.sqrt((x+1)**2+y*y+z*z)
q=s.Matrix([s.diff(Phi,v) for v in coords]);J=q.jacobian(coords)
qp=s.simplify(q.subs(pt));Jp=s.simplify(J.subs(pt));v=s.Matrix([2/(5*s.sqrt(5)),1+1/(5*s.sqrt(5)),0])
for i in range(3):eq('actual_potential_gradient_'+str(i),qp[i],v[i])
for i in range(3):
 for j in range(i,3):eq('Hessian_symmetry_'+str(i)+str(j),Jp[i,j],Jp[j,i])
eq('actual_vacuum_laplacian',s.trace(Jp))
normsq=s.simplify(qp.dot(qp));eq('actual_norm_square',normsq,(26+2*s.sqrt(5))/25);yes('nonzero_norm',normsq.is_positive)
C=s.simplify((Jp*qp).cross(qp))
for i in range(3):eq('actual_Hessian_cross_'+str(i),C[i],24*s.sqrt(5)/125 if i==2 else 0)
# Differentiate actual boosted components first with a generic radial kernel.
a0=s.symbols('a0',positive=True);N=s.Function('N');mag=s.sqrt(q.dot(q));A=N(mag/a0)*q
curl=s.Matrix([s.diff(A[2],y)-s.diff(A[1],z),s.diff(A[0],z)-s.diff(A[2],x),s.diff(A[1],x)-s.diff(A[0],y)])
# Evaluate at point only then normalize a0 to its positive actual norm.
expected=s.Subs(s.Derivative(N(s.Symbol('u')),s.Symbol('u')),s.Symbol('u'),mag/a0)*(J*q).cross(q)/(a0*mag)
for i in range(3):eq('actual_vector_chain_rule_'+str(i),(curl[i]-expected[i]).subs(pt))
u=s.symbols('u',positive=True);nu=1/(1-s.exp(-s.sqrt(u)));nup=s.diff(nu,u).subs(u,1)
eq('actual_low_y_derivative',nup,-s.exp(-1)/(2*(1-s.exp(-1))**2));yes('actual_derivative_negative',nup.is_negative)
actualcurl=s.simplify(nup*C[2]/normsq);yes('actual_vector_curl_nonzero',actualcurl.is_negative)
# Control: single positive source gradient and Hessian give no geometric cross.
P1=-1/s.sqrt(x*x+y*y+z*z);q1=s.Matrix([s.diff(P1,v) for v in coords]);J1=q1.jacobian(coords)
for i in range(3):eq('single_source_curl_geometry_'+str(i),((J1*q1).cross(q1))[i].subs(pt))
for i in range(3):eq('constant_boost_curl_'+str(i),(s.Matrix([s.diff(q[2],y)-s.diff(q[1],z),s.diff(q[0],z)-s.diff(q[2],x),s.diff(q[1],x)-s.diff(q[0],y)])[i]).subs(pt))
result={'all_passed':True,'count':len(checks),'checks':checks,'gradient':str(qp),'Hessian_cross':str(C),'kernel_derivative_at1':str(nup),'boost_curl_z_at_point':str(actualcurl),'scope':'literalvectorreading only, finite two-positive-condensed-source exterior witness; no scalarA2/model/empiricalclosure'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
