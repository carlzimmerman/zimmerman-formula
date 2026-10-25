"""Declare exact completed input closure before each final analysis or audit."""
import json,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];kind=sys.argv[1];assert kind in ['analysis','audit']
base=json.loads((P/'energy_contract.json').read_text());base['claim_id']='CCT020_'+kind.upper();base['mathematics']['assertion_tested']={'analysis':'All completed full-field snapshots, observational projections, sampled fluctuation binding, and matching-time lineage comparisons','audit':'Executable controls, original hashes, raw operators/invariants, first-birth logic and exact restart history'}[kind];base['mathematics']['bounds']={'scope':'completed bounded artifacts only; physical gate failures retained'}
files=[P/x for x in ['analyze.py' if kind=='analysis' else 'verify.py','kernel.py','kernel_gated.py','kernel_pade9.py','test_kernel.py','test_gated.py','test_pade9.py','test_prolongation.py','prolongation_v2.py','CONTRACT.md','ENERGY_SCOPE_CORRECTION.md','ANALYSIS_CONTRACT.md','ANALYSIS_ADDENDUM.md']]
files += [P.parent/'cold_formation_data_2026_10_25'/x for x in ['radial_v4.py','radial_v2.py','stars_v2.py','hst_onset.py']]
files += [P.parent/'cold_full_envelope_data_2026_10_25'/x for x in ['physics.py','fit_002/result.json','hst_data/DRACO_BINS.dat','hst_data/README.txt']]
files += [ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']
for folder in sorted(P.iterdir()):
 if not(folder/'manifest.json').exists():continue
 if kind=='analysis' and not(folder/'field.npz').exists():continue
 if folder.name.startswith('audit_'):continue
 if kind=='audit':
  mf=json.loads((folder/'manifest.json').read_text());files += [ROOT/x['path'] for x in mf['input_artifacts']+mf['outputs']]
 for f in ['manifest.json','result.json','field.npz','stars.npz','progress.json']:
  if (folder/f).exists():files.append(folder/f)
base['execution_artifacts']=sorted(set(str(f.relative_to(ROOT)) for f in files));(P/((sys.argv[2] if len(sys.argv)>2 else kind)+'_contract.json')).write_text(json.dumps(base,indent=2))
