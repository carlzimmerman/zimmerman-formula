"""Direct ADM/covariant transverse-vector expansion; no Claude model imported."""
from pathlib import Path
import sympy as s
import json,sys,time,resource,math
out=Path(sys.argv[1]);start=time.monotonic()
e=s.symbols('epsilon',real=True);t,x,y,z=s.symbols('t x y z',real=True);xs=[t,x,y,z]
a=s.Function('a',positive=True)(t);B=s.Function('B')(t,z);v=s.Function('v')(t,z)
chi=s.Function('chi')(t);C=s.diff(chi,t);Cd=s.diff(C,t);H=s.diff(a,t)/a
rho=s.Function('rho',positive=True)(t);lam=s.Function('lambda')(t)
K,gamma=s.symbols('K gamma',positive=True)
checks=[]
def tr(q,n=2):
 q=s.expand(q);return sum(q.coeff(e,j)*e**j for j in range(n+1))
def coeff(q,j):return s.simplify(s.expand(q).coeff(e,j))
def ck(name,q):checks.append({'check':name,'passed':bool(q)})
def eq(q,r=0):return s.simplify(q-r)==0
g=s.diag(-1,a*a,a*a,a*a);g[0,0]=-1+e*e*a*a*B*B;g[0,2]=g[2,0]=e*a*a*B
gi=s.diag(-1,a**-2,a**-2,a**-2);gi[0,2]=gi[2,0]=e*B;gi[2,2]=a**-2-e*e*B*B
ck('exact ADM inverse',all(eq(q) for q in g*gi-s.eye(4)))
ck('ADM volume independent of transverse shift',eq(g.det(),-a**6))
U=B+v;lorentz=1+e*e*a*a*U*U/2
u=s.Matrix([lorentz,0,e*v,0]);uc=(g*u).applyfunc(tr)
ck('fluid normalization through quadratic order',eq(tr((u.T*g*u)[0]),-1))
h=(gi+u*u.T).applyfunc(tr);hc=(g+uc*uc.T).applyfunc(tr);P=(s.eye(4)+uc*u.T).applyfunc(tr)
ck('projector annihilates fluid through quadratic order',all(eq(tr(q)) for q in P*uc))
Gamma={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   Gamma[i,j,k]=tr(sum(gi[i,l]*(s.diff(g[l,k],xs[j])+s.diff(g[l,j],xs[k])-s.diff(g[j,k],xs[l]))/2 for l in range(4)))
A=s.Matrix(4,4,lambda i,j:tr((Cd if i==j==0 else 0)-C*Gamma[0,i,j]))
D2=tr(sum(h[i,j]*A[i,j] for i in range(4) for j in range(4)))
ck('homogeneous projected Hessian trace',eq(coeff(D2,0),-3*H*C))
ck('no transverse linear scalar constraint',eq(coeff(D2,1)))
ck('quadratic projected trace retains multiplier inertia',eq(coeff(D2,2),a*a*(Cd-H*C)*U*U))
T=(P*A*P.T).applyfunc(lambda q:tr(q))-hc*D2/3
T=T.applyfunc(lambda q:tr(q))
N=s.Matrix(4,4,lambda i,j:tr(s.diff(uc[j],xs[i])-sum(Gamma[k,i,j]*uc[k] for k in range(4))))
theta=tr(sum(gi[i,j]*N[i,j] for i in range(4) for j in range(4)))
Sig=(P*(N+N.T)*P.T/2-hc*theta/3).applyfunc(tr)
T1=T.applyfunc(lambda q:coeff(q,1));S1=Sig.applyfunc(lambda q:coeff(q,1))
ck('original tidal yz geometry',eq(T1[2,3],C*a*a*s.diff(B,z)/2))
ck('fluid shear yz geometry',eq(S1[2,3],a*a*s.diff(v,z)/2))
Tnew=(T1+C*S1).applyfunc(s.simplify)
ck('alpha1 yz is relative-velocity gradient',eq(Tnew[2,3],C*a*a*s.diff(U,z)/2))
ck('alpha1 remaining components vanish',all(eq(Tnew[i,j]) for i in range(4) for j in range(4) if (i,j) not in [(2,3),(3,2)]))
gibg=gi.subs(e,0)
norm=s.simplify(sum(gibg[i,k]*gibg[j,l]*Tnew[i,j]*Tnew[k,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
ck('full tidal-square transverse normalization',eq(norm,C*C*s.diff(U,z)**2/2))
grad=tr(h[0,0]*C*C)
ck('W_full quadratic gradient includes relative velocity',eq(coeff(grad,2),C*C*a*a*U*U))
mn=rho*(1-e*e*a*a*U*U/2)
Lmatter=tr(-mn-grad/(2*K)+lam*(D2-K*mn))
A0=rho*(1+K*lam)-C*C/K+2*lam*(Cd-H*C)
ck('dust W and multiplier quadratic inertia',eq(coeff(Lmatter,2),a*a*A0*U*U/2))
# Flat spatial metric; K_ij=(dot h_ij-D_i N_j-D_j N_i)/2, N=1.
h3=s.eye(3)*a*a;Ncov=s.Matrix([0,e*a*a*B,0]);xyz=[x,y,z]
Extr=s.Matrix(3,3,lambda i,j:s.diff(h3[i,j],t)/2-(s.diff(Ncov[j],xyz[i])+s.diff(Ncov[i],xyz[j]))/2)
Exmixed=h3.inv()*Extr
ADM=(s.trace(Exmixed*Exmixed)-s.trace(Exmixed)**2)/(4*K)
ck('EH full ADM transverse shift sign',eq(coeff(ADM,2),s.diff(B,z)**2/(8*K)))
# Physical Fourier velocities p=a*v, b=a*B, wavenumber q=kcom/a.
q,p,b=s.symbols('q p b',real=True);M,d=s.symbols('A0 delta',positive=True)
G=q*q/(4*K);At=M-3*gamma*C*C*q*q/(4*K*K)
LV=(At*(p+b)**2+G*b*b)/2
bsol=s.solve(s.diff(LV,b),b)[0]
Ired=s.simplify(2*LV.subs(b,bsol)/p**2)
ck('metric shift exact elimination',eq(Ired,At*G/(At+G)))
ck('homogeneous multiplier zero branch is a solution',eq(s.diff(a**3*H*lam,t).subs({lam:0,s.diff(lam,t):0})))
f,L=s.symbols('f L',positive=True)
M0=rho*(1-f/6)
ck('lambda0 dust background inertia from constraint Friedmann',eq((rho-C*C/K).subs(C*C,K*rho*f/6),M0))
ck('source gamma is K Lstar squared over2',eq((M0/(3*gamma*C*C/(4*K*K))).subs({gamma:K*L*L/2,C*C:K*rho*f/6})*L*L,16/f-s.Rational(8,3)))
# Dimensionless b/G variable avoids rounding and states the entire sign proof.
bb=s.symbols('b',positive=True)
F=(M-d*bb)*bb/(M+(1-d)*bb)
for name,dd,bvalue,expected in [('small_delta',s.Rational(1,2),3,True),('unit_delta',s.Integer(1),2,True),('large_delta_band',s.Integer(2),s.Rational(3,4),True),('large_delta_beyond_pole',s.Integer(2),2,False)]:
 val=s.simplify(F.subs({M:1,d:dd,bb:bvalue}));ck(name+' exact sign',bool(val<0)==expected)
ck('kinetic zero is b=A0/delta',eq(s.factor(s.together(F)).subs(bb,M/d)))
ck('constraint denominator vanishes at separate pole for delta>1',eq((M+(1-d)*bb).subs(bb,M/(d-1))))
# Additional healthy ideal-fluid vector kinetic sectors retained in the shift.
J,w=s.symbols('J w',positive=True)
Lmulti=(At*(p+b)**2+J*(w+b)**2+G*b*b)/2
bm=s.solve(s.diff(Lmulti,b),b)[0]
Kmm=s.simplify(s.diff(Lmulti.subs(b,bm),p,p))
ck('healthy extra fluid retained principal diagonal',eq(Kmm,At*(G+J)/(At+G+J)))
zeta=s.symbols('zeta',positive=True)
ck('negative admissible multifluid direction just after crossing',bool((-zeta*(G+J)/(G+J-zeta)).subs({G:1,J:1,zeta:s.Rational(1,2)})<0))
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;rss_bytes=int(rss if sys.platform=='darwin' else rss*1024)
ck('measured RSS below shared one GB limit',rss_bytes<1000000000)
result={'claim':'For alpha1 on a homogeneous FRW background, retained transverse metric constraint yields I_V=A b/(A+b), A=A0-delta b. If A0>0,delta>0, there is a nonempty negative kinetic interval unless excluded by justified EFT cutoff.','scope':'Exact transverse quadratic sector, no scalar-sector elimination, no exponential growth rate, no universal completion no-go or dwarf mechanism. Fourier action normalized with a common positive real-mode phase-average factor removed. c=1.','A0':str(A0),'projected_Hessian_trace_quadratic':str(coeff(D2,2)),'tidal_norm_linear_squared':str(norm),'shift_solution':str(bsol),'I_V':str(Ired),'delta':'3*gamma*C**2/K','sign_intervals':{'0<delta<=1':'b>A0/delta','delta>1':'A0/delta<b<A0/(delta-1)','b':'kphys**2/(4*K)','degenerate':'A+b=0 cannot be divided out; A=0 is kinetic degeneracy, not an ordinary mode'},'physical_scope':'lambda_bar=0 is a consistent exact homogeneous branch. With dust/radiation GR and cold fraction0<f<=1, A0=rho*(1-f/6)>0. Original source gamma=K Lstar**2/2 gives onset kphys**2 Lstar**2=16/f-8/3. A cutoff below onset is a separate unproved route, not excluded here.','checks':checks,'passed':all(c['passed'] for c in checks),'runtime_seconds':time.monotonic()-start,'maximum_measured_RSS_bytes':rss_bytes}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'checks':len(checks),'maximum_measured_RSS_bytes':rss_bytes}))
sys.exit(0 if result['passed'] else 1)
