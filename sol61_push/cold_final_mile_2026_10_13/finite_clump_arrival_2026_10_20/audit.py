from pathlib import Path
import json,math,hashlib,subprocess
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=next((R/'campaign_fresh_gravity').glob('CFG877*'));hs={}
for n in ['cfg877.py','FROZEN_CRITERIA.md','README.md','cfg877_results.json']:
 p=S/n;hs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','d646067d6:'+p])).hexdigest()==h for p,h in hs.items()};assert all(matches.values());d=json.loads((S/'cfg877_results.json').read_text());checks=[];out=[];G=6.674e-11*1.989e30/(3.0857e16*1e6)
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)});assert v,n
for f in ['canonical','alt']:
 a=d[f];v=a['Vx'];M=a['Mcl_Msun'];t=a['rt_pc'];ck(f+' displayed scale GM/V2',abs(t-G*M/v**2)<1e-9)
 # Exact actual cap radius solves r^3/(r^2+c^2)=GM/V2, not r=t.
 lo,hi=t,t+104*2
 for _ in range(100):
  r=(lo+hi)/2
  if r**3/(r*r+104**2)<t:lo=r
  else:hi=r
 cap=(lo+hi)/2;ck(f+' actual cap larger than displayed scale',cap>t)
 for group,g in a['groups'].items():
  for row in g['rows']:
   if row['name'] not in ['Draco','Sextans','Fornax','Leo I']:continue
   r=row['r12'];extra=min(v*v*r**3/(G*(r*r+104**2)),M);pred=math.sqrt(row['law']**2+G*extra/(3*r));ck(f+' '+row['name']+' saved prediction',abs(pred-row['pred'])<1e-10)
   need=3*r*(row['sigma']**2-row['law']**2)/G
   out.append({'footing':f,'name':row['name'],'group':group,'sigma_pred':pred,'sigma_obs':row['sigma'],'needed_extra_mass_Msun_central':need,'available_extra_mass_Msun_aperture':extra,'total_clump_mass_Msun':M,'mass_ratio_needed_to_total_clump':need/M,'cap_radius_pc_actual':cap,'displayed_GM_over_V2_scale_pc':t})
res={'record':'CFG877-individual-budget-2026-10-20','source_commit':'d646067d6','format':'custom saved-arithmetic audit; not v2','hashes':hs,'committed_matches':matches,'n_checks':len(checks),'checks':checks,'rows':out,'scope':'Replays source saved predictions and inverts identical source aperture estimator; no raw observational error likelihood/bootstrap or formation simulation. Central requirements are not uncertainty-aware exclusions.'};Path('/private/tmp/ce877_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':out},indent=1))
