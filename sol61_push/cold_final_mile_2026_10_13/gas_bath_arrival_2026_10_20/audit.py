from pathlib import Path
import json,math,hashlib,subprocess
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=next((R/'campaign_fresh_gravity').glob('CFG878*'));hs={}
for n in ['cfg878.py','FROZEN_CRITERIA.md','README.md','cfg878_results.json']:
 p=S/n;hs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
matches={p:hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','4e75d21e8:'+p])).hexdigest()==h for p,h in hs.items()};assert all(matches.values());k=1.380649e-23;mH=1.6735575e-27;mMeV=1.782661921e-30;mgas=1.22*mH;checks=[];rows=[]
def ck(n,c):
 checks.append({'name':n,'pass':bool(c)});assert c,n
for T in [8000,10000]:
 gas=math.sqrt(k*T/mgas)/1000;particle=math.sqrt(k*T/mMeV)/1000;fragment=math.sqrt(k*T/(6e7*mMeV))/1000
 ck('equipartition mass ratio '+str(T),abs(particle/gas-math.sqrt(mgas/mMeV))<1e-12)
 rows.append({'T_K':T,'neutral_gas_sigma_kms':gas,'one_MeV_particle_sigma_at_same_T_kms':particle,'illustrative_6e7_quanta_fragment_sigma_at_same_T_kms':fragment,'one_MeV_mass_ratio_Msigma4_at_fixed_a0':(particle/gas)**4})
# detailed balance is a statement about equilibrium temperature, not velocity.
ck('MeV particle cannot have gas speed at equal T',all(r['one_MeV_particle_sigma_at_same_T_kms']>30*r['neutral_gas_sigma_kms'] for r in rows))
res={'record':'CFG878-thermal-transfer-2026-10-20','source_commit':'4e75d21e8','format':'custom bounded stdlib audit, not v2','hashes':hs,'committed_matches':matches,'checks':checks,'n_checks':len(checks),'rows':rows,'scope':'Equal-temperature versus equal-dispersion distinction for nonrelativistic translational thermal equilibrium. 1MeV and fragment mass are illustrative prior ARGON benchmark assumptions, not derived source spectra. Does not exclude bulk-flow entrainment or potential-driven common velocity; neither is computed.'};Path('/private/tmp/ce878_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'rows':rows}))
