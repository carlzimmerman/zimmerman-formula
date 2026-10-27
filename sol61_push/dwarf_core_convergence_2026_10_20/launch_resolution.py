"""Freeze explicitly requested cases into bounded v2 evidence records."""
import argparse
import json
from pathlib import Path
import platform
import subprocess
import numpy as np
import scipy

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;REL=HERE.relative_to(ROOT)
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
RUNNER='/opt/homebrew/bin/python3.12'


def launch(name,arguments,timeout=7200):
    if not name.replace('_','').isalnum():raise ValueError('simple case name required')
    if (HERE/('run_'+name)).exists():raise FileExistsError('record exists; choose a new case name')
    files=['CONTRACT.md','evolution.py','run_resolution.py','fast_gravity.py','fast_gravity.c','fast_gravity.dylib',
           'profile_diagnostics.py','test_evolution.py','test_resolution_driver.py','test_profile_diagnostics.py','test_fast_gravity.py','launch_resolution.py']
    if '--backend' in arguments and arguments[arguments.index('--backend')+1]=='metal':
        files+=['metal_gravity.py','metal_gravity.mm','metal_gravity.dylib','test_metal_gravity.py']
    inputs=[str(REL/f) for f in files]
    old=REL.parent/'isolated_host_dwarf_2026_10_19'
    inputs += [str(old/f) for f in ['dynamics.py','direct_gravity.c','direct_gravity.dylib','remnant.py','CONTRACT.md','source_inputs.json']]
    inputs += ['sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md']
    contract=dict(claim_id='DWARF_RESOLUTION_'+name,
        mathematics=dict(assertion_tested='Finite full3D resolution extension: quiet prepared dwarf, H4 deterministic gravity and positive-time revisedelasticC22; density, remnant and E/vectorJ diagnostics',
            coefficient_domain='Nativefloat64 or declared tested GPUhighlow expansions; stochasticelasticpairs',
            conventions='pc,Msun,Myr; all original particles retained; self-potential remnant frame; full3D evolution',
            inputs=['CONTRACT.md',arguments],bounds=dict(argv=arguments,wall_seconds=timeout,max_CPU_threads=4),
            non_claims=['A finite completed record alone is not convergence','No source-derived initialstate or canonicalresponse-field dynamics','Conditional count intervals exclude model/sampling/time/systematicerrors']),
        execution_artifacts=inputs,software=[dict(name='simulationPython',version=platform.python_version()),dict(name='numpy',version=np.__version__),dict(name='scipy',version=scipy.__version__)],
        randomness=dict(used=True,generator='scrambledscipySobol initialphases; PCG64 sequentialelasticpairdraws',seed=arguments[arguments.index('--seed')+1] if '--seed' in arguments else 87319))
    folder=HERE/'contracts';folder.mkdir(exist_ok=True);path=folder/(name+'.json')
    path.write_text(json.dumps(contract,indent=2)+'\n')
    output=REL/('run_'+name)
    command=[RUNNER,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(path),'--output',str(output),
             '--timeout',str(timeout),'--max-cpu-seconds',str(timeout*5),'--max-threads','4','--max-output-bytes','2097152']
    for f in inputs:command+=['--input',f]
    for f in ('initial.npz','final.npz','trajectory.npz','results.json'):
        command+=['--result',str(output/f)]
    command+=['--','nice','-n','19','/usr/bin/python3',str(REL/'run_resolution.py'),'--output',str(output)]+arguments
    print(json.dumps(dict(case=name,argv=command)),flush=True)
    return subprocess.call(command)


if __name__=='__main__':
    p=argparse.ArgumentParser(allow_abbrev=False);p.add_argument('--case',required=True);p.add_argument('--timeout',type=int,default=7200)
    args,rest=p.parse_known_args()
    raise SystemExit(launch(args.case,rest,args.timeout))
