"""Seal actual completed artifact closure, preserving prior contracts."""
import json,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'cold_pre_stellar_settling_2026_10_25';kind=sys.argv[1];assert kind in ['analysis','audit'];d=json.loads((P/'Draco_contract.json').read_text());d['claim_id']='CCT021_'+kind.upper();d['mathematics']['assertion_tested']=('Complete later field/observational diagnostics and exact-time ancestor comparisons' if kind=='analysis' else 'Original hashes/operators/invariants, exact restart, first birth and stellar coverage');d['mathematics']['bounds']={'scope':'actual completed evidence; no substitution of target horizon'};d['randomness']={'used':False,'generator':'','seed':None}
files=[P/f for f in ['analyze_late.py' if kind=='analysis' else 'verify_late.py','run_check.py','CONTRACT.md','ANALYSIS_CONTRACT.md']]+[OLD/f for f in ['kernel.py','kernel_gated.py','kernel_pade9.py','test_kernel.py','test_gated.py','test_pade9.py','test_prolongation.py','prolongation_v2.py','CONTRACT.md','ENERGY_SCOPE_CORRECTION.md']]
files += [P.parent/'cold_formation_data_2026_10_25'/f for f in ['radial_v4.py','radial_v2.py','stars_v2.py','hst_onset.py']]
files += [P.parent/'cold_full_envelope_data_2026_10_25'/f for f in ['physics.py','fit_002/result.json','hst_data/DRACO_BINS.dat','hst_data/README.txt']]+[ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']
folders=[f for f in P.iterdir() if f.is_dir() and (f/'manifest.json').exists() and not f.name.startswith('audit_')]+[OLD/f for f in ['Draco_base','Draco_base_continued','Draco_fine','Sextans_base','Sextans_base_continued','Sextans_fine','Sextans_fine_continued']]
for folder in folders:
 for f in ['manifest.json','result.json','field.npz','stars.npz','progress.json']:
  if (folder/f).exists():files.append(folder/f)
 if kind=='audit':
  mf=json.loads((folder/'manifest.json').read_text());files += [ROOT/x['path'] for x in mf['input_artifacts']+mf['outputs']]
d['execution_artifacts']=sorted(set(str(f.relative_to(ROOT)) for f in files));(P/((sys.argv[2] if len(sys.argv)>2 else kind)+'_contract.json')).write_text(json.dumps(d,indent=2))
