from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];p=r/'rebuild_2026_10_22/CSM2_single_L_search';out=p/sys.argv[1];files=[p/'bound_source_forward.py',p/'FORWARD_ERROR_CRITERIA.md',p/'FORWARD_ERROR_DERIVATION.md',p/'forward_error_contract.json',*sorted((p/'source_audit_numpy_1_26_4').iterdir()),p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'mass_enclosure_001/outward_mass_vectors.npz',p/'native_matrix_001/native_matrices.npz',p/'projection_dual_inflation.json',p/'exact_dual_001/certificate.json',p.parent/'F2_outer_lensing/f2_aqual.py']
c=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(r),'--contract',str(p/'forward_error_contract.json'),'--output',str(out.relative_to(r)),'--result',str((out/'results.json').relative_to(r)),'--timeout','600','--max-cpu-seconds','480','--max-threads','1','--max-output-bytes','1048576']
for f in files:c+=['--input',str(f.relative_to(r))]
c+=['--',sys.executable,'-I',str(p/'bound_source_forward.py'),'--output',str(out)];raise SystemExit(subprocess.call(c,cwd=r))
