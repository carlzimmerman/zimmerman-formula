"""Pin exact source and completed input closure before the named execution."""
import argparse,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];PREV=P.parent/'cold_fine_late_collapse_2026_10_25';OLD=P.parent/'cold_pre_stellar_settling_2026_10_25'
ap=argparse.ArgumentParser();ap.add_argument('case',choices=['screen','temporal','Draco','Sextans','analysis','audit']);a=ap.parse_args();dest=P/(a.case+'_contract.json');assert not dest.exists();d=json.loads((PREV/'Draco_contract.json').read_text());d['claim_id']='CCT022_'+a.case.upper();d['mathematics']['assertion_tested']='CCT022 CONTRACT.md finite assertion: '+a.case;d['mathematics']['conventions']='CCT022 CONTRACT.md; original criteria unchanged';d['mathematics']['bounds']={'case':a.case,'scope':'finite coverage only'};files=set();seen=set();sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def include(path):
 files.add(str(path.relative_to(ROOT)))
def closure(mf):
 if mf in seen:return
 seen.add(mf);include(mf);m=json.loads(mf.read_text())
 for x in m['input_artifacts']+m['outputs']:
  f=ROOT/x['path'];assert sha(f)==x['sha256'];include(f)
  if 'sha256_after' in x:assert x['sha256_after']==x['sha256']
  if f.name=='manifest.json':closure(f)
for f in ['CONTRACT.md','seal.py','run_case.py']:include(P/f)
script={'screen':'refinement_screen.py','temporal':'temporal_probe.py','analysis':'analyze.py','audit':'verify_late.py'}.get(a.case)
if script:include(P/script)
for gal in (['Draco','Sextans'] if a.case not in ['Draco','Sextans'] else [a.case]):closure(PREV/(gal+'_fine_late')/'manifest.json')
for f in ['kernel.py','kernel_gated.py','kernel_pade9.py','test_kernel.py','test_gated.py','test_pade9.py','test_prolongation.py','prolongation_v2.py']:include(OLD/f)
if a.case in ['Draco','Sextans']:
 d['mathematics']['bounds'].update(parent=str((PREV/(a.case+'_fine_late')).relative_to(ROOT)),ne=8192,tol=1.25e-8,T=8,wall_seconds=1800);include(OLD/'continue_gated.py')
if a.case in ['analysis','audit']:
 for f in P.glob('*/manifest.json'):closure(f)
 for f in ['controls_002/manifest.json','analysis_001/manifest.json']:closure(PREV/f)
 for folder in ['Draco_base','Draco_base_continued','Draco_fine','Sextans_base','Sextans_base_continued','Sextans_fine','Sextans_fine_continued']:closure(OLD/folder/'manifest.json')
 for f in ['radial_v4.py','radial_v2.py','stars_v2.py','hst_onset.py']:include(P.parent/'cold_formation_data_2026_10_25'/f)
 for f in ['physics.py','fit_002/result.json','hst_data/DRACO_BINS.dat','hst_data/README.txt']:include(P.parent/'cold_full_envelope_data_2026_10_25'/f)
 include(ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv')
d['execution_artifacts']=sorted(files);d['randomness']={'used':a.case in ['Draco','Sextans'],'generator':'PCG64' if a.case in ['Draco','Sextans'] else '', 'seed':1025 if a.case in ['Draco','Sextans'] else None};dest.write_text(json.dumps(d,indent=2));print(str(dest.relative_to(ROOT)))
