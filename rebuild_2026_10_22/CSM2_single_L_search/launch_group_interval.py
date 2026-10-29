from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];p=r/'rebuild_2026_10_22/CSM2_single_L_search';out=p/sys.argv[1];files=[p/'group_interval.py',p/'GROUP_INTERVAL_001_CRITERIA.md',p/'group_interval_contract.json',p/'group_preflight_001/results.json',p/'group_preflight_001/group_native_evidence.npz',p/'group_preflight_001/selected_groups.json',p/'group_preflight_review.json',p.parent/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',p.parent/'P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py',p.parent/'CSM1_consistent_core_switch/heldout/MW_BURKERT_MONOTONICITY.md']
c=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(r),'--contract',str(p/'group_interval_contract.json'),'--output',str(out.relative_to(r)),'--result',str((out/'results.json').relative_to(r)),'--timeout','600','--max-cpu-seconds','480','--max-threads','1','--max-output-bytes','1048576']
for f in files:c+=['--input',str(f.relative_to(r))]
c+=['--',sys.executable,'-I',str(p/'group_interval.py'),'--output',str(out)];raise SystemExit(subprocess.call(c,cwd=r))
