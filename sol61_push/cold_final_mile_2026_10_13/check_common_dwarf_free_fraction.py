import json,math,csv,sys
from pathlib import Path
r=json.loads(Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json').read_text())
errs={}
for x in csv.DictReader(Path('real_research/data/dsph/lvd_dwarf_mw.csv').open()):
 try:errs[x['name']]=float(x['vlos_sigma_em'])/float(x['vlos_sigma'])
 except:pass
res={}
for foot in ['canonical','alt']:
 def score(eta):
  total=0;rows=[]
  for x in r['dwarfs']:
   f=x['footings'][foot];D=x['Mdyn_in_r12_over_Mb'];model=.512+f['retained_settled_over_Mb']+eta*f['free_total_over_Mb'];lr=.5*math.log(D/model);con=lr*lr/(errs.get(x['name'],.1)**2+(math.log(10)*.15/2)**2);total+=con;rows.append({'name':x['name'],'sigma_pred_over_observed':math.sqrt(model/D),'chi2':con})
  return total,rows
 grid=[i/10000 for i in range(10001)];best=min(grid,key=lambda z:score(z)[0]);c,rows=score(best)
 res[foot]={'shared_inner_fraction_grid_best':best,'chi2':c,'chi2_no_free':score(0)[0],'rows':rows}
assert all(0<=x['shared_inner_fraction_grid_best']<=1 for x in res.values())
Path(sys.argv[1]).write_text(json.dumps({'claim_id':'CE-FM-077B','status':'completed','grid_points':10001,'results':res,'scope':'Exploratory universal inner free-fraction ansatz; not the queued Method A profile or a calibrated inference'},indent=2)+'\n')
print(json.dumps(res,indent=2))
