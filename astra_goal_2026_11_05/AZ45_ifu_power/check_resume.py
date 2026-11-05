#!/usr/bin/env python3
"""Small contract check; no production grid. Outputs belong to AZ45."""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));import engine as E
args=[sys.executable,str(P/'worker.py'),'--template','0','--rung','2','--foot','canonical','--mode','reference']
key='t00_r2_canonical_n0_flat_s30_free_reference_0.01.json'
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='contract_interrupted');options=ap.parse_args()
tag=options.tag;out=P/tag/'reference'/key
if out.exists():raise RuntimeError('Use existing contract result; refusing to overwrite fresh-run evidence')
with (P/'contract_interrupt.log').open('w') as f:
    child=subprocess.Popen(args+['--tag',tag],stdout=f,stderr=subprocess.STDOUT)
    time.sleep(1.)
    live=child.poll() is None
    if live:child.send_signal(signal.SIGTERM)
    code=child.wait(timeout=60)
checkpoint=out.with_suffix('.checkpoint.json')
if code!=75 or not checkpoint.exists():raise RuntimeError('SIGTERM contract failed: '+str(code))
with (P/'contract_resume.log').open('w') as f:res=subprocess.run(args+['--tag',tag,'--resume'],stdout=f,stderr=subprocess.STDOUT,timeout=240)
with (P/'contract_idempotent.log').open('w') as f:again=subprocess.run(args+['--tag',tag,'--resume'],stdout=f,stderr=subprocess.STDOUT,timeout=30)
baseline=P/'pilot/reference'/key
same=baseline.read_bytes()==out.read_bytes()
result=dict(interrupted_while_live=live,interrupted_exit=code,checkpoint_exists=checkpoint.exists(),resume_exit=res.returncode,
            completed_resume_exit=again.returncode,byte_identical_scientific_file=same,
            sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_hashes=E.hashes())
E.atomic(P/'resume_contract.json',result);print(json.dumps(result,indent=2))
raise SystemExit(int(not(live and code==75 and res.returncode==0 and again.returncode==0 and same)))
