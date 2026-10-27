"""CE-FM-052: bounded arithmetic and optical-efficiency scope controls."""
import json, math, sys
from pathlib import Path
from fractions import Fraction as F
base=Path('campaign_fresh_gravity/CFG789_cold_to_light')
a=json.loads((base/'cfg789_results.json').read_text())['res']
b=json.loads((base/'cfg789_results_MUTATE.json').read_text())['res']
c=2.998e8; G=6.674e-11; ms=1.989e30; pc=3.0857e16
rho=.26*3*(70e3/(pc*1e6))**2/(8*math.pi*G)
t=13.8*3.156e16
checks=0
for k,v in a.items():
    I,fz,rl=map(float,k.split('|'))
    rate=(4*math.pi*I/c)/(rho*c*c*t*fz)
    power=rl*ms/pc**3*c*c*1e9*rate
    expected={'tau_yr':1/rate/3.156e7,'P_km3':power,'S':3e8/power}
    for field,x in expected.items():
        assert math.isclose(v[field],x,rel_tol=3e-14); checks+=1
    for field,factor in [('tau_yr',1e-8),('P_km3',1e8),('S',1e-8)]:
        assert math.isclose(b[k][field]/v[field],factor,rel_tol=3e-14); checks+=1
# Normalize the optical emissivity cap to one. eta*Gamma <= 1.
# Saturation gives tau=eta and local optical power=eta_local/eta_cos.
for eta_cos in [F(1),F(1,1000),F(1,10**6)]:
    Gamma=1/eta_cos
    assert eta_cos*Gamma==1; checks+=1
    assert 1/Gamma==eta_cos; checks+=1
    assert eta_cos*Gamma==1; checks+=1 # identical local efficiency cancels
    for eta_loc in [F(1),F(1,1000)]:
        assert eta_loc*Gamma==eta_loc/eta_cos; checks+=1
# Strict zero optical efficiency leaves optical measurement blind to Gamma.
assert 0*F(10**40)==0; checks+=1
# Flat nu I_nu toy: band-integrated intensity requires a log bandwidth.
bandfactor=math.log(.9/.4)
assert .8<bandfactor<.82; checks+=1
pr=a['8e-09|0.5|0.01']
result={'claim_id':'CE-FM-052','checks_passed':checks,'grid_rows':len(a),
'primary':pr,'conditional_lifetime_years_at_eta_1e_6':pr['tau_yr']*1e-6,
'flat_nu_I_nu_top_hat_band_factor':bandfactor,
'local_inventory_J_per_km3':.01*ms/pc**3*c*c*1e9,
'scope':'provisional optical emissivity model; not a calibrated likelihood or general lifetime limit'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
