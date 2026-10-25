"""Run the three audited cases with the installed provenance runner."""
import argparse,json,sys,subprocess
from pathlib import Path
import numpy,scipy,astropy
ap=argparse.ArgumentParser(); ap.add_argument('--runner',required=True); args=ap.parse_args()
lane=Path('reviews/cold_shell_covariance_2026_10_24')
inputs=[str(lane/x) for x in ['FROZEN_CRITERIA.md','audit.py','launch.py']]+['reviews/cold_field_inversion_2026_10_24/invert.py','reviews/cold_field_inversion_2026_10_24/run/result.json','reviews/matched_clumping_2026_10_24/compare.py','sol61_push/continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md','sol61_push/cold_envelope_formation_2026_10_24/MECHANISM.md']
for pattern in ['*/*hydro_mass.fits','*/*fgas_profile.fits','*/*mstar.fits']: inputs+=sorted(str(p) for p in Path('real_research/data/xcop').glob(pattern))
contract={'claim_id':'COLD_SHELL_COVARIANCE_20261024','mathematics':{'assertion_tested':'Correlated linear-error extrema and exact marginal-box feasibility for cold-source shell positivity; separate AQUAL and selective Newtonian source maps.','coefficient_domain':'IEEE754 floating point; fixed SI constants inherited from matched comparison','conventions':'Error bounds are sensitivity sets, not joint confidence regions; unknown covariance not imputed. Six fixed physical radii; separate inherited footings; no cold parameter fit.','inputs':['Seven X-COP clusters with marginal widths','Published alternative mass profiles','Existing selective-wave eta=1500 pc km/s, imposed'], 'bounds':{'clusters':7,'radii':6,'footings':[9.3603e-11,1.1312e-10],'box_widths':[1,2,3],'correlation_range':'all PSD unit-diagonal matrices in linear diagnostic'},'non_claims':['No actual correlated posterior probability','No full radius/distance/systematic propagation','No parameter-free cold dynamics or a0 prediction','Released models are not independent datasets','Rectangular witness may be improbable under actual covariance']},'execution_artifacts':inputs,'software':[{'name':'Python','version':sys.version.split()[0]},{'name':'numpy','version':numpy.__version__},{'name':'scipy','version':scipy.__version__},{'name':'astropy','version':astropy.__version__}],'randomness':{'used':False,'generator':'','seed':None}}
(lane/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
for mode in ['run_aqual','run_selective','mutation']:
 out=lane/mode
 cmd=[sys.executable,args.runner,'--root','.', '--contract',str(lane/'contract.json'),'--output',str(out),'--timeout','60','--max-output-bytes','25000','--max-threads','1']
 for f in inputs: cmd+=['--input',f]
 if mode!='mutation':
  for f in ['result.json','shell_bounds.csv','model_sensitivity.csv','repair_sizes.csv','shell_uncertainty.png']: cmd+=['--result',str(out/f)]
 cmd+=['--','python',str(lane/'audit.py'),'--output',str(out)]
 if mode=='mutation': cmd+=['--mutate']
 if mode=='run_selective': cmd+=['--selective']
 ret=subprocess.run(cmd); assert ret.returncode==(1 if mode=='mutation' else 0)
