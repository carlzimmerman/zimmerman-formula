"""Fixed-bath source occupation reaction clock; not condensate growth kinetics."""
import json,math
from pathlib import Path
p=Path(__file__).parent
b=json.loads((p/'bose_endpoint_run/results.json').read_text())
d=json.loads((p/'detuned_carrier_run/results.json').read_text())
bg=json.loads((p/'portal_cosmology_run/results.json').read_text())['background']
a=d['parameters'];m=a['m_eV'];M=a['M_eV'];gap=M-2*m
hbar=6.582119569e-16;G=6.67430e-11
Gamma=1/d['vacuum_source_lifetime_seconds'];checks=[];rows=[]
def ck(name,v):checks.append(dict(name=name,passed=bool(v)))
for row in b['rows']:
    T=row['T_eV'];scale=row['scale_factor_ratio'];x=gap/(2*T)
    f=1/math.expm1(x) if x<700 else 0.
    B=f*f/(1+2*f)
    direct=1/math.expm1(2*x) if 2*x<700 else 0.
    ck('reaction detailed balance '+str(scale),abs(B-direct)<1e-12*max(1,direct))
    enhancement=1+2*f;rate=Gamma*enhancement
    cosmic_a=scale/(1+a['z'])
    H=math.sqrt(8*math.pi*G/3*(bg['rhom0_kg_m3']/cosmic_a**3+bg['rhor0_kg_m3']/cosmic_a**4+bg['rhoLambda_kg_m3']))
    # Collision term dB/dt=Gamma[f²-(1+2f)B]; perturb B about equilibrium.
    perturb=.1*max(1,B)
    rhs=Gamma*(f*f-(1+2*f)*(B+perturb))
    ck('linearized occupation decay '+str(scale),abs(rhs/(-rate*perturb)-1)<1e-11)
    rows.append(dict(scale_factor_ratio=scale,T_eV=T,daughter_occupation_at_rest_decay_momentum=f,source_zero_momentum_equilibrium_occupation=B,net_relaxation_enhancement=enhancement,gross_decay_enhancement=(1+f)**2,rest_source_relaxation_seconds=1/rate,H_s_inverse=H,rest_relaxation_over_H=rate/H,inmedium_width_over_gap=hbar*rate/gap))
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),vacuum_source_decay_rate_s_inverse=Gamma,scope='Rest-source mode with held-fixed isotropic ideal Bose daughter bath, tree vacuum width and stimulated gain/loss, no coherent condensate or moving-source average',non_claims=['Not global equilibration or condensation time','Large rate/H is only a local necessary consistency screen','Conditional background and temperatures inherited, not independently inferred'])
(p/'bose_reaction_clock_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
