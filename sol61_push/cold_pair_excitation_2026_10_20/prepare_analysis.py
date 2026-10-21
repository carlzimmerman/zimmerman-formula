"""Freeze finite analysis inputs and launch the bounded audit runner."""
from pathlib import Path
import json, subprocess

here=Path(__file__).resolve().parent
root=here.parents[1]
out=here/'analysis_run_001'
old=root/'sol61_push/cold_fragment_modes_2026_10_20'
refs=here/'matched_refs_run_004'
cases=['pair_inphase','pair_dt_half','pair_dx_fine','pair_antiphase',
       'isolated_static','isolated_moving','pair_separation','pair_faster']
inputs=[here/'analyze_pairs.py',here/'pair_projection.py',Path(__file__).resolve(),
        old/'radial_tools.py',old/'outgoing_library.py',
        root/'sol61_push/cold_completion_2026_10_20/run_001/results.json',
        refs/'manifest.json',refs/'results.json',
        old/'natural_run_002/Q80000_L60_N1199.npz',
        old/'profile_origin/run_001/Q80000.npz']
for Q in [136000,140000]:
    tag=f'Q{Q}_L60_N1199.npz'
    inputs.extend([refs/tag,refs/('profile_'+tag)])
for case in cases:
    run=here/(case+'_run_001')
    inputs.extend([run/'manifest.json',run/'results.json',
                   run/'evolution/log.jsonl',run/'evolution/enclosed_energy.jsonl'])
    times=[]
    if case in ['pair_inphase','pair_dt_half','pair_dx_fine','pair_separation']:
        times.extend(range(80,241,20))
    if case=='pair_inphase':times.extend([0,60,140,240])
    if case=='pair_antiphase':times.append(240)
    if case=='isolated_static':times.extend([0,80,120,160,200,240])
    inputs.extend(run/'evolution'/f'snap_t{t*1000:09d}.bin' for t in sorted(set(times)))
artifacts=[str(p.relative_to(root)) for p in inputs]
assert len(set(artifacts))==len(artifacts)
contract={
 'claim_id':'CE-ACTUAL-PAIR-CONDITIONAL-MODE-ANALYSIS-2026-10-20',
 'mathematics':{
   'assertion_tested':'Summarize eight completed actual field evolutions; project finite snapshots onto pinned Q136k/Q140k modes, compare frame/grid/time controls, and recompute weak Y20 radiation coefficients on those reference backgrounds.',
   'coefficient_domain':'Binary64 quadrature, cubic field interpolation, sparse outgoing solves, finite least-squares frequency scan',
   'conventions':'Canonical reduced order(u,s,chi,v,t), unit no-half K=1. m=0,Y20 angular norm1. Gyro operator always uses reference omega; two explicit velocity-frame choices are compared. Aperture Q/E are inventories, not automatically bound mass/escape. No implicit mode-energy acceptance.',
   'inputs':['Eight completed collision/control runs','Accepted discrete Q136k/Q140k references','True-origin Q80k isolated-control profile and mode','Prior fixed same-action equations and outgoing solver'],
   'bounds':{'mode_references':[136000,140000],'projection_times':list(range(80,241,20)),
             'fit_radius':12,'angular_nodes':48,'interpolation_order':3,
             'frame_choices':['reference_omega','fitted_omega'],
             'exploratory_frequency_search':[.04,.075,.00005],
             'fit_window':[120,240],'fit_basis':'constant+exp(i Omega t)+exp(2i Omega t)',
             'max_measured_RSS_bytes':1000000000,
             'source_work_relative_max':1e-6,'linear_residual_max':1e-8,
             'reference_omega_match_max':1e-11},
   'non_claims':['No persistent linear mode-energy fraction without remnant/reference/amplitude acceptance',
                 'No asymptotic escape, orbital angular momentum transfer, physical mass scale or dwarf capture/population kernel',
                 'No four-dwarf normalization/profile/stock/heating closure',
                 'Exploratory finite-frequency fit is not independent confirmation or a spectral theorem']},
 'execution_artifacts':artifacts,
 'software':[{'name':'Python','version':'3.9.6'},{'name':'NumPy','version':'1.26.2'},
             {'name':'SciPy','version':'1.11.4'},{'name':'Matplotlib','version':'3.9.4'}],
 'randomness':{'used':False,'generator':'','seed':None}}
path=here/'analysis_contract.json'
if path.exists():raise FileExistsError('contract already frozen')
path.write_text(json.dumps(contract,indent=2)+'\n')
runner=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
argv=['python3',str(runner),'--root',str(root),'--contract',str(path.relative_to(root)),
      '--output',str(out.relative_to(root)),'--timeout','180','--max-cpu-seconds','120',
      '--max-threads','1','--max-output-bytes','1048576']
for p in artifacts:argv.extend(['--input',p])
results=[out/'results.json',out/'pair_density.png',out/'pair_diagnostics.png']
results.extend(out/f'outgoing_Q{Q}_ell{ell}.npz' for Q in [136000,140000] for ell in [0,2,4])
for p in results:argv.extend(['--result',str(p.relative_to(root))])
argv.extend(['--','python3',str((here/'analyze_pairs.py').relative_to(root)),
             str(refs.relative_to(root)),str(out.relative_to(root))])
raise SystemExit(subprocess.run(argv,cwd=root).returncode)
