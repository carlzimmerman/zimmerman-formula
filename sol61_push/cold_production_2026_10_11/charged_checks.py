"""Algebra and linear instability checks for a distinct charge-protected action."""
import json,math,itertools
from pathlib import Path
import numpy as np
p=Path(__file__).parent
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
m=1.;u=.001;Delta=4*m*m*u*u;M=math.sqrt(4*m*m+Delta)
g=.01
# Deterministic complex samples, not trajectory solutions.
for j,(phi,chi,dp,dc) in enumerate(itertools.product([0j,.2+.3j,-.7+.1j],repeat=4)):
    U=abs(math.sqrt(Delta)*chi+g/math.sqrt(Delta)*phi**2)**2
    V=m*m*abs(phi)**2+4*m*m*abs(chi)**2+U
    Q=(1j*(phi.conjugate()*dp-dp.conjugate()*phi)+2j*(chi.conjugate()*dc-dc.conjugate()*chi)).real
    E=abs(dp)**2+abs(dc)**2+V
    sq=abs(dp+1j*m*phi)**2+abs(dc+2j*m*chi)**2+U
    check('energy-charge identity '+str(j),abs((E-m*Q)-sq)<1e-10*(1+E))
    theta=.713
    V2=m*m*abs(phi)**2+4*m*m*abs(chi)**2+abs(math.sqrt(Delta)*chi*np.exp(2j*theta)+g/math.sqrt(Delta)*(phi*np.exp(1j*theta))**2)**2
    check('charge symmetry '+str(j),abs(V2-V)<1e-10*(1+V))
    cubic=2*g*(chi.conjugate()*phi**2).real
    B=g*g/Delta*abs(phi)**4
    z=math.sqrt(Delta)*chi;w=g/math.sqrt(Delta)*phi**2
    check('virial remainder '+str(j),abs(.5*cubic+B-(w.conjugate()*(z+w)).real)<1e-10*(1+V))
eps=1e-7;c=2*eps*m*m
rows=[]
for offset in [-1.5,-.5,0,.5,1.5]:
    D=offset*c;p2=m*m*u*u+D
    mat=np.array([[0,0,1,0],[0,0,0,1],[-D-c,0,0,-M],[0,-D+c,M,0]],dtype=float)
    eig=np.linalg.eigvals(mat);growth=float(max(eig.real))
    den=D+M*M/2+math.sqrt(M**4/4+M*M*D+c*c)
    s2=(c*c-D*D)/den
    expected=math.sqrt(max(0,s2))
    check('linear rate '+str(offset),abs(growth-expected)<1e-10)
    rows.append(dict(offset=offset,p2_over_m2=p2,growth_per_mt=growth,analytic_growth=expected))
r=math.sqrt(1+u*u);eta=u*u/(r*(r+1))
coarse=2*eta/3+math.sqrt(2*eta*(eta+u*u))
out=dict(checks=checks,all_pass=all(c['passed'] for c in checks),linear_rows=rows,
 eta=eta,instantaneous_pressure_bound=eta+2*math.sqrt(eta),time_averaged_pressure_bulk_bound=coarse,
 averaging_endpoint_term_at_mT_1e6=2*math.sqrt(eta)/1e6,
 non_claims=['Distinct two-complex-field action','Classical fixed Minkowski volume for energy and pressure proof','No nonlinear quantum production yield or abundance'])
(p/'charged_checks_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass'])
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));assert out['all_pass']
