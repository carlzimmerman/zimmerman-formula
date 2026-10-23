"""Spherical ADM Hamiltonian and time-symmetric lapse preservation."""
import sympy as s
import sys,json
from pathlib import Path
r=s.symbols('r',positive=True)
K,eta,beta,gamma,Lam=s.symbols('K eta beta gamma Lambda',positive=True)
ell,R,P,pl,pr,J,N,M=[s.Function(t)(r) for t in ['ell','R','P','pl','pr','J','N','M']]
c=(1+beta)/(2+3*beta); delta=beta/(2+3*beta)
vol=ell*R**2; td=(ell*pl+R*pr)/2; tr=td/vol
w=s.Function('w')
d=s.diff(R**2*P/ell,r)/vol
R3=2/R**2*(1-(s.diff(R,r)/ell)**2-2*R/ell*s.diff(s.diff(R,r)/ell,r))
T=K/(ell*R**2)*(ell**2*pl**2+R**2*pr**2/2-c*(ell*pl+R*pr)**2)+ell*J**2/(2*eta*R**2)
clock=0 if '--mutate' in sys.argv else 1
U=vol*((2*Lam-R3)/(4*K)+w(P/ell)+clock*d+gamma*d*d/2)
H=T+U
qs=[ell,R,P]; ps=[pl,pr,J]
def EL(f,q):return s.diff(f,q)-s.diff(s.diff(f,s.diff(q,r)),r)+s.diff(s.diff(f,s.diff(q,r,2)),r,2)
# Derive kinetic energy by an independent Legendre transform of the radial extrinsic curvatures.
vl,vr,vp=s.symbols('vl vr vp')
Lkin=vol/(4*K)*((vl/ell)**2+2*(vr/R)**2-(1+beta)*(vl/ell+2*vr/R)**2)+eta*R**2/(2*ell)*vp**2
vel=s.solve([s.diff(Lkin,vl)-pl,s.diff(Lkin,vr)-pr,s.diff(Lkin,vp)-J],[vl,vr,vp],dict=True)[0]
Tleg=s.factor((pl*vl+pr*vr+J*vp-Lkin).subs(vel))
checks={'legendre_transform':s.simplify(Tleg-T)==0}
print('Legendre transform done',flush=True)
# Direct Euler derivative calculation of the smeared lapse bracket.
n0,n1,n2,m0,m1,m2=s.symbols('n0 n1 n2 m0 m1 m2')
ns={N:n0,s.diff(N,r):n1,s.diff(N,r,2):n2}
C1=0;C2=0
for q,p in zip(qs,ps):
 en=s.expand(EL(N*H,q).subs(ns));em=en.xreplace({n0:m0,n1:m1,n2:m2})
 b=s.expand((m0*en-n0*em)*s.diff(T,p))
 C1+=b.coeff(n1).coeff(m0);C2+=b.coeff(n2).coeff(m0)
 print('Euler',q,flush=True)
V=s.factor(-C1+s.diff(C2,r))
Hg=pr*s.diff(R,r)-ell*s.diff(pl,r)
Vexpected=Hg/ell**2+2*delta*vol/ell**2*s.diff(tr,r)+4*K*(1+gamma*d)*((1-c)*td*P/ell**2-pl*P/ell)+(1+gamma*d)*J/eta
checks['radial_lapse_bracket']=s.factor(V-Vexpected)==0
A=s.factor(Vexpected-(Hg-P*s.diff(J,r))/ell**2)
# At zero momenta A=0. Since A is linear in momenta, time derivatives of its
# configuration-dependent coefficients vanish from dot A on this slice.
pdot=[-EL(N*U,q) for q in qs]
Adot=sum(s.diff(A,p)*dp+s.diff(A,s.diff(p,r))*s.diff(dp,r) for p,dp in zip(ps,pdot))
print('A derivative constructed',flush=True)
jetN=s.symbols('n0:5')
replace={s.diff(N,r,i):jetN[i] for i in range(5)}
poly=s.Poly(s.expand(Adot.subs(replace)),*jetN)
coeff=[s.factor(poly.coeff_monomial(z)) for z in jetN]
checks['lapse_linear']=poly.total_degree()==1
checks['no_fourth_derivative_in_radial_flux']=coeff[4]==0
expected3=-delta*R**2/(K*ell**3)
checks['third_derivative_coefficient']=s.factor(coeff[3]-expected3)==0
# Flat background substitutions after variation. Use exact w derivatives at zero.
flat={ell:1,s.diff(ell,r):0,s.diff(ell,r,2):0,s.diff(ell,r,3):0,
 R:r,s.diff(R,r):1,s.diff(R,r,2):0,s.diff(R,r,3):0,
 P:0,s.diff(P,r):0,s.diff(P,r,2):0,s.diff(P,r,3):0,Lam:0}
Af=s.simplify(Adot.subs(flat).doit())
Af=Af.subs(w(0),0)
# At P=0 first derivative of w must vanish; higher derivatives multiply zero P jets here.
z=s.symbols('z')
Af=Af.replace(lambda v:isinstance(v,s.Subs) and v.expr.is_Derivative and v.point==(0,),lambda v:0 if v.expr.derivative_count==1 else v)
Af=s.simplify(Af)
expect_flat=r*r/eta*s.diff(N,r)-delta*r*r/K*s.diff(s.diff(N,r,2)+2*s.diff(N,r)/r,r)
checks['flat_lapse_operator']=s.simplify(Af-expect_flat)==0
result={'checks':checks,'all_pass':all(checks.values()),'radial_A':str(A),'third_derivative_coefficient':str(coeff[3]),'flat_Adot':str(Af),'flat_expected':str(expect_flat),'lapse_coefficients':{str(i):str(co) for i,co in enumerate(coeff)},'scope':'exact radial canonical sector; time-symmetric preservation; flat limit after variation; no actual galaxy solved'}
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
for name,ok in checks.items():print(name,'PASS' if ok else 'FAIL',flush=True)
print('COMPLETE',sum(checks.values()),'/',len(checks))
sys.exit(0 if all(checks.values()) else 1)
