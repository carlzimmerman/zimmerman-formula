import json,math,sys
from pathlib import Path
r=json.loads(Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json').read_text());xs=[.01,.1,.3,1,3,10,100,1000];ss=[.005,.048,.134,.358,.663,.894,.990,.998999];out={}
for x in r['dwarfs']:
 if x['name'] not in ['Fornax','Leo I']:continue
 row={}
 for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
  S=(x['Mdyn_in_r12_over_Mb']-.512)/x['footings'][foot]['retained_settled_over_Mb']
  for i in range(7):
   if ss[i]<=S<=ss[i+1]:q=(S-ss[i])/(ss[i+1]-ss[i]);s=math.exp(math.log(xs[i])+q*math.log(xs[i+1]/xs[i]));replay=ss[i]+math.log(s/xs[i])/math.log(xs[i+1]/xs[i])*(ss[i+1]-ss[i])
  rm=math.sqrt(6.674e-11*x['Mb_Msun']*1.989e30/a0)/3.0857e16;L=math.sqrt(2*rm*x['r12_pc']/s)
  assert abs(replay-S)<1e-12
  row[foot]={'maximum_settled_multiplier':S,'minimum_L_pc_if_CFG691_proxy_multiplies_settled_draw':L}
 out[x['name']]=row
Path(sys.argv[1]).write_text(json.dumps({'claim_id':'CE-FM-078B','status':'completed','results':out,'scope':'Conditional proxy dictionary ONLY: S_CFG691 times retained settled draw is not yet derived from the coupled action. No frozen criteria altered.'},indent=2)+'\n');print(json.dumps(out))
