#!/usr/bin/env python3
"""Measure a bounded worker's macOS physical footprint, not RSS alone."""
import argparse,ctypes,json,os,subprocess,sys,time
from pathlib import Path
import audit_inputs as A
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);parser.add_argument('--stage',choices=['solve','sample'],default='solve');args=parser.parse_args()
out=A.HERE/'worker_footprint'/args.tag
if out.exists():raise RuntimeError('Use a fresh footprint tag')
out.mkdir(parents=True)
class Usage(ctypes.Structure):
 _fields_=[('uuid',ctypes.c_uint8*16)]+[(name,ctypes.c_uint64) for name in ['user_time','system_time','pkg_idle_wkups','interrupt_wkups','pageins','wired','resident','footprint','start','exit','child_user','child_system','child_pkg','child_interrupt','child_pageins','child_elapsed','read','written','qos_default','qos_maintenance','qos_background','qos_utility','qos_legacy','qos_initiated','qos_interactive','billed_system','serviced_system','logical_writes','peak','instructions','cycles','billed_energy','serviced_energy','interval_peak','runnable']]
lib=ctypes.CDLL('/usr/lib/libproc.dylib');samples=[]
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
command=[sys.executable,str(A.HERE/'worker3d.py'),'--source','bullet','--n','16','--foot','canonical','--homotopy','--tag',str((out/'run').relative_to(A.HERE))]
if args.stage=='sample':command=[sys.executable,str(A.HERE/'sample_field.py'),'--field','worker_verified/contract_d/baseline','--tag',str((out/'run').relative_to(A.HERE))]
start=time.monotonic()
with (out/'worker.log').open('w') as log:
 child=subprocess.Popen(command,env=env,stdout=log,stderr=log)
 while child.poll() is None:
  usage=Usage()
  if lib.proc_pid_rusage(child.pid,4,ctypes.byref(usage))==0:
   samples.append(dict(seconds=time.monotonic()-start,phys_footprint_bytes=usage.footprint,lifetime_peak_bytes=usage.peak,resident_bytes=usage.resident))
  time.sleep(.005)
 code=child.wait()
if code or not samples:raise RuntimeError('Footprint pilot failed or not measured')
peak=max(s['lifetime_peak_bytes'] for s in samples)
if peak<=0:raise RuntimeError('No lifetime physical footprint measurement')
result_path=out/'run'/('samples.json' if args.stage=='sample' else 'result.json');result=json.loads(result_path.read_text())
obj=dict(stage=args.stage,exit_code=code,seconds=time.monotonic()-start,samples=samples,max_lifetime_phys_footprint_bytes=peak,source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'worker3d.py',A.HERE/'newton3d.py',A.HERE/'sample_field.py',A.HERE/'sampling3d.py']},result_sha256=A.sha(result_path),status=result['status'],scope='N16 single-thread pilot memory only; production scaling remains an estimate, not a measured bound')
A.atomic(out/'measurement.json',obj)
print(json.dumps(dict(samples=len(samples),peak_GB=peak/1e9,status=result['status']),indent=2))
