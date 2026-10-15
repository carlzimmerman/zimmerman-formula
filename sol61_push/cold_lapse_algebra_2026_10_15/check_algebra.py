import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
z=s.symbols('z',real=True);h=s.symbols('h',positive=True)
a,b,c=[s.Function(v)(z) for v in ['a','b','c']]
pa,pb,pc=[s.Function(v)(z) for v in ['pa','pb','pc']]
n,m=[s.Function(v)(z) for v in ['n','m']]
qs=[a,b,c];ps=[pa,pb,pc]
checks=[]
def ck(name,e):
 assert s.simplify(e)==0,(name,e)
 checks.append(name)
root=s.sqrt(a*b*c)
R=-s.diff(a,z,2)/(a*c)-s.diff(b,z,2)/(b*c)+s.diff(a,z)**2/(2*a*a*c)+s.diff(b,z)**2/(2*b*b*c)-s.diff(a,z)*s.diff(b,z)/(2*a*b*c)+s.diff(a,z)*s.diff(c,z)/(2*a*c*c)+s.diff(b,z)*s.diff(c,z)/(2*b*c*c)
P=pa*s.diff(a,z)+pb*s.diff(b,z)-pc*s.diff(c,z)-2*c*s.diff(pc,z)
kin=(2*((a*pa)**2+(b*pb)**2+(c*pc)**2)-(a*pa+b*pb+c*pc)**2)/root
V=h*root*((1/a-1)**2+(1/b-1)**2+(1/c-1)**2)/2
H=kin-root*R/2+P*P/(8*h*root)+V
flat={q:1 for q in qs}
for q in qs:
 for j in range(1,6):flat[s.diff(q,z,j)]=0
flatten=lambda e:s.simplify(e.xreplace(flat))
def euler(L,q,order):
 return sum((-1)**j*s.diff(s.diff(L,s.diff(q,z,j)),z,j) for j in range(order+1))
Eq=[flatten(euler(n*H,q,2)) for q in qs]
Ep=[flatten(euler(n*H,p,1)) for p in ps]
S=pa+pb+pc;P0=-2*s.diff(pc,z);T=P0*P0/(8*h);K=2*(pa*pa+pb*pb+pc*pc)-S*S
A=[4*p*p-2*S*p-K/2-T/2 for p in ps]
A[0]-=s.diff(P0*pa,z)/(4*h);A[1]-=s.diff(P0*pb,z)/(4*h)
A[2]+=(s.diff(P0,z)*pc-P0*s.diff(pc,z))/(4*h)
B=[-P0*pa/(4*h),-P0*pb/(4*h),P0*pc/(4*h)]
D=[4*p-2*S for p in ps];D[2]+=s.diff(P0,z)/(2*h)
E=[0,0,P0/(2*h)];CC=[s.Rational(1,2),s.Rational(1,2),0]
for i in range(3):
 ck('independent metric Euler derivative '+str(i),Eq[i]-n*A[i]-s.diff(n,z)*B[i]-s.diff(n,z,2)*CC[i])
 ck('independent momentum Euler derivative '+str(i),Ep[i]-n*D[i]-s.diff(n,z)*E[i])
# Integrate the n''m-nm'' coefficient by parts once.
beta=s.simplify(sum(A[i]*E[i]-D[i]*B[i] for i in range(3))+s.diff(sum(CC[i]*D[i] for i in range(3)),z))
# Raw bracket versus first-derivative normal form plus an exact total derivative.
raw=sum(Eq[i]*Ep[i].subs(n,m)-Ep[i]*Eq[i].subs(n,m) for i in range(3))
L=sum(CC[i]*D[i] for i in range(3))
ck('raw Poisson bracket modulo exact boundary divergence',raw-beta*(n*s.diff(m,z)-m*s.diff(n,z))-s.diff(L*(s.diff(n,z)*m-n*s.diff(m,z)),z))
t=s.Function('t')(z);cc=s.Function('p')(z)
sector={pa:t,pb:t,pc:cc}
bs=s.factor(beta.subs(sector).doit())
Cs=cc*cc-4*t*cc+s.diff(cc,z)**2/(2*h)
ck('constraint restricted family',flatten(H).subs(sector).doit()-Cs)
ck('bracket coefficient factorization',bs-(-2*s.diff(cc,z))*(1+Cs/(4*h)))
tstar=(cc*cc+s.diff(cc,z)**2/(2*h))/(4*cc)
ck('constraint surface exact',Cs.subs(t,tstar))
ck('nonzero weak bracket on constraint surface',bs.subs(t,tstar)+2*s.diff(cc,z))
kk=s.symbols('k',nonzero=True,real=True);c0=s.symbols('p0',positive=True);NN=s.Function('N')(z)
Pexp=-2*kk*c0*s.exp(kk*z)
ck('lapse preservation exponential patch',(2*Pexp*s.diff(NN,z)+s.diff(Pexp,z)*NN)-Pexp*(2*s.diff(NN,z)+kk*NN))
ck('positive lapse patch solution',(2*s.diff(NN,z)+kk*NN).subs(NN,s.exp(-kk*z/2)).doit())
ck('flux form of consistency',NN*(2*Pexp*s.diff(NN,z)+s.diff(Pexp,z)*NN)-s.diff(NN*NN*Pexp,z))
result={'claim_id':'CLA-001','checks_passed':len(checks),'normalization':'Mp=1; constant h>0 patch; diagonal gamma=diag(a,b,c), p^{ij}=diag(pa,pb,pc); fields only z','Hamiltonian_constraint':str(H),'flat_Euler_metric':[str(q) for q in Eq],'flat_Euler_momentum':[str(q) for q in Ep],'family_constraint':str(Cs),'family_Poisson_coefficient':str(bs),'weak_coefficient':'-2*pprime=Pz','lapse_condition':'2 Pz Nprime+Pzprime N=0, equivalently (N^2 Pz)prime=0 when N>0','scope':'Exact local planar subsector at gamma=I, arbitrary z-dependent canonical momenta and compact smearings. Not full constraint algorithm, spherical gluing, physical DOF count or propulsion.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
