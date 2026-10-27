import csv,json,math,hashlib,subprocess,sys,time
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import spearmanr
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula'); O=Path(__file__).parent
paths=['campaign_fresh_gravity/CFG827_dwarf_age_sfh_ml/'+x for x in ['cfg827.py','cfg827_results.json','cfg827_results_MUTATE.json','FROZEN_CRITERIA.md']]+['campaign_fresh_gravity/CFG824_dwarf_age_fossil/cfg824_results.json','real_research/data/dsph/emiles_ml_dl/UBBVRIJHK_ku_iPp0.00.MAG','real_research/data/dsph/weisz2014_dl/table5.tsv','real_research/data/dsph/weisz2014_dl/table6.tsv']+['real_research/data/dsph/'+x for x in ['lvd_dwarf_mw.csv','lvd_dwarf_m31.csv','lvd_dwarf_local_field.csv']]
def hashes():return {p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths}
before=hashes(); checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def tsv(p):
 lines=[s for s in (R/p).read_text().splitlines() if s.strip() and not s.startswith('#')];return list(csv.DictReader(lines[:1]+lines[3:],delimiter='\t'))
def sfh(row):
 q=sorted([(float(k[1:]),float(v)) for k,v in row.items() if k.startswith('f') and k[1:].replace('.','').isdigit()],reverse=True)
 weights=[(13.3,q[0][1])]+[(10**((q[i][0]+q[i-1][0])/2-9),q[i][1]-q[i-1][1]) for i in range(1,len(q))]
 ck('monotone SFH '+row['ID'],min(w for t,w in weights)>=-1e-12)
 ck('unit formed mass '+row['ID'],abs(sum(w for t,w in weights)-1)<1e-8)
 return weights
# Reconstruct current mass and luminosity separately, preserving formed-mass weights.
ssp={}
for line in (R/paths[5]).read_text().splitlines()[1:]:
 v=line.split();ssp.setdefault(float(v[2]),[]).append((float(v[3]),float(v[4]),float(v[17])))
for z in ssp:ssp[z].sort()
def ml(bins,z):
 tab=np.array(ssp[z]); ages=np.log10(tab[:,0]);m=l=0
 for t,w in bins:
  u=np.interp(math.log10(t),ages,tab[:,1]);v=np.interp(math.log10(t),ages,tab[:,2]);m+=w*u;l+=w*u/v
 return m/l
T6={r['ID'].strip():r for r in tsv(paths[7])}; histories={}
rename={'Canes Venetici I':'Canes Venatici I','Canes Venetici II':'Canes Venatici II','DDO 210':'Aquarius','Pegasus':'Pegasus dIrr','Sag DIG':'Sagittarius dIrr','M32':'M 32'}
for r in tsv(paths[6]):
 name=rename.get(r['ID'].strip(),r['ID'].strip())
 if name not in histories:histories[name]=sfh(T6.get(r['ID'].strip(),r))
cat={}
for p in paths[8:]:
 for r in csv.DictReader((R/p).open()):cat[r['name']]=r
src=json.loads((R/paths[1]).read_text());raw=json.loads((R/paths[4]).read_text())['rows']; G,MS,PC=6.674e-11,1.989e30,3.0857e16;P=64/125;C=5.364;F=.1
replay={};new=[]
def law(r,ups):
 m=ups*10**(.4*(4.83-float(r['M_V'])));radius=4/3*float(r.get('rhalf_sph_physical') or r['rhalf_physical'])*PC
 y=G*m/2*MS/radius**2/9.3603e-11
 return math.sqrt(G*m*MS/(6*radius)/(-math.expm1(-math.sqrt(y))))/1000
for name,s in src['rows'].items():
 r=cat[name];ups={z:ml(histories[name],z) for z in [-1.31,-1.71,-.71]}
 for z,k in [(-1.31,'ups'),(-1.71,'ups_lo'),(-.71,'ups_hi')]:ck('M/L replay '+name+str(z),abs(ups[z]-s[k])<1e-10)
 e=math.log(raw[name]['so']/law(r,ups[-1.31]));ck('E replay '+name,abs(e-s['E_SFH'])<1e-11)
 replay[name]={'ups':ups,'E':e}
 if name in ['Draco','Ursa Minor','Canes Venatici I','Fornax','Leo I']:
  cases={}
  for tag,u in [('old',2),('primary',ups[-1.31]),('lowZ',ups[-1.71]),('highZ',ups[-.71])]:
   m=u*10**(.4*(4.83-float(r['M_V'])));rad=4/3*float(r.get('rhalf_sph_physical') or r['rhalf_physical'])*PC
   d=3*rad*(1000*raw[name]['so'])**2/(G*MS*m);y=G*P*m*MS/rad**2/9.3603e-11;settled=min(P*(math.sqrt(.25+1/y)-.5),C)
   sig=math.sqrt(G*m*MS*(P+settled)/(3*rad))/1000
   cases[tag]={'ups':u,'baseline_sigma':sig,'obs':raw[name]['so'],'required_cold_fraction_of_total':(d-P)/(C/F),'additional_cold_over_Mstars':d-P-settled,'additional_fraction_remaining':(d-P-settled)/(C/F-settled),'settled_over_Mstars':settled}
  new.append({'name':name,'cases':cases})
oos=[n for n,s in src['rows'].items() if not s['train']];rho,p=spearmanr([replay[n]['E'] for n in oos],[src['rows'][n]['tau90'] for n in oos],alternative='greater')
ck('28 held out',len(oos)==28);ck('rho replay',abs(rho-src['scores']['-1.31']['rho'])<1e-13);ck('p replay',abs(p-src['scores']['-1.31']['p'])<1e-13);ck('NO SIGNAL preserved',src['cls']=='NO SIGNAL' and p>.05)
ck('Fornax and Leo primary baseline below observed',all(x['cases']['primary']['additional_cold_over_Mstars']>0 for x in new if x['name'] in ['Fornax','Leo I']))
ck('Sextans has no SFH-based M/L here','Sextans' not in src['rows']);after=hashes();ck('source hashes unchanged',before==after)
result={'assertion_tested':'Reconstruct CFG827 M/L and heldout primary statistic from local SSP/SFH/catalogue tables; conditional fixed-stock rational-Plummer aperture budget at updated stellar masses. No coupled infall solve.','status':'completed','checks':checks,'n_checks':len(checks),'all_pass':True,'rho':float(rho),'p':float(p),'dwarf_cases':new,'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'inputs_before':before,'inputs_after':after,'versions':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},'non_claims':['Local upstream tables not independently authenticated','SFH/M/L/metallicity/IMF uncertainties not marginalized','No revised frozen verdict, normalization repair, infall profile, or transport dynamics','Sextans stellar M/L unchanged because no matched SFH row','No proof of theory completion']}
(O/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['n_checks','rho','p','dwarf_cases']},indent=2))
