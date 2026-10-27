from pathlib import Path
import json,math,csv,hashlib,subprocess
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=next((R/'campaign_fresh_gravity').glob('CFG884*'));hs={}
for n in ['README.md','FROZEN_CRITERIA.md','cfg884.py','cfg884_results.json','inputs_tolstoy2025_table2.json']:
 p=S/n;hs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','fcc6529b85:'+p])).hexdigest()==h for p,h in hs.items()};assert all(matches.values())
d=json.loads((S/'cfg884_results.json').read_text());i=json.loads((S/'inputs_tolstoy2025_table2.json').read_text());lvd=R/'real_research/data/dsph/lvd_dwarf_mw.csv';lv=next(x for x in csv.DictReader(lvd.open()) if x['key']=='sextans_1');ell=float(lv['ellipticity']);a=i['distance_kpc']*1000*math.tan(math.radians(.62))*math.sqrt(1-ell);G=6.674e-11*1.989e30/(3.0857e16*1e6);out=[];checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)});assert v,n
# Author arXiv v1 Table2 independently read via web, not a final publisher-table check.
auth=[{'label':'MR','fraction':.63,'Rh_deg':.339,'Rh_error_deg':.021,'sigma_kms':7.,'sigma_error_minus_kms':.4,'sigma_error_plus_kms':.4},{'label':'MP','fraction':.37,'Rh_deg':.62,'Rh_error_deg':.05,'sigma_kms':10.5,'sigma_error_minus_kms':.7,'sigma_error_plus_kms':.8}]
for p,q in zip(i['populations'],auth):
 for k,v in q.items():ck('author Table2 '+q['label']+' '+k,p[k]==v)
for f in ['canonical','alt']:
 x=d[f];law=x['models']['L']['pred0']['MP'];y=3*a*(10.5**2-law**2)/G;stock=53.64*2*x['LV'];stored=x['required']['circ|L']['y'][1];ck(f+' independently inverted MP mass',abs(y/stored-1)<1e-12);ck(f+' optimistic entire cold stock below central MP floor',stock<y);out.append({'footing':f,'aMP_pc':a,'law_sigmaMP_kms':law,'optimistic_entire_cold_stock_Msun':stock,'central_MP_minimum_extra_mass_Msun':y,'ratio':y/stock,'two_tracer_stored_floor_Msun_NOT_independently_reproduced':x['required']['circ|L']['M']})
for u in [0,.1,1,10,100]:ck('Plummer shell kernel bounded '+str(u),0<(1+u*u)**(-1.5)<=1)
res={'record':'CE-Sextans-stock-precondition-2026-10-20','source_commit':'fcc6529b85','hashes':hs,'committed_matches':matches,'catalogue_sha256':hashlib.sha256(lvd.read_bytes()).hexdigest(),'author_source':'https://arxiv.org/html/2504.02787v1#S4.T2','source_authentication_scope':'Table2 numerical fields and meanings confirmed against author arXiv v1 HTML. Not final publisher version; sample selection and radial coverage not reconstructed.','checks':checks,'n_checks':len(checks),'rows':out,'scope':'Single-tracer whole-population spherical-Plummer virial mass bound with nonnegative Newtonian-added extra mass and source saved law baseline. Fixed Ups2, entire stock53.64Mstar. Not error-weighted exclusion, not raw Jeans rerun, not actual envelope capacity/transfer rate.'};Path('/private/tmp/ce884_stock_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':out}))
