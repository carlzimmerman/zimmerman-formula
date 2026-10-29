from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];p=r/'rebuild_2026_10_22/CSM2_single_L_search';out=p/sys.argv[1];files=[p/'certify_mass_vectors.py',p/'MASS_ENCLOSURE_CRITERIA.md',p/'mass_enclosure_contract.json',p/'interval_001/results.json',p/'root_sign_001/results.json',p/'native_matrix_001/native_matrices.npz',p/'interval_local.py',p.parent/'CSM1_consistent_core_switch/heldout/MW_BURKERT_MONOTONICITY.md']
c=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(r),'--contract',str(p/'mass_enclosure_contract.json'),'--output',str(out.relative_to(r)),'--result',str((out/'results.json').relative_to(r)),'--timeout','600','--max-cpu-seconds','480','--max-threads','1','--max-output-bytes','1048576']
for f in files:c+=['--input',str(f.relative_to(r))]
c+=['--',sys.executable,'-I',str(p/'certify_mass_vectors.py'),'--output',str(out)];raise SystemExit(subprocess.call(c,cwd=r))
