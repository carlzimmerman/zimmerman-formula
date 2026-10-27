"""Local regulated-band tail probe on a prescribed finite-count host.

High-gap rows extrapolate the regulated toy, not the controlled nodal EFT.
The profile is diagnostic input, not a solved hydrostatic/formation state.
"""
import json
import math
import sys
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import brentq

out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
parent=json.loads((base/'one_scale_nodal_flux_run_002/results.json').read_text())
Astar=parent['constants']['Astar'];ch=parent['constants']['ch'];cL=parent['constants']['cLambda']
mp.mp.dps=60;checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
models={'flux_spectrum':(0.,0.,0.),'material_spectrum':(1/3,1/3,-1/3),
        'compensated_cubic':(1/3,1/3,-1/9)}
runs=[]
for name,(aexp,lexp,hexp) in models.items():
    rows=[]
    for radius in np.geomspace(1.,1e8,161):
        y=(1+radius*radius)**-2 # finite-count r^-4 tail, Q=1
        A=Astar*y**aexp;cutoff=cL*y**lexp;h=ch*y**hexp
        D=radius/(1+radius*radius)**1.5
        def derivative(logp):
            gap=h*math.exp(logp)
            return 2*A*h*cutoff*gap*gap/(gap+cutoff+math.sqrt(gap*gap+cutoff*cutoff))
        guess=max(math.sqrt(D/(A*h**3)),D/(A*cutoff*h*h))
        low=math.log(guess)-10;high=math.log(guess)+10
        logp=brentq(lambda lp:math.log(derivative(lp)/D),low,high,xtol=1e-12,rtol=1e-14)
        p=math.exp(logp);gap=h*p
        check('regulated algebraic force '+str((name,float(radius))),abs(derivative(logp)/D-1)<1e-9)
        aa,dd,ll=map(lambda x:mp.mpf(str(x)),(A,gap,cutoff))
        energy=-aa*((ll*ll+dd*dd)**mp.mpf('1.5')-ll**3-dd**3)/3+aa*ll*dd*dd/2
        shell=4*math.pi*radius**3*float(energy)
        check('positive local excess energy '+str((name,float(radius))),shell>0)
        rows.append(dict(r=float(radius),host_y=y,p=p,gap_over_cutoff=gap/cutoff,
            local_excess_energy=float(energy),excess_energy_per_log_radius=shell,
            controlled_small_gap_below_0p1=bool(gap/cutoff<.1)))
    radii=np.log([r['r'] for r in rows[-20:]])
    slope=float(np.polyfit(radii,np.log([r['p'] for r in rows[-20:]]),1)[0])
    energy_slope=float(np.polyfit(radii,np.log([r['excess_energy_per_log_radius'] for r in rows[-20:]]),1)[0])
    expected={'flux_spectrum':(-1.,0.),'material_spectrum':(-2.,-1.),'compensated_cubic':(-2/9,7/9)}[name]
    check('tail force exponent '+name,abs(slope-expected[0])<.01)
    check('tail shell-energy exponent '+name,abs(energy_slope-expected[1])<.01)
    runs.append(dict(model=name,p_log_slope=slope,shell_energy_log_slope=energy_slope,
        expected_regulated_toy_slopes=expected,controlled_tail_at_last_sample=rows[-1]['controlled_small_gap_below_0p1'],rows=rows))
result=dict(host_profile='y=(1+r^2)^-2, finite material count pi^2 in unit normalization; sourceD=r/(1+r^2)^1.5; prescribed profile, not solved hydrostatic equilibrium',
    force_equation='D=dV_Fren/dp, exact local finite-tube determinant; C=Q=1',checks=checks,runs=runs,
    non_claims=['High-gap tail continuation is only the specified regulated toy, not controlled low-gap microscopic EFT','No spatial band gradients, live host stress/equilibrium, physical boundary, gravity/lensing or cosmology','Finite label count does not establish finite cold-mass supply or a galaxy prediction'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),summaries=[{k:v for k,v in r.items() if k!='rows'} for r in runs]),indent=2))
