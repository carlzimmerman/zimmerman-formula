"""Finite one-loop soft-Higgs daughter form factor at fixed tree inputs.

Not the hard on-shell Higgs decay amplitude. No finite matching counterterm
or all-orders prediction is silently fixed by this one-loop calculation.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent
parent=json.loads((base/'thermal_charge_run_002/results.json').read_text())
p=next(r['parameters'] for r in parent['phase_rows'] if r['parameters']['m']==.002)
m,M,g,lp=p['m'],p['M'],p['g'],p['lp']
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
z,w=roots_legendre(128);x=(z+1)/2;w=w/2
rows=[]
for ratio in (2.,M/m,2.1,3.,5.,10.):
    r=ratio**2
    # Feynman x is the source-propagator fraction; external p^2=m^2.
    f=lambda y:y/(r*y+(1-y)**2)
    integral=quad(f,0,1,epsabs=1e-14,epsrel=1e-12)[0]
    gauss=float(w@(x/(r*x+(1-x)**2)))
    check('independent quadrature '+str(ratio),abs(integral/gauss-1)<2e-12)
    def mass_correction_scaled(rr):
        # Sigma/g^2 = (4/16pi^2) integral log(D/m^2), up to constant.
        return float(w@np.log(rr*x+(1-x)**2))/(4*math.pi**2)
    step=r*1e-4
    finite=(mass_correction_scaled(r+step)-mass_correction_scaled(r-step))/(2*step)
    derivative=integral/(4*math.pi**2)
    check('soft insertion vs mass derivative '+str(ratio),abs(finite/derivative-1)<2e-8)
    check('positive soft form factor '+str(ratio),integral>0)
    if ratio==2.:check('exact threshold limit',abs(integral/(math.log(2)-.5)-1)<2e-13)
    rows.append(dict(source_mass_over_m=ratio,dimensionless_integral=integral,
        soft_form_factor_over_lp=g*g/(4*math.pi**2*m*m)*integral))
selected=next(r for r in rows if r['source_mass_over_m']==M/m)
coefficient=lp*selected['soft_form_factor_over_lp']
rho=json.loads((base/'portal_response_run_001/results.json').read_text())['baryon_response'][1]['density_GeV4']
shift=-coefficient*.308*rho/125**2
result=dict(parameters=p,rows=rows,soft_higgs_daughter_coefficient=coefficient,
    baryon_density_GeV4=rho,delta_daughter_mass_squared_GeV2=shift,
    fractional_daughter_mass_squared_shift=shift/(m*m),
    conventions='L includes -v h Csoft |Phi|^2; tree lambda_HPhi=0; soft Higgs q=0; daughter on-shell p^2=m^2; other parameters fixed; leading order lambda_HX*g^2',
    checks=checks,non_claims=['No hard Higgs decay or freeze-in correction calculated','No physical total independent of an allowed finite tree matching term','No full renormalization, gravity, response phase, vacuum magnitude or novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
