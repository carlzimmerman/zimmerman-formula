"""Frozen route 3: pressure projector and independent response coefficient."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
d,k,rho,L,P,eta,astar,al=s.symbols('d k rho Lambda pressure eta a_star a_Lambda',positive=True)
checks=[]
def ck(name,expr):
 r=s.simplify(expr);checks.append({'name':name,'residual':str(r),'passed':r==0})
# Einstein equation includes vacuum on its source side, signature (-,+,...,+).
R=2*(k*rho+d*L)/(d-2)
Ruu=k*rho-L-R/2
ck('dust_vacuum_pressure_projector',(R/2-Ruu)/(d-1)-L)
# Add isotropic matter pressure to the same dust+vacuum source.
Rp=2*(k*(rho-(d-1)*P)+d*L)/(d-2)
Ruup=k*rho-L-Rp/2
ck('pressure_projector_contamination',(Rp/2-Ruup)/(d-1)-(L-k*P))
# Fixed baryon source normalization; a_star is the operational deep-MOND scale.
y=s.symbols('y',positive=True)
F=2*y**s.Rational(3,2)/(3*astar)+2*eta*y**s.Rational(3,2)/(3*al)
aeff=1/(1/astar+eta/al)
ck('constitutive_response',s.diff(F,y)-s.sqrt(y)/aeff)
ck('response_sensitivity',s.diff(aeff,eta)+aeff**2/al)
# Small-field response term has zero background value and first and second derivatives.
b=s.symbols('b',nonnegative=True)
for order in range(3):
 ck('zero_background_jet_'+str(order),s.diff(b**3,b,order).subs(b,0))
result={'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'scope':'Einstein dust/vacuum projector; conditional preferred-clock static EFT, not its full stability or radiative protection'}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
