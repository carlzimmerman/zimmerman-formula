import json,sys
from pathlib import Path
b=Path('sol61_push/cold_final_mile_2026_10_13');a=json.loads((b/'run_080/results.json').read_text());raw=json.loads(Path('campaign_fresh_gravity/CFG822_hex_dsph/cfg822_results.json').read_text());out={};checks=[]
for foot in ['canonical','alt']:
 rows=[]
 for x in a['results'][foot]['rows']:
  y=raw['rows'][foot+'|'+x['name']];F=x['actual_free_inside_over_Mb'];outer_free=53.64*y['free_frac']-F;delta=x['extra_inner_mass_needed_over_Mb'];move_in=max(0,delta);move_out=max(0,-delta);free_out=min(F,move_out);settled_out=move_out-free_out;inner_settled=x['inferred_core_plus_settled_over_Mb']-.512
  feasible=move_in<=outer_free+1e-12 and settled_out<=inner_settled+1e-12
  checks.append({'name':foot+x['name']+' signed mass balance','pass':abs(move_in-free_out-settled_out-delta)<1e-12})
  if feasible:checks.append({'name':foot+x['name']+' nonnegative reassigned categories','pass':outer_free-move_in+free_out>=0 and F+move_in-free_out>=0 and inner_settled-settled_out>=0})
  rows.append({'name':x['name'],'inward_free_transfer_over_Mb':move_in,'available_outer_free_over_Mb':outer_free,'fraction_outer_free_to_move_in':move_in/outer_free,'outward_free_transfer_over_Mb':free_out,'outward_settled_transfer_over_Mb':settled_out,'settled_inner_fraction_removed':settled_out/inner_settled,'mass_only_transfer_feasible_at_fixed_stock':feasible})
 out[foot]=rows
assert all(x['pass'] for x in checks)
assert [x['name'] for x in out['canonical'] if not x['mass_only_transfer_feasible_at_fixed_stock']]==['Antlia II']
res={'claim_id':'CE-FM-081B','status':'completed','n_checks':len(checks),'all_pass':True,'checks':checks,'rows':out,'scope':'Algebraic minimum cold-category transfers at saved core/response, assuming observed stellar aperture fraction. Not a transported equilibrium, work budget, or action solution; potential must be recomputed.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'n_checks':len(checks),'canonical':[x for x in out['canonical'] if x['name'] in ['Draco','Sextans','Fornax','Leo I']]},indent=2))
