"""Finite checks and evaluation of a conditional all-momentum pressure bound."""
import json,math
from pathlib import Path
p=Path(__file__).parent
u=.001;r=math.sqrt(1+u*u);M=2*r;m=1.
# Rationalized excess fraction avoids cancellation at threshold.
eta=u*u/(r*(r+1));checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
# Each entry constructs a mixture with exactly N_y+2N_h=2 and E=M.
# The allocated kinetic energy is split across species, without any momentum cutoff.
rows=[]
for daughter_fraction in [.01,.1,.5,.9,1.]:
    Ny=2*daughter_fraction;Nh=1-daughter_fraction
    budget=(M-2)*daughter_fraction
    for allocation in [0.,.1,.5,.9,1.]:
        if Nh==0 and allocation!=1:continue
        Ty=budget*allocation;Th=budget*(1-allocation)
        ey=m+Ty/Ny;eh=M+Th/Nh if Nh else M
        py2=(ey-m)*(ey+m);ph2=(eh-M)*(eh+M)
        E=Ny*ey+Nh*eh
        PV=(Ny*py2/ey+Nh*ph2/eh)/3
        bound=2*(E-2*m)/3
        check('energy '+str((daughter_fraction,allocation)),abs(E-M)<1e-14)
        check('pressure '+str((daughter_fraction,allocation)),0<=PV<=bound+1e-14)
        rows.append(dict(daughter_fraction=daughter_fraction,kinetic_allocation_to_daughters=allocation,w=PV/E))
# Relativistic single-particle inequality: p^2/E <= 2(E-mass).
for mass in [1.,M]:
 for ratio in [.001,.1,1.,10.,1e4]:
    energy=mass*math.sqrt(1+ratio*ratio)
    kinetic=mass*ratio*ratio/(math.sqrt(1+ratio*ratio)+1)
    check('relativistic inequality '+str((mass,ratio)),(mass*ratio)**2/energy<=2*kinetic*(1+1e-14))
out=dict(eta=eta,w_bound=2*eta/3,energy_fraction_bound_p_over_mass_at_least_one=eta/(1-1/math.sqrt(2)),rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Requires number-weighted invariant and on-shell kinetic stress','No coherent interaction energy bound','Not a theorem for the original real-field action'])
(p/'pressure_bound_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','checks']},indent=2));print('Checks:',len(checks));assert out['all_pass']
