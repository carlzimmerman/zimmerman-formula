#!/usr/bin/env python3
"""Content-pinned bounded runner; deliberately performs no Git operation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

p = Path('fine_structure_puzzle/qcd_sea_curvature/sea_ope')
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
out = Path(args.output)
out.mkdir(exist_ok=False)
contract = json.loads((p/'COMPUTATION_CONTRACT.json').read_text())
paths = contract['execution_artifacts']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (10, 10))

before = {x:digest(x) for x in paths}
argv = [sys.executable,str(p/'compute_uv.py'),'--inputs',str(p/'INPUTS.json'),
        '--output',str(out/'result.json')]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
run = subprocess.run(argv,capture_output=True,text=True,timeout=30,
                     preexec_fn=limits,env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
elapsed = time.monotonic()-t
(out/'stdout.txt').write_text(run.stdout)
(out/'stderr.txt').write_text(run.stderr)
after = {x:digest(x) for x in paths}
status = 'completed' if run.returncode == 0 else 'failed'
if before != after:
    status = 'inputs-changed'
outputs = [{'path':str(out/x),'sha256':digest(out/x),
            'kind':'result' if x == 'result.json' else 'log'}
           for x in ['stdout.txt','stderr.txt','result.json'] if (out/x).exists()]
manifest = {
    'schema_version':2,'claim_id':contract['claim_id'],
    'repository':{'commit':'unavailable: Git not inspected under task restrictions',
                  'dirty':True,'dirty_note':'Conservative true; not a Git observation. Content hashes are authoritative.'},
    'command':argv,'environment':{'software':[{'name':'Python','version':platform.python_version()}],
                                'hardware':platform.platform()},
    'mathematics':contract['mathematics'],'randomness':contract['randomness'],
    'run':{'started_at':started,'runtime_seconds':elapsed,'exit_status':run.returncode,
           'status':status,'timeout_seconds':30,
           'resource_limits':{'memory_bytes':None,'cpu_seconds':10,'max_cores':None,'max_threads':1}},
    'outputs':outputs,
    'checks':[{'name':'input_hashes_unchanged','passed':before == after},
              {'name':'child_exit_zero','passed':run.returncode == 0}],
    'result':'Finite algebra completed' if run.returncode == 0 else 'Inspect stderr',
    'residual_risks':['Git revision/dirty state not inspected; dirty=true is a conservative placeholder.',
                      'Memory cap unavailable on macOS; bounded small matrices and CPU/wall limits used.',
                      'OPE convergence and nonperturbative matrix elements are outside finite assertion.',
                      'Thread environment may be ignored; computation is single-threaded stdlib.'],
    'input_artifacts':[{'path':x,'sha256':before[x],'sha256_after':after[x]} for x in paths],
    'execution_artifacts':paths,'declared_results':[str(out/'result.json')],
    'output_directory':str(out)}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(run.stdout)
print(run.stderr)
print('run.status='+status)
sys.exit(run.returncode)
