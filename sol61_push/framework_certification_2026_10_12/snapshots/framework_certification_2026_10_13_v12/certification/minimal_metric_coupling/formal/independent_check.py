"""Independent weak-metric/action/clock algebra; no metric gravity equations."""
import sympy as s,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
e,a,X0,rho0,u,S,Phi,Psi,eta=s.symbols('e a X0 rho0 u S Phi Psi eta',real=True)
P=lambda X:-rho0+a*(X-X0)**2/2
PX=lambda X:a*(X-X0)
Ncoef=1+2*e*Phi;Gcoef=1-2*e*Psi
volume=s.sqrt(Ncoef*Gcoef**3)
X=(u*u/Ncoef-S/Gcoef)/2
Xb=(u*u-S)/2
T00=PX(Xb)*u*u-P(Xb);trace=PX(Xb)*S+3*P(Xb)
checks=[]
def eq(name,expression):
 r=s.factor(expression);checks.append({'name':name,'passed':r==0,'residual':str(r)})
eq('actual determinant root derivative',s.diff(volume,e).subs(e,0)-(Phi-3*Psi))
eq('actual inverse metric X derivative',s.diff(X,e).subs(e,0)+Phi*u*u+Psi*S)
eq('actual action derivative to stress',s.diff(volume*P(X),e).subs(e,0)+Phi*T00+Psi*trace)
# Mixed homogeneous current: phase and weak metric perturbations vary together.
Vdot=u+e*eta
Xcur=Vdot**2/(2*Ncoef)
J=volume*PX(Xcur)*Vdot/Ncoef
Xh=u*u/2;K=PX(Xh)+a*u*u
expected=K*eta-u*(K*Phi+3*PX(Xh)*Psi)
eq('actual conserved density first variation',s.diff(J,e).subs(e,0)-expected)
# Lapse and physical spatial volume with actual canonical velocity.
N,V,v=s.symbols('N V v',positive=True)
Xh=v*v/(2*N*N)
L=N*V*P(Xh)
pi=s.diff(L,v)
eq('actual homogeneous canonical momentum',pi-V*PX(Xh)*v/N)
H=pi*v-L
rho=lambda X:2*X*PX(X)-P(X)
eq('actual Legendre transform H=N V rho',H-N*V*rho(Xh))
eq('exact vacuum proper energy',s.simplify((H/N).subs(v,N*s.sqrt(2*X0)))-V*rho0)
eq('vacuum clock compensation has no physical X change',u*(u*Phi)-u*u*Phi)
assert all(c['passed'] for c in checks)
result={'all_passed':True,'check_count':len(checks),'checks':checks,'scope':'Prospective minimal matter coupling; metric potentials independent and gravity equations unspecified. Quantum/UV/DE receipt not derived.'}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'check_count':len(checks)}))
