from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];p=root/'rebuild_2026_10_22/CSM2_single_L_search';data=root/'real_research/data/lensing_rar';csm=root/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration'
files=[p/'interval_local.py',p/'native_matrix_001/native_matrices.npz',p/'native_matrix_001/results.json',p/'INTERVAL_001_CRITERIA.md',p/'interval_contract.json',p/'native_matrix.py',p/'projection_operator.py',p/'NATIVE_MATRIX_CRITERIA.md',p/'native_matrix_contract.json',csm/'run_003_audited/results.json',csm/'run_004_replay/results.json',data/'lr_lenses.npz',data/'cfg110_perlens.npz',*sorted((data/'brouwer2021_rar').glob('Fig-3_Lensing-rotation-curves_Massbin*.txt')),root/'rebuild_2026_10_22/F2_outer_lensing/f2_outer_lensing.py',root/'rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py']
files+= [root/f for f in __import__('json').loads((csm/'run_003_audited/manifest.json').read_text())['execution_artifacts']]
out=p/sys.argv[1];cmd=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(root),'--contract',str(p/'interval_contract.json'),'--output',str(out.relative_to(root)),'--result',str((out/'results.json').relative_to(root)),'--timeout','600','--max-cpu-seconds','480','--max-output-bytes','1048576','--max-threads','1']
for f in sorted(set(files)):cmd+=['--input',str(f.relative_to(root))]
cmd+=['--',sys.executable,'-I',str(p/'interval_local.py'),'--output',str(out)];raise SystemExit(subprocess.call(cmd,cwd=root))
