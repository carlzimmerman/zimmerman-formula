from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];p=root/'rebuild_2026_10_22/CSM2_single_L_search';data=root/'real_research/data/lensing_rar';csm=root/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration'
files=[p/'native_matrix.py',p/'projection_operator.py',p/'NATIVE_MATRIX_CRITERIA.md',p/'native_matrix_contract.json',csm/'run_003_audited/results.json',csm/'run_004_replay/results.json',data/'lr_lenses.npz',data/'cfg110_perlens.npz',*sorted((data/'brouwer2021_rar').glob('Fig-3_Lensing-rotation-curves_Massbin*.txt')),root/'rebuild_2026_10_22/F2_outer_lensing/f2_outer_lensing.py',root/'rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py']
out=p/sys.argv[1];cmd=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(root),'--contract',str(p/'native_matrix_contract.json'),'--output',str(out.relative_to(root)),'--result',str((out/'results.json').relative_to(root)),'--timeout','180','--max-cpu-seconds','120','--max-output-bytes','1048576','--max-threads','1']
for f in files:cmd+=['--input',str(f.relative_to(root))]
cmd+=['--',sys.executable,'-I',str(p/'native_matrix.py'),'--output',str(out)];raise SystemExit(subprocess.call(cmd,cwd=root))
