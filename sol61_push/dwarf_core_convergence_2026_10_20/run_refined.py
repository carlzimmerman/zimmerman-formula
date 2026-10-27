"""Fixed-common-state H4/CTMC runs with explicitly separate force budgets."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import argparse
import importlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy

import refined_core as core

CHECKPOINTS = (1, 2, 100, 1000, 6000, 30000, 60000, 120000, 240000)
CPU_REFERENCE_LIMIT = 32768
CANDIDATE_BACKENDS = ('mixed','tile','tile2')


def parser():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--initial', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--ncold', type=int, required=True)
    p.add_argument('--seed', type=int, default=87319)
    p.add_argument('--collision-seed', type=int)
    p.add_argument('--eps', type=float, default=10.)
    p.add_argument('--h', type=float, default=25.)
    p.add_argument('--dt', type=float, default=.25)
    p.add_argument('--duration', type=float, default=10000.)
    p.add_argument('--record-interval', type=float, default=10.)
    p.add_argument('--host', action='store_true')
    p.add_argument('--collisionless', action='store_true')
    p.add_argument('--threads', type=int, default=4)
    p.add_argument('--backend', choices=('cpu', 'metal', 'mixed', 'tile', 'tile2'), default='cpu')
    p.add_argument('--collision-method', choices=('ctmc',), default='ctmc')
    return p


def validate_args(args):
    if args.ncold < 16 or args.ncold & (args.ncold-1):
        raise ValueError('ncold must be a power of two >=16 with ncold/8 stars')
    if not 1 <= args.threads <= 4:
        raise ValueError('one to four CPU threads required')
    if (not all(np.isfinite(z) for z in (args.eps, args.h, args.dt, args.duration, args.record_interval))
            or args.eps < 0 or min(args.h, args.dt, args.duration, args.record_interval) <= 0):
        raise ValueError('finite eps>=0 and positive h, dt, duration, record interval required')
    for value in (args.duration, args.record_interval):
        if abs(round(value/args.dt)*args.dt-value) > 1e-9:
            raise ValueError('duration and record interval must be integer multiples of dt')


def precision_budget(backend):
    if backend in CANDIDATE_BACKENDS:
        return dict(name='separate_FP32_interaction_candidate_budget',
                    force_relative_L2=5e-7, force_relative_max=2e-6,
                    phi_relative_max=5e-7, potential_energy_relative=5e-7,
                    inherited_DS_1e_minus11_budget=False,
                    scope='empirical same-state admission only; independent trajectory/profile/invariant controls still required')
    if backend == 'metal':
        return dict(name='existing_DS_same_state_budget', force_relative_L2=1e-11,
                    phi_relative_L2=1e-11, potential_energy_relative=1e-11,
                    scope='independent full native CPU checks only when supplied total N<=32768')
    return dict(name='native_binary64_direct_reference',
                scope='same softened all-pairs law; analytical and independent implementation tests, no GPU candidate budget')


def precision_metrics(answer, reference):
    a, U, phi = answer
    b, V, psi = reference
    delta = np.asarray(a)-b
    local = np.linalg.norm(b, axis=1)
    error = np.linalg.norm(delta, axis=1)
    tiny = 1.e-300
    return dict(force_relative_L2=float(np.linalg.norm(delta)/max(np.linalg.norm(b), tiny)),
                force_relative_max=float(np.max(error/np.maximum(local, tiny))),
                force_max_absolute_normalized=float(np.max(error)/max(np.max(local), tiny)),
                force_global_normalization='maximum reference particle acceleration magnitude',
                phi_relative_L2=float(np.linalg.norm(np.asarray(phi)-psi)/max(np.linalg.norm(psi), tiny)),
                phi_relative_max=float(np.max(abs(np.asarray(phi)-psi)/np.maximum(abs(psi), tiny))),
                potential_energy_relative=float(abs(U-V)/max(abs(V), tiny)))


def precision_pass(metrics, backend):
    budget = precision_budget(backend)
    keys = (('force_relative_L2','force_relative_max','phi_relative_max','potential_energy_relative')
            if backend in CANDIDATE_BACKENDS else
            ('force_relative_L2','phi_relative_L2','potential_energy_relative') if backend=='metal' else ())
    return bool(keys) and all(key in metrics and np.isfinite(metrics[key]) and metrics[key] < budget[key] for key in keys)


def select_backend(args):
    if args.backend == 'cpu':
        return (lambda x,m,eps: core.cpu_gravity(x,m,eps,threads=args.threads)), core.backend_metadata()
    module = importlib.import_module(args.backend + '_gravity')
    return module.gravity, module.backend_metadata()


def main(args):
    validate_args(args)
    out = Path(args.output)
    if any((out/name).exists() for name in ('initial.npz','final.npz','trajectory.npz','results.json','progress.json','precision_checks.json')):
        raise FileExistsError('fresh refined scientific output required')
    original, metadata = select_backend(args)
    metadata = dict(metadata, selected_backend=args.backend, admission_budget=precision_budget(args.backend))
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    calls = 0
    def save_checks():
        (out/'precision_checks.json').write_text(json.dumps(dict(
            backend=metadata, scheduled_gravity_calls=list(CHECKPOINTS),
            cpu_reference_total_particle_limit=CPU_REFERENCE_LIMIT,
            evolved_state_precision_checks=checks,
            convention='gravity calls include instantaneous-unbinding diagnostics; N is recorded for every comparison'),
            indent=2, allow_nan=False)+'\n')
    save_checks()
    def checked(x,m,eps):
        nonlocal calls
        answer = original(x,m,eps)
        calls += 1
        if calls in CHECKPOINTS and args.backend != 'cpu':
            references = []
            if args.backend in CANDIDATE_BACKENDS:
                from metal_gravity import gravity as ds_reference
                references.append(('full_DS_expansion', ds_reference(x,m,eps)))
            if args.ncold*9//8 <= CPU_REFERENCE_LIMIT:
                references.append(('full_native_CPU_binary64', core.cpu_gravity(x,m,eps,threads=args.threads)))
            for name, reference in references:
                row = dict(gravity_call=calls, N=len(m), reference=name,
                           selected_backend=args.backend, **precision_metrics(answer, reference))
                row['passed'] = precision_pass(row,args.backend)
                checks.append(row)
                save_checks()
                if not row['passed']:
                    raise RuntimeError('Refined force candidate admission failed: '+str(row))
            if not references:
                checks.append(dict(gravity_call=calls, N=len(m), reference=None,
                    selected_backend=args.backend, passed=None,
                    skipped_reason='full CPU bound exceeded; no independent same-state comparison made'))
                save_checks()
        return answer
    from null_scatter import scatter as ctmc
    totals = dict(proposals=0,events=0)
    def collision(*pos,**kw):
        result = ctmc(*pos,**kw)
        totals['proposals'] += result.get('proposals',0)
        totals['events'] += result['n']
        return result
    core.simulate(args, gravity=checked, backend=metadata, scatter_operator=collision)
    path = out/'results.json'
    result = json.loads(path.read_text())
    result.update(evolved_state_precision_checks=checks, force_admission_budget=precision_budget(args.backend),
                  precision_check_schedule=list(CHECKPOINTS), gravity_call_count=calls,
                  collision_method='ctmc', null_sampler_totals=totals,
                  collision_method_convention='frozen-position central elastic CTMC; positive physical collision time',
                  common_initial_convention='exact saved arrays before optional host orbital translation; no velocity renormalization',
                  runtime_software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                  numerical_convergence='pending matched timestep, force, softening, support, N and realization controls')
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


if __name__ == '__main__':
    main(parser().parse_args())
