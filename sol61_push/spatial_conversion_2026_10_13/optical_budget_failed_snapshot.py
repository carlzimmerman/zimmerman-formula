#!/usr/bin/env python3
"""Conditional optical luminosity per source mass, using the prior tree rate.
Benchmark zeta=1, delta=5 eV; Lambda/M=1 is an EFT-edge comparison only.
"""
import json,math,sys
from pathlib import Path
from scipy.special import gamma,betainc
Z=gamma(4)**2*gamma(1.5)/gamma(9.5)
hbar=6.582119569e-16;eV=1.602176634e-19;c=299792458.
delta=5.;hc=1239.8419843320026
fvis=float(betainc(5,5.5,hc/400/delta)-betainc(5,5.5,hc/700/delta))
rows=[];checks=[]
for m in [1000.,12500.,1e6]:
 pair=[]
 for cutoff_ratio in [1.,10.]:
  M=2*m+delta;cutoff=cutoff_ratio*M
  width=Z*delta**8.5/(96*math.pi**5*M*math.sqrt(m)*cutoff**6)
  power=width/hbar*(16*delta/19)*eV*fvis/(M*eV/c**2)
  pair.append(power)
  rows.append(dict(m_eV=m,delta_over_m=delta/m,cutoff_over_M=cutoff_ratio,zeta=1,
   width_eV=width,rate_per_second=width/hbar,visible_power_W_per_kg_of_sources=power,
   source_kg_for_1W_visible=1/power,daughter_rms_v_over_c=math.sqrt(3*delta/(19*m))))
 checks.append(dict(name=f'cutoff sixth-power scaling m={m}',passed=abs(pair[0]/pair[1]/1e6-1)<1e-12))
# Cold daughter requirement v/c <= beta implies a lower mass at fixed gap.
cold=[]
for beta in [.01,.001]:
 m=3*delta/(19*beta*beta);M=2*m+delta;L=10*M
 width=Z*delta**8.5/(96*math.pi**5*M*math.sqrt(m)*L**6)
 power=width/hbar*(16*delta/19)*eV*fvis/(M*eV/c**2)
 cold.append(dict(max_rms_v_over_c=beta,minimum_m_eV=m,visible_power_at_minimum_mass_W_kg=power))
r=dict(all_passed=all(c['passed'] for c in checks),checks=checks,visible_energy_fraction=fvis,cases=rows,cold_requirements=cold,
 scope='Conditional near-threshold tree-level rate per available source mass with zeta=1; no observed coupling, optical transport, population preparation or empirical constraints. Lambda=M is not a controlled EFT hierarchy.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
sys.exit(0 if r['all_passed'] else 1)
