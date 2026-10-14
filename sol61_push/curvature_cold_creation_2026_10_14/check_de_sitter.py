"""Exact homogeneous de Sitter test for the stated action, including metric response."""
import json,sys,math
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def eq(n,x):ck(n,s.simplify(x)==0)
a,ad,add,N,Nd,phi,v,acc,MP,eta,mm,ll,H,Hd=s.symbols('a a_dot a_ddot lapse lapse_dot phi phi_dot phi_ddot M_P eta mass_squared lambda H H_dot',positive=True)
U=mm*phi**2/2+ll*phi**4/4;F=eta*phi**2/2;Fp=s.diff(F,phi)
# Derive the equations from the lapse-dependent homogeneous action, not a copied stress tensor.
# N a^3 GB = 8 d/dt(a_dot^3/N^3), so +F GB -> -8 F_dot a_dot^3/N^3.
GB=24*(ad**2*add/(a**3*N**4)-ad**3*Nd/(a**3*N**5))
eq('GB total derivative primitive',N*a**3*GB-8*(3*ad**2*add/N**3-3*ad**3*Nd/N**4))
L=-3*MP**2*a*ad**2/N+a**3*v**2/(2*N)-N*a**3*U-8*Fp*v*ad**3/N**3
constraint=s.diff(L,N).subs({N:1,ad:a*H})/a**3
fried=3*MP**2*H**2-v**2/2-U+24*Fp*v*H**3
eq('Friedmann from lapse variation',constraint-fried)
dLdv=s.diff(L,v)
totaldt=s.diff(dLdv,a)*ad+s.diff(dLdv,ad)*add+s.diff(dLdv,N)*Nd+s.diff(dLdv,phi)*v+s.diff(dLdv,v)*acc
scalar=((totaldt-s.diff(L,phi))/a**3).subs({N:1,Nd:0,ad:a*H,add:a*(H**2+Hd)})
expected=acc+3*H*v+s.diff(U,phi)-24*Fp*H**2*(H**2+Hd)
eq('scalar equation from action',scalar-expected)
# Linearize around constant phi, H. Friedmann gives dH=A dphi+B dphi_dot.
A=4*Fp*H**3/MP**2;B=-4*Fp*H**2/MP**2
Z=1-24*Fp*H**2*B
fric=3*H-Fp*(96*H**3*B+24*H**2*A)
C=s.diff(U,phi,2)-24*s.diff(F,phi,2)*H**4-96*Fp*H**3*A
eq('positive homogeneous kinetic coefficient',Z-(1+96*Fp**2*H**4/MP**2))
eq('homogeneous friction exactly 3HZ',fric-3*H*Z)
H2=U/(3*MP**2);eta_ds=(mm+ll*phi**2)/(24*H2**2)
Cds=s.factor(C.subs(H**6,H2**3).subs(H**4,H2**2).subs(eta,eta_ds))
Cclosed=-(8*mm**2+12*mm*ll*phi**2+6*ll**2*phi**4)/(2*mm+ll*phi**2)
eq('negative homogeneous restoring coefficient',Cds-Cclosed)
Zds=s.factor(Z.subs(H**4,H2**2).subs(eta,eta_ds))
eq('eliminated homogeneous kinetic coefficient',Zds-(1+24*MP**2*(mm+ll*phi**2)**2/(phi**2*(2*mm+ll*phi**2)**2)))
eq('curvature and field control relation',eta_ds*H2-MP**2*(mm+ll*phi**2)/(2*phi**2*(2*mm+ll*phi**2)))
# Independently linearize the original first-order homogeneous equations with exponential perturbations.
z,ds=s.symbols('growth perturbation')
base_scalar=expected
original_pert=base_scalar.subs({phi:phi+ds,v:z*ds,acc:z*z*ds,H:H+(A+B*z)*ds,Hd:z*(A+B*z)*ds})
linear=s.diff(original_pert,ds).subs(ds,0)
eq('independent linearization characteristic',linear-(Z*z*z+fric*z+C))
rows=[]
for m2 in [0.,.01,1.]:
 for lam in [0.,.1,1.]:
  if m2==lam==0:continue
  for ph in [.01,.1,1.,10.]:
   uu=.5*m2*ph*ph+.25*lam*ph**4;h2=uu/3;ee=(m2+lam*ph*ph)/(24*h2*h2)
   zz=1+96*ee*ee*ph*ph*h2*h2
   cc=2*lam*ph*ph-384*ee*ee*ph*ph*h2**3
   ck('de Sitter background scalar constraint',abs((m2+lam*ph*ph)/(24*ee*h2*h2)-1)<1e-12)
   ck('de Sitter homogeneous instability',cc<0 and zz>0)
   growth=(-3+math.sqrt(9-4*cc/(zz*h2)))/2
   ck('positive physical homogeneous growth',growth>0)
   rows.append({'mass_squared':m2,'lambda':lam,'phi_over_MP':ph,'eta_MP_squared':ee,'H_squared_over_MP_squared':h2,'Z':zz,'C_over_ZH_squared':cc/(zz*h2),'growth_over_H':growth})
result={'passed':len(checks),'checks':checks,'rows':rows,'theorem':'Every constant nonzero-scalar, expanding flat de Sitter solution of the canonical quadratic+quartic potential with positive quadratic Gauss-Bonnet coupling, no independent cosmological constant and no other asymptotic source, has a growing homogeneous scalar-metric mode. m_squared>=0, lambda>=0, not both zero.','exact_C':'-(8 m_squared^2+12 m_squared lambda phi^2+6 lambda^2 phi^4)/(2 m_squared+lambda phi^2)','scope':'Homogeneous instability is sufficient to reject an attractor for this action. It does not exclude other potentials, couplings, additional vacuum terms, time-dependent acceleration, or modified matter sectors.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
