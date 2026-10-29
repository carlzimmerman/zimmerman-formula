from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];p=r/'rebuild_2026_10_22/CSM2_single_L_search';out=p/sys.argv[1];files=[p/'exact_dual.py',p/'DUAL_CRITERIA.md',p/'DUAL_ROUTE.md',p/'dual_contract.json',p/'native_matrix_001/native_matrices.npz',p/'signed_dot_002_cached/signed_map_evidence.npz',p/'signed_dot_002_cached/results.json',p.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json']
c=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(r),'--contract',str(p/'dual_contract.json'),'--output',str(out.relative_to(r)),'--result',str((out/'results.json').relative_to(r)),'--timeout','240','--max-cpu-seconds','180','--max-threads','1','--max-output-bytes','1048576']
for f in files:c+=['--input',str(f.relative_to(r))]
c+=['--',sys.executable,'-I',str(p/'exact_dual.py'),'--output',str(out)];raise SystemExit(subprocess.call(c,cwd=r))
