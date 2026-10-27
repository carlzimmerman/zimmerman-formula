"""Width and decay-acceptance transfer only; not an independent E137 event recast."""
import json,math,sys,hashlib
from pathlib import Path
from scipy.integrate import quad
p=json.loads(Path('sol61_push/electron_material_wall_2026_10_13/run/results.json').read_text())
source=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
e=math.sqrt(4*math.pi/137.035999084);M=2e6;hc=1.973269804e-7
coef=source['rows'][0]['photon_width_eV']/source['rows'][0]['yukawa']**2
rows=[];checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
for r in p['rows']:
 y=abs(r['ye']);ee=r['electron_width_eV'];electron_phot=coef*y*y;base=ee+electron_phot
 # The smaller retuned delta leaves ordinary widths unchanged at this precision.
 full=ee+r['coherent_photon_width_eV']+r['retuned_carrier_width_eV']
 diff=full-base
 betamin=math.sqrt((2e9/M)**2-1)
 bound=math.expm1(abs(diff)*383/(betamin*hc))
 probabilities=[]
 for energy in [2e9,5e9,10e9,20e9]:
  bg=math.sqrt((energy/M)**2-1)
  def prob(width):
   ell=bg*hc/width
   return ee/width*math.exp(-179/ell)*(-math.expm1(-204/ell))
  a=prob(base);b=prob(full)
  independent=quad(lambda z:ee/(bg*hc)*math.exp(-full*z/(bg*hc)),179,383,epsabs=1e-14,epsrel=1e-11)[0]
  ck('decay integral '+str(y)+' '+str(energy),math.isclose(b,independent,rel_tol=1e-10,abs_tol=1e-16))
  ck('uniform transfer bound '+str(y)+' '+str(energy),abs(b/a-1)<=bound+1e-12)
  probabilities.append({'source_energy_GeV':energy/1e9,'electron_only_decay_probability':a,'extended_electron_decay_probability':b,'ratio':b/a,'extended_lab_decay_length_m':bg*hc/full})
 rows.append({'abs_ye':y,'epsilon_abs_ye_over_e':y/e,'electron_only_total_width_eV':base,'extended_total_width_eV':full,
 'relative_width_change':diff/base,'uniform_relative_probability_change_bound_E_at_least_2GeV':bound,'sampled_probabilities':probabilities})
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
 'non_claims':['Not a production integration or fresh confidence interval',
 'Exclusion membership is separately inspected in the published figure',
 'Transfer bound holds for unchanged primary production and ee detection with stipulated on-shell widths']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
