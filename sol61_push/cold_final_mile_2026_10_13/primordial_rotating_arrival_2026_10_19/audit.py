import json,math,hashlib,subprocess,sys
from pathlib import Path
import numpy as np
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');B=R/'campaign_fresh_gravity';S=B/'CFG845_primordial_vs_rotating';
# Locate by file inventory; fixed unique CFG845 path.
S=next(p for p in B.iterdir() if p.is_dir() and p.name.startswith('CFG845_'));names=['cfg845.py','FROZEN_CRITERIA.md','README.md','cfg845_results.json','cfg845_results_MUTATE.json'];paths=[S/n for n in names]+[B/'CFG844_primordial_free_core/cfg844_results.json',B/'CFG654_independent_inputs/cfg654_ics_tables_cmb.npz'];hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};d=json.loads((S/'cfg845_results.json').read_text());m=json.loads((S/'cfg845_results_MUTATE.json').read_text());r44=json.loads(paths[-2].read_text());T=np.load(paths[-1]);rho0=2.775e11*(float(T['omega_b'])+float(T['omega_c']))/1e9;fraction=.9*float(T['omega_c'])/(float(T['omega_b'])+float(T['omega_c']));G,MS,KPC,A0=6.674e-11,1.989e30,3.0857e19,9.3603e-11;checks=[];rows=[];extra={};rawhash={}
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
x=np.log10([q['r12']/q['rvir'] for q in r44['rows']]);y=np.log10([q['P'] for q in r44['rows']]);gam,a=np.polyfit(x,y,1);ck('calibration a',abs(a-d['calib']['a'])<1e-12);ck('calibration gamma',abs(gam-d['calib']['gamma'])<1e-12);k1=10**(a+gam*np.median(x))/np.median([q['P'] for q in r44['rows']]);ck('K1 actually misses10percent',abs(k1-1)>.1)
for q in d['galaxies']:
 p=R/'real_research/data/sparc_data'/(q['name']+'_rotmod.dat');rawhash[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest();plain=[];capped=[];ncap=0
 rf=178*rho0*(1+q['zc'])**3*fraction;supply=rf*4*math.pi*q['rvir']**3/3
 for l in p.read_text().splitlines():
  if not l.strip() or l.startswith('#'):continue
  radius,V,eV,Vg,Vd,Vb=map(float,l.split()[:6])
  if V<=0 or radius<=0 or eV/V>=.1:continue
  gb=(Vg*abs(Vg)+.5*Vd*abs(Vd)+.7*Vb*abs(Vb))*1e6/(radius*KPC)
  if gb<=0:continue
  u=radius/q['rvir']
  if not .01<=u<=.5:continue
  gl=gb/(-math.expm1(-math.sqrt(max(gb/A0,1e-15))));go=V*V*1e6/(radius*KPC);eta=10**(a+gam*math.log10(u))*u**3;ncap+=eta>1
  def delta(M):return math.log10(go/(gl+G*M*MS/(radius*KPC)**2))
  plain.append(delta(eta*supply));capped.append(delta(min(eta,1)*supply))
 ck(q['name']+' point count',len(plain)==q['n']);ck(q['name']+' raw differential replay',abs(float(np.median(plain))-q['d'])<1e-10)
 rows.append({'name':q['name'],'source_D':q['d'],'mass_capped_D':float(np.median(capped)),'n':len(plain),'n_mass_cap_active':int(ncap)})
D=np.array([q['source_D'] for q in rows]);C=np.array([q['mass_capped_D'] for q in rows]);rng=np.random.default_rng(845);bs=[rng.choice(D,len(D)).mean() for _ in range(2000)];rng=np.random.default_rng(845);bc=[rng.choice(C,len(C)).mean() for _ in range(2000)]
ck('D source replay',abs(D.mean()-d['D'])<1e-12);ck('bootstrap source replay',abs(np.std(bs)-d['sD'])<1e-12);ck('mutation mean law-only',abs(m['D']-np.mean([q['obs'] for q in m['galaxies']]))<1e-12);ck('all sources unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in {**hashes,**rawhash}.items()))
res={'record':'CE845-ARRIVAL-AUDIT-2026-10-19','checks':checks,'n_checks':len(checks),'rows':rows,'source_commit':'c2f63ebbe','source_hashes':hashes,'raw_rotation_curve_hashes':rawhash,'K1_ratio':k1,'source_D':float(D.mean()),'source_error':float(np.std(bs)),'capped_exploratory_D':float(C.mean()),'capped_exploratory_error':float(np.std(bc)),'capped_exploratory_z':float(C.mean()/np.std(bc)),'mass_overdraw_points':sum(q['n_mass_cap_active'] for q in rows),'total_points':sum(q['n'] for q in rows),'scope':'Raw rotation-point differential replay using saved galaxy selection/zc/rvir and inherited native constants; selection/catalogue mass/collapse roots not independently regenerated. Exploratory mass cap is not a frozen verdict repair. Calibration K1 remains failed.','non_claims':['No original scorer run, live experiment or manuscript edited','No proof all primordial or spin-dependent histories excluded','CFG846 within-SPARC NO PATTERN read but not independently reconstructed']};Path('/private/tmp/ce845_audit.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k not in ['checks','rows','source_hashes','raw_rotation_curve_hashes']},indent=1))
