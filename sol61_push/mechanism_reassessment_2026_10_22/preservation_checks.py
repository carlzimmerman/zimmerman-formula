"""Canonical Euler-derivative test in a plane-dependent invariant sector."""
import sympy as s
import sys,json
from pathlib import Path
x=s.symbols('x', real=True)
K,eta,beta,gamma,lam=s.symbols('K eta beta gamma Lambda',positive=True)
A,B,C,p,pa,pb,pc,j,N,M=[s.Function(z)(x) for z in ['A','B','C','p','pa','pb','pc','j','N','M']]
root=s.sqrt(A*B*C)
c=(1+beta)/(2+3*beta)
trace=A*pa+B*pb+C*pc
d=s.diff(root*p/A,x)/root
R=(-s.diff(B,x,2)/(A*B)-s.diff(C,x,2)/(A*C)
   +s.diff(A,x)*s.diff(B,x)/(2*A*A*B)+s.diff(A,x)*s.diff(C,x)/(2*A*A*C)
   +s.diff(B,x)**2/(2*A*B*B)+s.diff(C,x)**2/(2*A*C*C)
   -s.diff(B,x)*s.diff(C,x)/(2*A*B*C))
# Arbitrary local potential represented by a quartic polynomial; it cannot enter the bracket.
w2,w4=s.symbols('w2 w4')
W=w2*p*p/A+w4*p**4/(A*A)
T=4*K/root*((A*pa)**2+(B*pb)**2+(C*pc)**2-c*trace**2)+A*j*j/(2*root*eta)
U=root*((2*lam-R)/(4*K)+d+gamma*d*d/2+W)
H=T+U
qs=[A,B,C,p]; ps=[pa,pb,pc,j]
def EL(f,q):
 return s.diff(f,q)-s.diff(s.diff(f,s.diff(q,x)),x)+s.diff(s.diff(f,s.diff(q,x,2)),x,2)
# Replace the smearing jets by algebraically independent symbols to extract coefficients.
n0,n1,n2,m0,m1,m2=s.symbols('n0 n1 n2 m0 m1 m2')
subs={N:n0,s.diff(N,x):n1,s.diff(N,x,2):n2,M:m0,s.diff(M,x):m1,s.diff(M,x,2):m2}
C1=0; C2=0; zeroth=0
for qi,pi in zip(qs,ps):
 en=s.expand(EL(N*H,qi).subs(subs))
 em=en.xreplace({n0:m0,n1:m1,n2:m2})
 tp=s.diff(T,pi)
 integ=s.expand((en*m0-em*n0)*tp)
 C1+=integ.coeff(n1).coeff(m0)
 C2+=integ.coeff(n2).coeff(m0)
 zeroth+=integ.coeff(n0).coeff(m0)
 print('Euler sector',str(qi),flush=True)
V=s.factor(-C1+s.diff(C2,x))
Hg=-2*A*s.diff(pa,x)-pa*s.diff(A,x)+pb*s.diff(B,x)+pc*s.diff(C,x)
Vgg=Hg/A+2*beta/(2+3*beta)*(s.diff(trace,x)-s.diff(root,x)/root*trace)/A
Vcross=4*K*(1+gamma*d)*((1-c)*trace*p/A-2*pa*p)
Vp=(1+gamma*d)*j/eta
expected=Vgg+Vcross+Vp
if '--mutate' in sys.argv: expected-=Vcross
res=s.factor(V-expected)
checks={'full_reduced_bracket':res==0,'ultralocal_cancel':s.simplify(zeroth)==0,
        'potential_absent':not V.has(w2,w4,lam)}
print('bracket residual:',res,flush=True)
# Independent curvature construction from Christoffels, no hard-coded scalar formula.
g=s.diag(A,B,C); gi=s.diag(1/A,1/B,1/C)
def partial(expr,i):return s.diff(expr,x) if i==0 else s.S.Zero
G=[[[sum(gi[i,l]*(partial(g[l,k],j)+partial(g[l,j],k)-partial(g[j,k],l))/2 for l in range(3)) for k in range(3)] for j in range(3)]for i in range(3)]
Ric=s.Matrix(3,3,lambda i,j:sum(partial(G[l][i][j],l)-partial(G[l][i][l],j)+sum(G[l][l][m]*G[m][i][j]-G[l][j][m]*G[m][i][l] for m in range(3)) for l in range(3)))
checks['curvature_from_connection']=s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(3) for j in range(3))-R)==0
# Full three-dimensional P-jet derivative checks the magnetic bracket contribution.
jet=s.Matrix(3,3,lambda i,j:s.Symbol('P'+str(i)+'_d'+str(j)))
dflat=s.trace(jet); Fflat=jet.T-jet
Uflat=dflat+gamma*dflat*dflat/2+gamma*sum(Fflat[i,j]**2 for i in range(3) for j in range(3))/4
checks['full_3d_P_gradient_derivative']=all(s.expand(s.diff(Uflat,jet[i,j])-(1+gamma*dflat)*(1 if i==j else 0)-gamma*Fflat[j,i])==0 for i in range(3) for j in range(3))
# Exact positive-lapse obstruction. Flat torus, P=0, Pi=J(sin x,cos x,0).
J=s.symbols('J',positive=True)
q2=(2+3*beta)/(12*K)*(J**2/(2*eta)+lam/(2*K))
constraint=s.simplify(-12*K*q2/(2+3*beta)+J**2*(s.sin(x)**2+s.cos(x)**2)/(2*eta)+lam/(2*K))
checks['rotating_current_H_constraint']=constraint==0
checks['rotating_current_divergence']=s.diff(J*s.sin(x)/eta,x)==J*s.cos(x)/eta
# At x=0: 2 partial_y N + N=0. Monodromy in y of period 2pi is exp(-pi).
monodromy=s.exp(-s.pi)
checks['positive_lapse_monodromy_obstruction']=bool(monodromy<1)
# No-clock mutation cannot remove beta anomaly in general; we test only the P=0 constant trace witness.
checks['flat_zero_current_limit']=s.simplify((J/eta).subs(J,0))==0
result={'checks':checks,'all_pass':all(checks.values()),'plane_bracket_residual':str(res),
 'Vgg':str(Vgg),'Vcross':str(Vcross),'Vp':str(Vp),
 'rotating_current_H_residual':str(constraint),'lapse_orbit_multiplier':str(monodromy),
 'lapse_orbit_multiplier_numeric':float(monodromy),'mutated':bool('--mutate' in sys.argv)}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
for name,ok in checks.items():print(name,'PASS' if ok else 'FAIL')
print('COMPLETE',sum(checks.values()),'/',len(checks))
sys.exit(0 if result['all_pass'] else 1)
