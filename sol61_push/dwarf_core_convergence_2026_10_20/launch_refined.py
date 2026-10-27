"""Fresh, bounded, versioned common-initial-state refinement records."""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess

import numpy as np
import scipy

import run_refined
from refined_initial import load_initial

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REL = HERE.relative_to(ROOT)
SKILL = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
RUNNER = '/opt/homebrew/bin/python3.12'
WORKER = '/usr/bin/python3'


def prepare_launch(name, arguments, timeout=14400):
    """Build a reviewable argv and complete input closure without launching."""
    if not name or not name.replace('_','').isalnum():
        raise ValueError('simple nonempty case name required')
    output = HERE/('run_'+name)
    if output.exists():
        raise FileExistsError('record exists; choose a new case name')
    if timeout <= 0:
        raise ValueError('positive bounded timeout required')
    if any(arg=='--output' or arg.startswith('--output=') for arg in arguments):
        raise ValueError('output is owned by the launcher; do not pass --output')
    args = run_refined.parser().parse_args(['--output',str(output)]+list(arguments))
    if Path(args.output).resolve() != output:
        raise ValueError('output is owned by the launcher; do not pass --output')
    run_refined.validate_args(args)
    initial = Path(args.initial).resolve()
    # The worker runs from ROOT, while the launcher may be invoked from HERE.
    worker_arguments = list(arguments)
    if '--initial' in worker_arguments:
        worker_arguments[worker_arguments.index('--initial')+1] = str(initial)
    else:
        worker_arguments = [('--initial='+str(initial)) if arg.startswith('--initial=') else arg
                            for arg in worker_arguments]
    _,_,m,_,ic = load_initial(initial,args.ncold,args.seed)
    files = ['CONTRACT.md','SAMPLER_AND_PRECISION.md','REFINED_NUMERICAL_BUDGET.md',
             'evolution.py','run_resolution.py','run_production.py','refined_initial.py',
             'refined_core.py','run_refined.py','launch_refined.py','test_refined_runner.py',
             'test_refined_initial.py','profile_diagnostics.py','test_profile_diagnostics.py',
             'null_scatter.py','test_null_scatter.py','fast_gravity.py','fast_gravity.c',
             'test_fast_gravity.py','test_evolution.py','test_resolution_driver.py']
    inputs = [str(REL/f) for f in files]
    libraries = {'fast': 'FAST_GRAVITY_LIBRARY'}
    if args.backend != 'cpu':
        files = ['metal_gravity.py','metal_gravity.mm','test_metal_gravity.py']
        inputs += [str(REL/f) for f in files]
        libraries['metal'] = 'METAL_GRAVITY_LIBRARY'
    if args.backend in run_refined.CANDIDATE_BACKENDS:
        inputs += [str(REL/(args.backend+'_gravity'+suffix)) for suffix in ('.py','.mm')]
        inputs.append(str(REL/('test_'+args.backend+'_gravity.py')))
        libraries[args.backend] = args.backend.upper()+'_GRAVITY_LIBRARY'
    selected_libraries = {}
    for key,env in libraries.items():
        library = Path(os.environ.get(env,HERE/(key+'_gravity.dylib'))).resolve()
        inputs.append(str(library.relative_to(ROOT)))
        selected_libraries[env] = str(library)
    old = REL.parent/'isolated_host_dwarf_2026_10_19'
    inputs += [str(old/f) for f in ('dynamics.py','direct_gravity.c','direct_gravity.dylib',
                                   'remnant.py','CONTRACT.md','source_inputs.json')]
    inputs += ['sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md',
               str(initial.relative_to(ROOT)),str(initial.with_name('initial_metadata.json').relative_to(ROOT))]
    inputs = list(dict.fromkeys(inputs))
    candidate = args.backend in run_refined.CANDIDATE_BACKENDS
    domain = ('Separately declared FP32-interaction candidate: force L2<5e-7, per-particle max<2e-6, phi max/U<5e-7; not inherited DS1e-11 admission'
              if candidate else 'Native binary64 direct reference' if args.backend=='cpu'
              else 'Declared DS-expansion direct reference with full CPU1e-11 gates in bounded N range')
    contract = dict(claim_id='DWARF_FIXED_STATE_'+name,
        mathematics=dict(
            assertion_tested='Finite common-initial-state full3D Plummer/H4/CTMC refinement with profile, remnant and E/vectorJ/host-work ledgers',
            coefficient_domain=domain,
            conventions='pc,Msun,Myr; fixed saved phase-space arrays, no velocity renormalization; no inserted core or imposed dynamical symmetry; analytic fixed host; all particles retained',
            inputs=['REFINED_NUMERICAL_BUDGET.md',list(arguments)],
            bounds=dict(argv=worker_arguments,requested_argv=list(arguments),wall_seconds=timeout,max_CPU_threads=args.threads,
                        ncold=args.ncold,loaded_total_particles=len(m),initial_seed=args.seed,
                        collision_seed=args.collision_seed if args.collision_seed is not None else args.seed+1000000,
                        initial_relative_state_sha256=ic['relative_state_sha256'],dt_Myr=args.dt,
                        softening_pc=args.eps,collision_support_pc=args.h,selected_backend=args.backend,
                        precision_check_gravity_calls=list(run_refined.CHECKPOINTS),
                        full_CPU_reference_N_limit=run_refined.CPU_REFERENCE_LIMIT),
            non_claims=['Finite completion is not physical convergence',
                        'Candidate force budget is separate from DS admission and does not certify accumulated trajectory error',
                        'No source-derived initial state, response-field dynamics, imposed cold core or live host absorption',
                        'Conditional count intervals exclude temporal, ensemble, centring and model uncertainty',
                        'Instantaneous self-boundness does not guarantee tidal survival']),
        execution_artifacts=inputs,
        software=[dict(name='launcherPython',version=platform.python_version()),
                  dict(name='launcherNumpy',version=np.__version__),dict(name='launcherScipy',version=scipy.__version__),
                  dict(name='simulationPython',version=WORKER+'; actual worker versions recorded at runtime')],
        randomness=dict(used=not args.collisionless,generator='PCG64 frozen-position central-pair CTMC; initial phases loaded from saved bytes',
                        seed=args.collision_seed if args.collision_seed is not None else args.seed+1000000))
    contract_path = HERE/'contracts'/('refined_'+name+'.json')
    if contract_path.exists():
        raise FileExistsError('refined contract already exists; choose a new case name')
    output_rel = output.relative_to(ROOT)
    command = [RUNNER,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
               '--contract',str(contract_path),'--output',str(output_rel),'--timeout',str(timeout),
               '--max-cpu-seconds',str(timeout*5),'--max-threads',str(args.threads),'--max-output-bytes','2097152']
    for path in inputs:
        command += ['--input',path]
    for name_result in ('initial.npz','final.npz','trajectory.npz','results.json','precision_checks.json'):
        command += ['--result',str(output_rel/name_result)]
    # Explicit env arguments pin the same binaries that the input closure hashed.
    command += ['--','nice','-n','19','env']+[key+'='+value for key,value in selected_libraries.items()]
    command += [WORKER,str(REL/'run_refined.py'),'--output',str(output_rel)]+worker_arguments
    return dict(inputs=inputs,contract=contract,contract_path=contract_path,command=command,
                case=name,output=output,selected_libraries=selected_libraries)


def launch(name,arguments,timeout=14400):
    spec = prepare_launch(name,arguments,timeout)
    missing = [path for path in spec['inputs'] if not (ROOT/path).is_file()]
    if missing:
        raise FileNotFoundError('Missing frozen input(s): '+str(missing))
    spec['contract_path'].parent.mkdir(exist_ok=True)
    spec['contract_path'].write_text(json.dumps(spec['contract'],indent=2)+'\n')
    print(json.dumps(dict(case=name,argv=spec['command'])),flush=True)
    return subprocess.call(spec['command'],cwd=ROOT)


if __name__ == '__main__':
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--case',required=True)
    p.add_argument('--timeout',type=int,default=14400)
    args,rest = p.parse_known_args()
    raise SystemExit(launch(args.case,rest,args.timeout))
