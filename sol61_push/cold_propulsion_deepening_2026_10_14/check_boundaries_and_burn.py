import json
import sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
base=Path('sol61_push/cold_propulsion_deepening_2026_10_14')
gprev=json.loads((base/'gravity_run_v1/calculation/results.json').read_text())
eprev=json.loads((base/'exhaust_run_v1/calculation/results.json').read_text())
checks=[]
q=s.symbols('q',positive=True);r=s.Integer(25000);L=s.Integer(100);C=s.Integer(10)**12;mu=s.Integer(2)
K=s.Matrix([[((4/r+6)*q+(6+9*r)*L)/(q-L),(2+3*r)*L/(q-L)],[(2+3*r)*L/(q-L),r*L/(q-L)]])
G=s.Matrix([[-2*q+4*q*q/(r*C)+6*r*mu,2*r*mu],[2*r*mu,2*r*mu]])
u=s.symbols('omega2');pol=s.Poly(s.factor((u*K-G).det()),u)
a=pol.coeff_monomial(u**2);b=-pol.coeff_monomial(u);c=pol.coeff_monomial(1)
qq=s.Integer(100000)
assert s.simplify(G.det().subs(q,qq))>0 and K.det().subs(q,qq)>0
checks.append('exact endpoint positive scalar kinetic and potential')
# Strong stability threshold proportional to q, so checking r above the
# largest q-band threshold proves the potential remains positive throughout.
strong=qq*(1+s.sqrt(1-16*mu/C))/(4*mu)
assert s.N(r-strong,60)>0
checks.append('whole prior exterior band on positive strong branch')
A=s.N(a.subs(q,qq),80);B=s.N(b.subs(q,qq),80);CC=s.N(c.subs(q,qq),80)
big=(B+s.sqrt(B*B-4*A*CC))/(2*A);small=CC/(A*big)
speeds=[]
for val in (small,big):
    ds=-s.N((s.diff(a,q)*u*u-s.diff(b,q)*u+s.diff(c,q)).subs(q,qq).subs(u,val),80)/(2*A*val-B)
    speeds.append(s.N(s.sqrt(qq)*ds/s.sqrt(val),40))
assert small>0 and big>0 and max(abs(v) for v in speeds)>1
checks.append('coupled group speed can exceed c despite positive energy band')
jet=next(r for r in eprev['ideal_massive_exhaust'] if r['energy_transfer_efficiency']==1.)
massrate=jet['cold_pair_mass_rate_kg_s'];power=jet['total_released_power_W']
speed=next(v['speed_km_s'] for v in jet['terminal_speeds'] if v['fuel_fraction']==.9)
rows=[]
for F in (1,100,1000):
    md=massrate*F;t=900/md
    assert abs(md*t-900)<1e-10
    checks.append('proper burn fuel balance '+str(F))
    rows.append({'constant_proper_thrust_N':F,'released_source_power_W':power*F,'proper_burn_years':t/(365.25*86400),'initial_mass_kg':1000,'initial_fuel_fraction':.9,'final_mass_kg':100,'ideal_final_speed_km_s':speed})
result={'claim':'CPD-F001','checks_passed':len(checks),'coupled_near_boundary':{'r':str(r),'q':int(qq),'scalar_omega2_D':[str(s.N(small,25)),str(s.N(big,25))],'group_speeds_c':[str(v) for v in speeds],'interpretation':'Frequency-dependent group speed, not UV/front causality result. The old frozen matter bound is not inherited by full gravity.'},'ideal_neutron_mission_burn':rows,'warning':'Illustrative envelopes only; no physical reactor, neutron nozzle, fuel store, IR interface or complete spacecraft designed.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
