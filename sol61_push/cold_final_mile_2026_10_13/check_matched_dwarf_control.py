"""CE-FM-081: same-model control plus global free-profile normalization obstruction."""
from pathlib import Path
import json,math,sys
base=Path('sol61_push/cold_final_mile_2026_10_13');a=json.loads((base/'run_077/results.json').read_text());old=json.loads((base/'run_080/results.json').read_text());d={x['name']:x for x in a['dwarfs']};raw=json.loads(Path('campaign_fresh_gravity/CFG822_hex_dsph/cfg822_results.json').read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
G,MS,PC=6.674e-11,1.989e30,3.0857e16;pstar=.512;c=5.364
res={}
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 rows=[];lowers=[];uppers=[]
 for row in old['results'][foot]['rows']:
  x=d[row['name']];Mb=x['Mb_Msun'];R=x['r12_pc']*PC;D=x['Mdyn_in_r12_over_Mb'];free=row['actual_free_inside_over_Mb'];y=G*(pstar*Mb)*MS/R**2/a0;nu=.5+math.sqrt(.25+1/y);draw=min((nu-1)*pstar,c);matched=pstar+draw;actual=row['inferred_core_plus_settled_over_Mb'];ratio=math.sqrt(actual/matched)
  ck(foot+row['name']+' matched no-free control within2percent',abs(ratio-1)<.02)
  ck(foot+row['name']+' matched draw independently agrees',abs(draw-x['footings'][foot]['retained_settled_over_Mb'])<1e-12)
  # Even granting an independent arbitrary retained draw in[0,c] to every object,
  # a COMMON multiplier A on saved free inner masses requires these intervals.
  lower=max(0,(D-pstar-c)/free);upper=(D-pstar)/free;lowers.append((lower,row['name']));uppers.append((upper,row['name']))
  rows.append({'name':row['name'],'matched_no_free_sigma':math.sqrt(G*MS*Mb*matched/(3*R))/1000,'saved_no_free_sigma':math.sqrt(G*MS*Mb*actual/(3*R))/1000,'same_model_sigma_ratio':ratio,'allowed_global_free_multiplier_lower':lower,'allowed_global_free_multiplier_upper':upper})
 lower,ln=max(lowers);upper,un=min(uppers)
 ck(foot+' common-free-amplifier interval empty even with independent settlement',lower>upper)
 dr=d['Draco'];Mb=dr['Mb_Msun'];R=dr['r12_pc']*PC;fn=G*MS*Mb/(3*R)/1e6
 def law(frac,kernel):
  y=G*frac*Mb*MS/R**2/a0;nu=(1/(-math.expm1(-math.sqrt(y)))) if kernel=='exp' else (.5+math.sqrt(.25+1/y));return math.sqrt(fn*frac*nu)
 stages={'half_mass_exponential':law(.5,'exp'),'half_mass_rational_uncapped':law(.5,'rational'),'Plummer_rational_uncapped':law(.512,'rational'),'Plummer_rational_capped':math.sqrt(fn*(.512+min((.5+math.sqrt(.25+a0*R**2/(G*.512*Mb*MS))-1)*.512,c)))}
 res[foot]={'max_matched_control_relative_sigma_error':max(abs(z['same_model_sigma_ratio']-1) for z in rows),'Draco_convention_stages':stages,'common_free_multiplier_intersection':{'lower':lower,'lower_driver':ln,'upper':upper,'upper_driver':un,'empty':True},'rows':rows}
result={'claim_id':'CE-FM-081','status':'completed','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'results':res,'scope':'Matched-kernel/cap/aperture diagnostic and necessary interval obstruction for a common multiplier on saved free profiles. No trajectory rerun, original frozen control remains failed, no physical normalization repair claimed.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{z:v for z,v in d.items() if z!='rows'} for k,d in res.items()},indent=2));print('checks',len(checks))
