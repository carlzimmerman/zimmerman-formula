import sympy as s

def invariants(C,n):
 D=n+1;sg=[-1]+[1]*n
 c=[sum(C.get((j,i,j),0) for j in range(D)) for i in range(D)]
 cb=[sum(sg[j]*C.get((i,j,j),0) for j in range(D)) for i in range(D)]
 S1=sum(sg[i]*C.get((j,i,k),0)*C.get((k,i,j),0) for i in range(D) for j in range(D) for k in range(D))
 S2=sum(cb[i]*c[i] for i in range(D));S3=sum(sg[i]*cb[i]**2 for i in range(D));S4=sum(sg[i]*c[i]**2 for i in range(D));S5=sum(sg[i]*sg[j]*sg[k]*v*v for (i,j,k),v in C.items())
 return list(map(s.expand,[S1,S2,S3,S4,S5]))
def nr(n,pert=True):
 q=s.Rational(1,n-2);C={};D=n+1;a=[s.S(1)]+[s.S(0)]*(n-1)
 for i in range(1,D):
  C[i,0,0]=a[i-1];C[0,0,i]=C[0,i,0]=a[i-1]
  for j in range(1,D):
   for k in range(1,D): C[i,j,k]=-q*((i==j)*a[k-1]+(i==k)*a[j-1]-(j==k)*a[i-1])
 base=invariants(C,n)
 variables={}
 for i in range(1,D):
  for j in range(i,D):
   for k in range(1,D):variables[i,j,k]=s.Symbol('h%d%d%d'%(i,j,k))
 def h(i,j,k):return variables[min(i,j),max(i,j),k]
 eps=s.Symbol('eps')
 for i in range(1,D):
  for j in range(1,D):
   for k in range(1,D): C[i,j,k]+=eps*(h(i,k,j)+h(i,j,k)-h(j,k,i))/2
 lin=[s.expand(z).coeff(eps,1) for z in invariants(C,n)]
 mat=s.Matrix([[z.coeff(v) for z in lin] for v in variables.values()]+[base]);null=mat.nullspace()
 return base,null,mat

import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['kinetic_repair','drop_H','all_invisible']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
def ck(name,b,detail=''):rows.append({'name':name,'passed':bool(b),'residual':str(detail)})
# Independent raw tensor sums; no parent numerical imports.
d,v,g,H=s.symbols('d v g H');C={}
for i,sign in [(1,1),(2,-1)]:
 C[0,i,i]=sign*(H*d+v/2);C[i,0,i]=C[i,i,0]=sign*v/2
 C[i,i,3]=C[i,3,i]=sign*g/2;C[3,i,i]=-sign*g/2
TT=[s.expand(z/2) for z in invariants(C,3)]
expected=[H*d*v+(v*v-g*g)/4,0,0,0,-H*H*d*d-H*d*v-3*(v*v-g*g)/4]
for i in range(5):eq('raw_TT_S'+str(i+1),TT[i]-expected[i])
J=3*TT[0]-2*TT[1]-TT[3]+TT[4]
eq('invisible_J_TT',J-(2*H*d*v-H*H*d*d))
eq('J_kinetic_zero',s.diff(J,v,2))
eq('J_gradient_zero',s.diff(J,g,2))
# Full static spatial-metric derivative directions at finite tested dimensions.
for N in [3,4,5,6]:
 base,ns,mat=nr(N);vec=s.Matrix([3,-2,0,-1,1]);v3=s.Matrix([0,0,1,0,0]);eq('J_NRvalue_n'+str(N),sum(base[i]*vec[i] for i in range(5)))
 ck('J_all_NRspatial_firstvariations_n'+str(N),mat*vec==s.zeros(mat.rows,1))
 ck('S3_all_NRspatial_firstvariations_n'+str(N),mat*v3==s.zeros(mat.rows,1))
 ck('complete_NRinvisible_space_n'+str(N),len(ns)==2 and mat.rank()==3)
# Lapse variation is an exact tangent of the NR conformal branch.
for N in [3,4,5,6]:
 base,ns,mat=nr(N)
 eq('NR_lapse_tangent_zero_n'+str(N),3*base[0]-2*base[1]-base[3]+base[4])

# Pointwise temporal first variation is nonzero; stationary EL is a boundary.
for N in [3,4,5,6]:
 C={};aa=[s.S(1)]+[s.S(0)]*(N-1);qq=s.Rational(1,N-2)
 for i in range(1,N+1):
  C[i,0,0]=aa[i-1];C[0,0,i]=C[0,i,0]=aa[i-1]
  for j in range(1,N+1):
   for k in range(1,N+1): C[i,j,k]=-qq*((i==j)*aa[k-1]+(i==k)*aa[j-1]-(j==k)*aa[i-1])
 eps,u0,u1=s.symbols('eps u0 u1');C[0,0,1]+=eps*u0;C[0,1,0]+=eps*u0;C[1,0,0]+=eps*u1
 ss=invariants(C,N);lin=s.expand(3*ss[0]-2*ss[1]-ss[3]+ss[4]).coeff(eps,1)
 eq('raw_temporal_NR_shift_coefficient_n'+str(N),lin-4*(1+qq)*(u0-u1))

# Exact general-n basis equation, independent of finite dimension checks.
N=s.symbols('n',integer=True,positive=True);q=1/(N-2);a1,a2,a3,a4,a5=s.symbols('a1 a2 a3 a4 a5');P,R=s.symbols('P R');S1=-(N-1)/(N-2);S4=4*q*q;S5=-3*S1+S4
lin=-2*q*(a1+a2-a5)*P-4*q*(a4+a5)*R
val=a1*S1+a4*S4+a5*S5
sol={a1:3*a5,a2:-2*a5,a4:-a5}
eq('general_n_firstvariation_null',lin.subs(sol));eq('general_n_value_null',val.subs(sol))
# de Sitter integration and corrected action EOM.
t=s.symbols('t');D=s.Function('D')(t);a=s.exp(H*t);K,m,xi,k=s.symbols('K m xi k',positive=True);Qt=2*H*D*s.diff(D,t)-H*H*D*D
integ=-((N+1)*H*H)*D*D
boundary=s.diff(a**N*H*D*D,t)
eq('general_n_J_IBP',a**N*Qt-a**N*integ-boundary)
kin=K*(1-2*m)/8;pot=K*(m*N-xi*(N+1))*H*H/2
L=a**N*(kin*(s.diff(D,t)**2-k*k*D*D/a**2)+pot*D*D)
EL=s.diff(s.diff(L,s.diff(D,t)),t)-s.diff(L,D)
mu2=4*(xi*(N+1)-m*N)*H*H/(1-2*m)
eq('corrected_comoving_EOM',s.simplify(EL/(2*kin*a**N)-s.diff(D,t,2)-N*H*s.diff(D,t)-(k*k/a**2+mu2)*D))
ck('explicit_regular_stable_cone',kin.subs({m:s.Rational(1,4),K:1})>0 and mu2.subs({m:s.Rational(1,4),xi:s.Rational(1,4),N:3,H:1})>0)
eq('explicit_mass_squared',mu2.subs({m:s.Rational(1,4),xi:s.Rational(1,4),N:3})-2*H*H)
eq('critical_kinetic_still_zero',kin.subs(m,s.Rational(1,2)))
# Actual false propositions, not Boolean flips.
if args.mutation=='kinetic_repair':eq('claim_J_repairs_critical_kinetic',s.diff(J,v,2)-1)
if args.mutation=='drop_H':eq('claim_drop_background_H',J)
if args.mutation=='all_invisible':
 base,ns,mat=nr(3);ck('claim_S5_value_invisible',base[4]==0,base[4])
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'mutation':args.mutation,'scope':'general-n proof identities plus raw finite-n tensor/NR contractions; no scalar-vector health'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
