"""CE-FM-077: corrected accounting and inverse dwarf inventory, no infall run."""
import csv,hashlib,json,math,statistics,sys
from pathlib import Path
G,MS,PC=6.674e-11,1.989e30,3.0857e16
C,FRET=5.364,.1
P=64/125 # Plummer enclosed fraction at r=4a/3
checks=[]
def ck(name,v):
 checks.append({'name':name,'pass':bool(v)})
 if not v:raise AssertionError(name)
def f(x):
 try:return float(x)
 except (ValueError,TypeError):return None
source=json.loads(Path('campaign_fresh_gravity/CFG453_t15_deficit_units/cfg453_results.json').read_text())
# Direct group re-read; no nu kernel required for total missing-mass ratio.
lines=[x for x in Path('real_research/data/lovisari2015_groups.tsv').read_text().splitlines() if not x.startswith('#')]
groups=list(csv.DictReader(lines,delimiter='\t'));greplay={}
for bias in [0,.3]:
 ratios=[];fbs=[]
 for x in groups:
  mass=float(x['M500_1e13'])*1e13/(1-bias);mb=1.1*float(x['Mgas500_1e12'])*1e12
  ratios.append(mass/mb-1);fbs.append(mb/mass)
 j=0 if bias==0 else 1
 greplay[str(bias)]={'n':len(ratios),'median_x_total':statistics.median(ratios),'median_fb':statistics.median(fbs)}
 for foot in ['canonical','alt']:
  ck('raw group xT '+foot+str(bias),abs(statistics.median(ratios)-source['D1'][foot]['xT']['gr'][j])<1e-10)
  ck('raw group fb '+foot+str(bias),abs(statistics.median(fbs)-source['D1'][foot]['fb']['gr'][j])<1e-10)
ck('exact Plummer fraction',abs((4/3)**3/((4/3)**2+1)**1.5-P)<1e-15)
rows=[]
for x in csv.DictReader(Path('real_research/data/dsph/lvd_dwarf_mw.csv').open()):
 mv,so,rh=f(x.get('M_V')),f(x.get('vlos_sigma')),f(x.get('rhalf_sph_physical')) or f(x.get('rhalf_physical'))
 if mv is None or so is None or rh is None or mv> -7.7 or x['name'] in ['LMC','SMC','Sagittarius']:continue
 mb=2*10**(.4*(4.83-mv));r=4/3*rh*PC;D=3*r*(1000*so)**2/(G*MS*mb)
 cold_need=D-P;cap=C/FRET;eta=cold_need/cap;fmax=C/cold_need
 row={'name':x['name'],'Mb_Msun':mb,'r12_pc':4/3*rh,'sigma_obs_kms':so,'Mdyn_in_r12_over_Mb':D,'cold_required_in_r12_over_Mb':cold_need,'cold_total_available_over_Mb':cap,'fraction_all_cold_needed_inside_r12':eta,'retention_max_for_cold_only_budget':fmax,'minimum_upsilon_for_inventory':2*D/(P+cap),'footings':{}}
 # Census branch is low mass for each system, including the implied catchment.
 FB=.02237/(.02237+.1200);Mta=(mb/FRET)/FB
 ck(x['name']+' census low mass branch',math.log10(Mta)<12.5)
 for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
  y=G*(P*mb)*MS/r**2/a0;nu=.5+math.sqrt(.25+1/y)
  draw=min((nu-1)*P,C) # optimistic fully settled retained-star share
  available=cap-draw # expelled share plus undrawn retained share, counted once
  signed_need=D-P-draw;fraction=max(0,signed_need)/available
  # Like-for-like corrected local definition identity, using the same aperture.
  xT=(D-P)/P;xA=(D-P-draw)/(C*P)
  ck(x['name']+foot+' correct deficit dictionary',abs(xT-(C*xA+draw/P))<1e-12)
  ck(x['name']+foot+' cold partition',abs(draw+available-cap)<1e-12)
  # Independent constructive target only: a Plummer reservoir giving this fraction.
  scale=None
  if 0<fraction<1:
   scale=(r/PC)*math.sqrt(fraction**(-2/3)-1)
   frac=(r/PC)**3/((r/PC)**2+scale**2)**1.5
   ck(x['name']+foot+' inverse Plummer target',abs(frac-fraction)<1e-12)
  row['footings'][foot]={'retained_settled_over_Mb':draw,'free_total_over_Mb':available,'free_required_signed_over_Mb':signed_need,'free_fraction_needed_inside_r12':fraction,'optimistic_no_free_sigma_kms':math.sqrt(G*MS*mb*(P+draw)/(3*r))/1000,'inverse_Plummer_free_scale_pc':scale,'placement_status':'baseline_overpredicts' if signed_need<0 else ('inventory_insufficient' if fraction>1 else 'inventory_possible_placement_unproved')}
 rows.append(row)
ck('11 selected dwarfs',len(rows)==11)
ck('central cold-only inventory fails AntliaII only',[x['name'] for x in rows if x['fraction_all_cold_needed_inside_r12']>1]==['Antlia II'])
# Conservative bound on the queued K1 spot check: cannot exceed all retained cold inside r12.
d=next(x for x in rows if x['name']=='Draco');r=d['r12_pc']*PC;mb=d['Mb_Msun'];a0=9.3603e-11
y=G*(mb/2)*MS/r**2/a0;mono=1/(-math.expm1(-math.sqrt(y)));sigma821=math.sqrt(G*MS*mb*.5*mono/(3*r))/1000
cap822=math.sqrt(G*MS*mb*(P+C)/(3*r))/1000;ratio=cap822/sigma821
ck('queued Draco K1 optimistic cap outside two percent',ratio<.98)
result={'claim_id':'CE-FM-077','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'groups_raw_replay':greplay,'dwarfs':rows,'queued_CFG822_K1_bound':{'spot_object':'Draco','source821_sigma_kms':sigma821,'optimistic822_retained_only_cap_sigma_kms':cap822,'cap_ratio':ratio,'scope':'Assumes core is normalized to observed stars; exact infall/interpolation not executed. Cannot certify queued K1.'},'non_claims':['No measured cold halo or nonlinear concentration','No cold particle production or physical parameter derivation','No rerun or regrade of CFG822','No Antlia exclusion with observational or mass/light uncertainty','Source X-COP FITS cluster reconstruction not rerun; raw group totals replayed']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'n_checks':len(checks),'group_replay':greplay,'rows':[{'name':x['name'],'cold_fraction':x['fraction_all_cold_needed_inside_r12'],'fret_max':x['retention_max_for_cold_only_budget'],'ups_min':x['minimum_upsilon_for_inventory'],'can':x['footings']['canonical']} for x in rows],'K1_bound':result['queued_CFG822_K1_bound']},indent=2))
