"""Independent forcing identities and saved field/tracer bookkeeping."""
import json,math
from pathlib import Path

b=Path(__file__).parent
def scale(t,start=5.,outward=1.):
    if t<=start or t>=start+30:return 1.
    u=(t-start)%10
    if u<outward:return 1+2*(1-math.cos(math.pi*u/outward))
    return 1+2*(1+math.cos(math.pi*(u-outward)/(10-outward)))
def potential(r,a):return -.02/math.sqrt(r*r+1)-.2/math.sqrt(r*r+a*a)
checks={}
for name,start,outward in [('early',5,1),('late',25,1),('slow',5,5)]:
    values=[scale(n*.06,start,outward) for n in range(1001)]
    checks[name+'_closed_geometry']=values[0]==values[-1]==1 and min(values)>=1 and max(values)<=5
    # A fixed test density at three radii receives zero work over a closed cycle.
    work=0.
    for r,weight in [(0.,.2),(1.,.3),(5.,.5)]:
        work+=weight*sum(potential(r,values[n+1])-potential(r,values[n]) for n in range(1000))
    checks[name+'_fixed_density_zero_cycle_work']=abs(work)<1e-12
for r in [.1,1.,4.]:
    h=1e-5
    deriv=(potential(r+h,2)-potential(r-h,2))/(2*h)
    gn=.02*r/(r*r+1)**1.5+.2*r/(r*r+4)**1.5
    checks['force_gradient_'+str(r)]=abs(deriv-gn)<1e-9
for p in (b/'runs').glob('*.json'):
    d=json.loads(p.read_text())
    if 'parameters' not in d:continue
    t=p.stem;i,f=d['initial'],d['final']
    checks[t+'_counted_work']=abs((f['E']+f['removed']['E']-i['E']-d['external_work'])/abs(i['E'])-d['E_residual'])<1e-10
    checks[t+'_cold_inventory']=abs(f['M']+f['removed']['M']-i['M'])<1e-8
    checks[t+'_declared_baryon_masses']=d['parameters']['stellar_source_mass']==.02 and d['parameters']['gas_mass']==.2
    # Final source geometry returns to one in every case; none creates gas mass.
    checks[t+'_gas_geometry_returned']=f['gas_scale']==1.
assert all(checks.values()),checks
(b/'verification.json').write_text(json.dumps({'checks':checks,'scope':'forcing derivatives, closed-cycle control and saved ledgers; no full PDE or observational validation'},indent=2)+'\n')
print(len(checks),'checks passed')
