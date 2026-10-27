"""Run only reviewed, hash-pinned evaluators. Generated Python is never executed."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid
import shutil
import resource
import math

from engine import pinned_bytes, sha, validate_contract

def sandbox_command(argv, directory, extra_reads=()):
    """macOS seatbelt: generated code can write only scratch and cannot use the network."""
    binary = shutil.which('sandbox-exec')
    if sys.platform != 'darwin' or not binary:
        raise ValueError('Generated execution requires macOS sandbox-exec on this installation')
    q = lambda p: json.dumps(str(Path(p).resolve()))
    profile = ('(version 1)(allow default)(deny network*)(deny file-write*)(deny process-fork)(deny signal)'
               '(deny file-read*)(allow file-read-metadata)'
               '(allow file-read* (literal "/") (subpath "/System") (subpath "/Library") (subpath "/usr")'
               ' (subpath "/bin") (subpath "/opt") (subpath "/private/etc")'
               ' (subpath "/private/var/db") (subpath "/dev"))'
               '(allow file-write* (subpath '+q(directory)+') (literal "/dev/null"))'
               '(allow file-read* (subpath '+q(directory)+') (subpath '+q(sys.prefix)+')'+
               ''.join(' (subpath '+q(p)+')' for p in extra_reads)+')')
    return [binary, '-p', profile, *argv]

def run_process(argv, cwd, env, timeout, prefix):
    """Preserve logs on disk, bound output and kill the process group on timeout."""
    prefix = Path(prefix)
    stdout, stderr = prefix.with_suffix('.stdout'), prefix.with_suffix('.stderr')
    start, reason = time.monotonic(), None
    with stdout.open('xb') as out, stderr.open('xb') as err:
        def limits():
            cpu = math.ceil(timeout)+2
            resource.setrlimit(resource.RLIMIT_CPU, (cpu,cpu+1))
            resource.setrlimit(resource.RLIMIT_FSIZE, (64*1024*1024,64*1024*1024))
            resource.setrlimit(resource.RLIMIT_NOFILE, (256,256))
            resource.setrlimit(resource.RLIMIT_CORE, (0,0))
            try: resource.setrlimit(resource.RLIMIT_AS, (12*1024**3,12*1024**3))
            except (ValueError, OSError): pass  # macOS may not enforce virtual-address limits
        p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=out, stderr=err,
                             start_new_session=True, preexec_fn=limits)
        try:
            while p.poll() is None:
                if time.monotonic() - start > timeout:
                    reason = 'timeout'; break
                if stdout.stat().st_size + stderr.stat().st_size > 4 * 1024 * 1024:
                    reason = 'output_limit'; break
                time.sleep(0.025)
        finally:
            try: os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            p.wait()
    if stdout.stat().st_size + stderr.stat().st_size > 4 * 1024 * 1024: reason = 'output_limit'
    return {'exit': p.returncode, 'complete': reason is None and p.returncode == 0,
            'error': reason, 'seconds': round(time.monotonic()-start, 3),
            'stdout': stdout.name, 'stderr': stderr.name}

def environment(directory):
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'PYTHONUNBUFFERED': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[key] = '1'
    env.update(TMPDIR=str(directory), MPLCONFIGDIR=str(Path(directory)/'matplotlib'))
    return env

def payload(path, required):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result: raise ValueError('Duplicate JSON key')
            result[k] = v
        return result
    v = json.loads(Path(path).read_text(), object_pairs_hook=unique,
                   parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))
    if not isinstance(v, dict) or v.get('protocol') != 2 or v.get('complete') is not True:
        raise ValueError('Evaluator did not complete protocol 2')
    checks = v.get('checks', {})
    if not isinstance(checks, dict) or not all(k in checks and type(checks[k]) is bool for k in required):
        raise ValueError('Missing or non-boolean required checks')
    return v

def evaluate(contract, work):
    validate_contract(contract)
    if contract['kind'] not in ('evaluator', 'exploration'): raise ValueError('Not an evaluator contract')
    work = Path(work).resolve(); work.mkdir(parents=True, exist_ok=True)
    source = pinned_bytes(contract['evaluator'])
    inputs = [(x, pinned_bytes(x)) for x in contract.get('inputs', [])]
    required, results = contract['required_checks'], {}
    for mode in ('main', 'positive', 'negative'):
        directory = work/(mode+'-'+uuid.uuid4().hex); directory.mkdir()
        script = directory/'evaluator.py'; script.write_bytes(source)
        manifest, original = {}, {script: sha(source)}
        for idx, (item, data) in enumerate(inputs):
            dest = directory/(f'input-{idx}'+Path(item['path']).suffix)
            dest.write_bytes(data); original[dest] = sha(data)
            manifest[item['name']] = str(dest)
        mp = directory/'inputs.json'; mp.write_text(json.dumps(manifest)); original[mp] = sha(mp.read_bytes())
        env = environment(directory); env.update(ORCH_MODE=mode, ORCH_INPUTS=str(mp))
        try:
            argv = [sys.executable, '-B', str(script)]
            if contract['kind'] == 'exploration': argv = sandbox_command(argv, directory)
            r = run_process(argv, directory, env,
                            min(1800, max(1, float(contract.get('timeout_s', 120)))), directory/'process')
            results[mode] = dict(r, directory=directory.name)
            if not r['complete']: raise ValueError(f'Execution incomplete: exit={r["exit"]}, {r["error"]}')
            if any(not p.exists() or sha(p.read_bytes()) != h for p, h in original.items()):
                raise ValueError('Evaluator changed its pinned code or input')
            results[mode]['payload'] = payload(directory/r['stdout'], required)
        except (ValueError, OSError, TypeError) as e:
            return {'validity': 'invalid', 'outcome': 'inconclusive', 'reason': f'{mode}: {e}', 'runs': results}
    pos, neg = results['positive']['payload']['checks'], results['negative']['payload']['checks']
    if not all(pos[k] for k in required) or any(neg[k] for k in contract['negative_checks']):
        return {'validity': 'invalid', 'outcome': 'inconclusive', 'reason': 'Control expectations not met',
                'control_failures': {'positive_expected_true': [k for k in required if not pos[k]],
                                     'negative_expected_false': [k for k in contract['negative_checks'] if neg[k]]},
                'runs': results}
    main = results['main']['payload']['checks']
    return {'validity': 'candidate_checked' if contract['kind'] == 'exploration' else 'checked',
            'outcome': 'supported' if all(main[k] for k in required) else 'rejected',
            'runs': results, 'scope': 'Frozen evaluator and controls completed; scientific interpretation needs review.'}
