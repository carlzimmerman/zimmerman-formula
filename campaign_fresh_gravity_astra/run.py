"""Run the finite experiment with pinned inputs and a mathbox v2 manifest."""
import json
import platform
import subprocess
import sys
from pathlib import Path
import astropy
import numpy
import scipy
import sympy

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SKILL = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit')
out = HERE / (sys.argv[1] if len(sys.argv)>1 else 'run_001')
assert not out.exists(), 'Choose a fresh run directory; preserve earlier evidence.'
inputs = [HERE/'experiment.py', HERE/'run.py', HERE/'CONTRACT.md',
          ROOT/'real_research/data/sparc_master_clean.csv',
          ROOT/'real_research/data/xcop/xcop_r500_ettori2019.json']
inputs += sorted((ROOT/'real_research/data/sparc_data').glob('*_rotmod.dat'))
inputs += sorted((ROOT/'real_research/data/xcop').glob('*/*.fits'))
paths = [str(p.relative_to(ROOT)) for p in inputs]
contract = dict(claim_id='AFG-001', mathematics=dict(
    assertion_tested='Exact restricted moment closure and spectral recovery; numerical inverse budgets on pinned cached profiles.',
    coefficient_domain='Binary64 numerical arithmetic; symbolic positive-real derivative.',
    conventions='CONTRACT.md: Q, R and M separate; fixed stellar M/L; both a0 normalizations and separate vacuum/H redshift branches.',
    inputs=paths, bounds=dict(inverse_grid_y=[1e-6, 1e6, 121], monotone_grid=[1e-12, 1e12, 240001],
                             cluster_radii_kpc=[100, 300, 1000], redshifts=[0,.5,1,2,3,5],
                             spectra='four weighted source components and three Gaussian widths'),
    non_claims=['No covariant completion, universal fit, historical novelty, empirical line-moment measurement or covariance-aware significance.',
                'Cached observational reductions are conditional on original distances, geometry and equilibrium modelling.',
                'The unfiltered M radial law is not its complete field theory.']),
    execution_artifacts=paths,
    software=[dict(name=n, version=v) for n,v in [('Python',platform.python_version()),('numpy',numpy.__version__),
        ('scipy',scipy.__version__),('sympy',sympy.__version__),('astropy',astropy.__version__)]],
    randomness=dict(used=False, generator='', seed=None))
contract_file=HERE/(out.name+'_contract.json')
contract_file.write_text(json.dumps(contract, indent=2)+'\n')
cmd=[sys.executable, str(SKILL/'scripts/run_experiment.py'), '--root',str(ROOT),
     '--contract',str(contract_file), '--output',str(out.relative_to(ROOT)), '--timeout','120',
     '--max-output-bytes','1048576','--max-threads','1']
for path in paths:
    cmd.extend(['--input',path])
for name in ['results.json','sparc_accelerations.csv','cluster_inverse_budget.csv']:
    cmd.extend(['--result',str((out/name).relative_to(ROOT))])
cmd += ['--',sys.executable,'-B',str(HERE/'experiment.py'),'--out',str(out)]
result=subprocess.run(cmd,cwd=ROOT)
if (out/'manifest.json').exists():
    validation=subprocess.run([sys.executable,str(SKILL/'scripts/validate_manifest.py'),
        str(out/'manifest.json'),'--root',str(ROOT)],cwd=ROOT)
    if validation.returncode:
        sys.exit(validation.returncode)
sys.exit(result.returncode)
