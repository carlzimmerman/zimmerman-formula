"""Fresh bounded measurement run with hashed contract, code and outputs."""
import json
import platform
import subprocess
import sys
from pathlib import Path
import numpy
import scipy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts')
out=HERE/(sys.argv[1] if len(sys.argv)>1 else 'run_001')
assert not out.exists(), 'Use a new run directory.'
paths=[str((HERE/p).relative_to(ROOT)) for p in ['measurement.py','run.py','CONTRACT.md']]
contract=dict(claim_id='AFG-004-006',mathematics=dict(
    assertion_tested='Q geometry/PSF invariant, width-correction row-space obstruction, Gaussian-width scale degeneracy and sixth-moment separation.',
    coefficient_domain='Binary64 with separately written exact proofs.',
    conventions='Dimensionless velocities sqrt(a_reference*r_reference), source B/a_reference, radius/r_reference; Poisson unnormalized raw moments.',
    inputs=paths,bounds=dict(source_grid=[8,8],psf_sigmas=[.05,.2,.4,.7,1.],
        scales=[1.,float(numpy.sqrt(.315*4**3+.685))],line_noise=['gaussian','symmetric uniform'],
        MC_replicates=400,MC_expected_photons=5000,derivative_grid=[1e-4,1e4,101]),
    non_claims=['No real spectra, empirical instrument calibration, global gravity closure or historical novelty.',
                'The linear-estimator obstruction is not a no-go for model-based inference.']),
    execution_artifacts=paths,software=[dict(name=n,version=v) for n,v in [
        ('Python',platform.python_version()),('numpy',numpy.__version__),('scipy',scipy.__version__)]],
    randomness=dict(used=True,generator='numpy.default_rng / PCG64',seed=27092026))
cp=HERE/(out.name+'_contract.json'); cp.write_text(json.dumps(contract,indent=2)+'\n')
cmd=[sys.executable,str(SKILL/'run_experiment.py'),'--root',str(ROOT),'--contract',str(cp),
     '--output',str(out.relative_to(ROOT)),'--result',str((out/'results.json').relative_to(ROOT)),
     '--timeout','120','--max-output-bytes','1048576','--max-threads','1']
for path in paths: cmd+=['--input',path]
cmd+=['--',sys.executable,'-B',str(HERE/'measurement.py'),'--out',str(out)]
result=subprocess.run(cmd,cwd=ROOT)
if (out/'manifest.json').exists():
    check=subprocess.run([sys.executable,str(SKILL/'validate_manifest.py'),str(out/'manifest.json'),
                          '--root',str(ROOT)],cwd=ROOT)
    if check.returncode: sys.exit(check.returncode)
sys.exit(result.returncode)
