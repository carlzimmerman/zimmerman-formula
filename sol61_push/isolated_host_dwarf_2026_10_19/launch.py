"""Launch only the explicitly enumerated, user-authorized finite runs."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
import numpy as np
import scipy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
REL=HERE.relative_to(ROOT)
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
RUNNER_PYTHON='/opt/homebrew/bin/python3.12'
SIM_PYTHON='/usr/bin/python3'
CASES={
 'pilot_iso':['--ncold','256','--nstar','32','--duration','1000'],
 'pilot_host':['--ncold','256','--nstar','32','--duration','1000','--host'],
 'pilot_host_fine':['--ncold','256','--nstar','32','--duration','1000','--dt','.5','--host'],
 'base_iso':[], 'base_host':['--dt','.5','--host'],
 'nocoll_iso':['--collisionless'], 'nocoll_host':['--collisionless','--dt','.5','--host'],
 'dt_iso':['--dt','1'], 'dt_host':['--dt','.25','--host'],
 'n_iso':['--ncold','4096','--nstar','512'],
 'n_host':['--ncold','4096','--nstar','512','--dt','.5','--host'],
 'h_iso':['--h','100'], 'h_host':['--h','100','--dt','.5','--host'],
}
INPUT_NAMES=['CONTRACT.md','source_inputs.json','run_dwarf.py','dynamics.py',
             'direct_gravity.c','direct_gravity.dylib','launch.py','test_driver.py','test_dynamics.py']


def launch(name):
    if name not in CASES:
        raise ValueError('Unknown run '+name)
    output=REL/('run_'+name)
    (HERE/'contracts').mkdir(exist_ok=True)
    inputs=[str(REL/f) for f in INPUT_NAMES]
    contract=dict(claim_id='ISO_HOST_DAUGHTER_CARRIER_'+name,
      mathematics=dict(assertion_tested='Finite prepared dilute daughter-carrier Boltzmann-Poisson dwarf evolution and E/vector-J closure under declared initial state and numerical scales',
        coefficient_domain='IEEE754 double; softened Newtonian N-body and stochastic finite-support elastic carrier scattering',
        conventions='pc,Msun,Myr; live dwarf stars/cold; optional prescribed static Plummer host; no target-profile forcing or deleted particles',
        inputs=['CONTRACT.md scenario; fixed seed87319; revised .3cm2/g carrier kernel'],
        bounds=dict(case=name,case_arguments=CASES[name],baseline_Ncold=2048,baseline_Nstar=256,
                    baseline_dt_Myr=2,baseline_duration_Myr=10000,softening_pc=40,collision_support_pc=200),
        non_claims=['Not full canonical polarization theory','Not a production-derived initial state',
                    'No continuum, universal core formation or universal exclusion conclusion',
                    'No live host response, radiative cooling, gas history or cosmological assembly']),
      execution_artifacts=inputs,
      software=[dict(name='simulation Python',version=platform.python_version()),dict(name='numpy',version=np.__version__),
                dict(name='scipy',version=scipy.__version__),dict(name='C backend compiler',version='Apple clang21.0.0; cc -O3 -dynamiclib; no fast-math/OpenMP')],
      randomness=dict(used=True,generator='NumPy default_rng PCG64',seed=87319,
                      collision_seed=1087319,initial_phasespace_seed=87319))
    contract_path=HERE/'contracts'/(name+'.json')
    contract_path.write_text(json.dumps(contract,indent=2)+'\n')
    command=[RUNNER_PYTHON,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
             '--contract',str(contract_path),'--output',str(output),
             '--timeout','1800','--max-cpu-seconds','1750','--max-threads','1','--max-output-bytes','1048576']
    for filename in inputs:
        command+=['--input',filename]
    for filename in ('results.json','initial.npz','final.npz'):
        command+=['--result',str(output/filename)]
    command+=['--','nice','-n','19',SIM_PYTHON,str(REL/'run_dwarf.py'),'--output',str(output)]+CASES[name]
    print(json.dumps(dict(case=name,command=command)),flush=True)
    rc=subprocess.call(command)
    print(json.dumps(dict(case=name,exit_code=rc)),flush=True)
    return rc


if __name__=='__main__':
    for name in sys.argv[1:]:
        rc=launch(name)
        if rc:
            raise SystemExit(rc)
