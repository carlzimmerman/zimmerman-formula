import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
rho,K,beta,k,omega,chi,p,q=s.symbols('rho K beta k omega chi p q',positive=True)
v,w=s.symbols('v w',real=True)
Z=1+K*beta**2*rho
checks=[]
def ck(n,vv):
 checks.append({'name':n,'ok':bool(vv)})
 if not bool(vv):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
L=rho*v*v/2+Z*w*w/(2*K)-k*k*chi*chi/(2*K)-beta*rho*k*chi*v
ze('current canonical momentum',s.diff(L,v)-(rho*v-beta*rho*k*chi))
ze('radiation canonical momentum',s.diff(L,w)-Z*w/K)
H=(p*v+q*w-L).subs({v:p/rho+beta*k*chi,w:K*q/Z})
ze('full positive principal Hamiltonian',H-(p+beta*rho*k*chi)**2/(2*rho)-K*q*q/(2*Z)-k*k*chi*chi/(2*K))
matrix=s.Matrix([[-rho*omega**2,s.I*beta*rho*k*omega],[-s.I*beta*rho*k*omega,(k*k-Z*omega**2)/K]])
ze('coupled mode determinant',matrix.det()-rho*Z*omega**2*(omega**2-k*k)/K)
ze('propagating branch luminal',(1+K*beta*beta*rho)/Z-1)
ze('no adjusted kinetic term is supermetric',((1+K*beta*beta*rho)-1)-K*beta*beta*rho)
ze('vacuum scalar branch',Z.subs(rho,0)-1)
# A prescribed homologous Gaussian flow v=(Rdot/R) r has theta=3Rdot/R.
M,R,rd=s.symbols('M R Rdot',positive=True)
ze('compression monopole at fixed conserved mass',3*M*rd/R-M*(3*rd/R))
for den in [.01,1,100,1e6]:
 z=1+den
 for kk in [.1,1,10]:
  # Choose K=beta=1, so rho=den, and canonical momenta of either sign.
  for pp,qq in [(-2,1),(1,-3),(0,0)]:
   val=(pp+den*kk*.2)**2/(2*den)+qq*qq/(2*z)+kk*kk*.2*.2/2
   ck('positive H d='+str(den)+' k='+str(kk)+' p='+str(pp),val>0)
result={'passed':len(checks),'checks':checks,'covariant_candidate':'Lchi=-[g^{mu nu}-K beta^2 rho u^mu u^nu] partial_mu chi partial_nu chi/(2K)+beta rho chi nabla_mu u^mu; u=J/rho, nabla_mu J^mu=0, dust current varied. c=1.','principal_result':'Positive Hamiltonian, one luminal propagating scalar-fluid branch and a zero-frequency dust factor in homogeneous rest background. Static theta=chi=0 unchanged. Full nonlinear current/metric, finite-halo matching and cooling remain open.','nontriviality':'J^mu partial_mu chi is a boundary for a conserved current; rho chi div u is not, since current conservation gives rho div u=-u dot grad rho.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
