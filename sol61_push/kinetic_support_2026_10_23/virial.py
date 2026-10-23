import json,sys,numpy as np
from scipy.integrate import simpson
from pathlib import Path
b=Path(__file__).parent;cases=json.loads((b/'family/result.json').read_text());rows=[]
for c in cases:
 r=np.array(c['r']);rho=np.array(c['rho']);phi,g,h,P,chi,z=np.array(c['fields']);integ=lambda f:float(simpson(f*r*r,x=r));p=abs(P)
 T=1.5*c['K']*integ(rho**(5/3));U=.5*integ(rho*phi);V=.5*integ(chi*h*h);Z=.005/2*integ((chi-1)**2);J=.125/2*integ(z*z);H=integ(h*h);B=integ(-p-np.log1p(-p));D=integ(p*p/(1-p));E=T+U+V+Z+J+B
 vir=2*T+U+3*V-3*Z-J+2*D-3*B;phase=V-2*J-2*Z-H/2;left=c['mu']*c['M']-E;right=-4*T/3-4*J-2*Z-H+2*B-D;jeans=2*T-integ(rho*r*(g-P/(1-p)))
 rows.append(dict(M=c['M'],K=c['K'],energy=E,energy_per_mass=E/c['M'],muM_minus_E=left,identity_rhs=right,identity_relative_error=abs(left-right)/max(abs(left),1e-20),virial_relative=abs(vir)/abs(U),phase_relative=abs(phase)/max(V,1e-20),jeans_relative=abs(jeans)/(2*T),T=T,U=U,V=V,Z=Z,J=J,H=H,B=B,D=D))
json.dump(rows,open(sys.argv[1],'w'),indent=2);print('max errors',max(x['identity_relative_error'] for x in rows),max(x['virial_relative'] for x in rows),max(x['jeans_relative'] for x in rows));print('all negative',all(x['muM_minus_E']<0 for x in rows))
