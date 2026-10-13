"""Conditional finite scan: production and conservative cluster rate screen."""
import json,math
from pathlib import Path
from scipy.integrate import quad
P=Path(__file__).resolve().parent
base=json.loads((P.parent/'dilute_decay_v2_run/results.json').read_text())['rows'][-1]
hb=6.582119569e-16;c=299792.458;m=base['m_eV'];M=base['M_eV'];u=.01
rows=[];checks=[]
for S in [.01,.03,.1,.3,.48,1.,4.]:
 q=S/4;lm=base['lambda_min']*math.sqrt(q);g=base['cubic_g_eV']*q**.25
 G=g*g*u/math.sqrt(1+u*u)/(8*math.pi*M);O=2*g*base['source_amplitude_eV']/M
 f=math.sinh(2*O/G)**2
 # Cross-check independent scaling, not merely table interpolation.
 assert abs(G/base['source_width_eV']/math.sqrt(q)-1)<1e-12
 assert abs(O/base['pump_energy_eV']/q**.25-1)<1e-12
 mean=1900.;s=mean*math.sqrt(math.pi)/4
 pdf=lambda v:v*v*math.exp(-v*v/(4*s*s))/(2*math.sqrt(math.pi)*s**3)
 def sigma(v):
  x=(v/(2*c*u))**2
  return S*((2-x/(1-x))/2)**2/(1+u*u*x)
 lower=quad(lambda v:sigma(v)*v*pdf(v)/mean,0,3000,epsabs=1e-10)[0]
 # Conditional running-width vacuum pole ansatz. No kinetic double-counting:
 # this diagnostic integrates the two-body cross section, not a separate conversion term.
 # x=(s_mandelstam-4m²)/(4m²u²); sqrt(s)*Gamma(s)=g² beta/(8pi).
 # Narrow width gives integral in x of sigma/m = S*pi/(alpha²*eta), alpha=2.
 eta=(g*g*(u/math.sqrt(1+u*u))/(8*math.pi))/(4*m*m*u*u)
 vpole=2*c*u
 narrow_area=S*math.pi/(4*eta*(1+u*u))
 resonant_effective=narrow_area*(vpole/2)*vpole*pdf(vpole)/mean
 # An elementary collision-count diagnostic, explicitly assumed halo density/speed.
 rho_kg_m3=.1*1.98847e30/(3.085677581491367e16**3)
 collision_time_gyr=1/(rho_kg_m3*(S*.1)*30e3)/(365.25*86400*1e9)
 rows.append(dict(threshold_cm2_g=S,lambda_min=lm,g_eV=g,lifetime_s=hb/G,occupation_bound=f,bose_enhancement_bound=2*f+f*f,width_over_gap=G/(M-2*m),cluster_partial_lower_cm2_g=lower,passes_partial_screen_only=lower<.35,narrow_pole_diagnostic_cm2_g=resonant_effective,assumed_dwarf_collision_time_Gyr=collision_time_gyr))
checks=[{'name':'width and pump scaling in every row','passed':True},{'name':'all scan points remain dilute at occupation < .001','passed':all(r['occupation_bound']<.001 for r in rows)},{'name':'all remain narrow width/gap < .0001','passed':all(r['width_over_gap']<1e-4 for r in rows)}]
R=dict(rows=rows,checks=checks,all_pass=all(x['passed'] for x in checks),scope='Fixed m=1MeV, u=.01, alpha=2 and source density; normalization scan, no galaxy fit',pole_caveat='Narrow-width leading resonant area with vacuum running-width ansatz; not full coherent scattering calculation or empirical likelihood',collision_time_caveat='Assumed rho=.1 solar mass/pc3, relative speed30km/s; one collision time, not core formation time')
(P/'lower_run'/'results.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2));assert R['all_pass']
