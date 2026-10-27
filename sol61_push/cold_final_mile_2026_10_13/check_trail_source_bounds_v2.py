import json,sys,math,hashlib
l8='campaign_fresh_gravity/CFG768_trail_alpha_and_clocks/';l9='campaign_fresh_gravity/CFG769_trail_condition/'
d=json.load(open(l8+'cfg768_results.json'));q=json.load(open(l9+'cfg769_results.json'));bounds={'DF2':{'canonical':.36,'alt':.33},'DF4':{'canonical':.29,'alt':.26},'DF9':{'canonical':.52,'alt':.46}};out={};checks=0
for foot in ['canonical','alt']:
 out[foot]={}
 for name,bb in bounds.items():
  b=bb[foot]
  row=d['B'][foot]['universal']['rows'][name];age=row['t_Gyr'];tau=row['tau_Gyr'];f=-math.expm1(-age/tau)
  assert abs(f-row['f'])<1e-12 and f>b;checks+=1
  mintau=age/(-math.log1p(-b));eta=b/f
  assert mintau>tau and 0<eta<1;checks+=1
  out[foot][name]=dict(tau_required_min_Gyr=mintau,rate_suppression_max=tau/mintau,eligible_supply_fraction_max=eta)
 assert q['part1'][foot]['verdict']=='TENSION';checks+=1
 assert q['part1'][foot]['n_tested']==3 and q['part1'][foot]['n_requires']==1;checks+=1
h=hashlib.sha256(open(l9+'cfg769_SEALED_predictions.json','rb').read()).hexdigest()
assert h==q['part2']['sha256'];checks+=1
json.dump(dict(checks=checks,bounds=out,sealed_sha256=h,scope='Conditional necessary source/rate bounds and stored classifications, not independent external data validation'),open(sys.argv[1],'w'),indent=2)
