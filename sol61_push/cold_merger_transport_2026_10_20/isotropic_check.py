"""Zero-COM-momentum/intrinsic-J emission cannot supply arbitrary orbital J."""
from pathlib import Path
import json,math,sys,resource
R=Path(__file__).resolve().parents[2];B=Path(__file__).resolve().parent
p=json.loads((B/'run_002/results.json').read_text());t=json.loads((R/'sol61_push/cold_collision_outflow_2026_10_20/run_001/results.json').read_text());s=json.loads((R/'campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json').read_text());c=299792.458;rows=[];checks=[]
for x in p['rows']:
 z=next(y for y in t['targets'] if y['name']==x['name']);b=s['results']['canonical']['B0'][x['name']]['base'];J=z['initial_mass_Msun']*z['required_J_per_mass'];samples=[]
 for a in x['shared_release_scan']:
  if not a['mass_budget_pass']:continue
  v=a['wind_speed_at_core_kms'];gamma=1/math.sqrt(1-(v/c)**2);energy_mass_equivalent=gamma*a['new_wind_rest_mass_Msun'];bound=energy_mass_equivalent*b['R']*(2*z['sigma_kms'])/J
  ok=bound<1;checks.append({'name':x['name']+' isotropic-J fail at epsilon'+str(a['epsilon_rest_defect_per_initial_free_mass']),'pass':ok});assert ok
  samples.append({'epsilon':a['epsilon_rest_defect_per_initial_free_mass'],'maximum_advected_orbital_J_fraction':bound})
 rows.append({'name':x['name'],'samples':samples})
out={'rows':rows,'checks':checks,'n_checks':len(checks),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Outgoing ensemble has zero net momentum and zero intrinsic J in each emitter COM, retains isotropy/selection assumption after escape; emitter radius<=R and bulk<=2sigma. Then P=(E_lab/c²)V and orbitalJ=(E_lab/c²)RcrossV. Applies also to massive energetic ejecta. Excludes anisotropic kicks, escaping-subset bias, intrinsic/multipole emission J, coherent near fields and external torques. Kinematic branch test, not full merger no-go.'};Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'at_epsilon_2e6':[{ 'name':r['name'],'Jfraction':next(x for x in r['samples'] if x['epsilon']==2e-6)['maximum_advected_orbital_J_fraction']} for r in rows]},indent=2))
