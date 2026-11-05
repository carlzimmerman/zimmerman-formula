#!/usr/bin/env python3
"""Mock-input integrity and ungraded fit pilots; not KA1/KA2 acceptance."""
import argparse,copy,json,os,shutil,subprocess,sys
from pathlib import Path
import raw_cube as R
import io_beam as B
parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
root=R.HERE/args.tag
if root.exists():raise RuntimeError('Fresh tag required')
root.mkdir(parents=True);checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
base=[sys.executable,'-W','error',str(R.HERE/'fit_unit.py'),'--prepared','prepare_verified/baseline/NA_bin8','--model','free','--budget','2','--start-inc','35']
source=R.HERE/'mock_verified/contract_a/NA_canonical_law';slow=R.HERE/'mock_verified/contract_a/NA_canonical_slow'
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
def run(name,extra):
 command=base+['--tag',str((root/name).relative_to(R.HERE))]+extra
 result=subprocess.run(command,capture_output=True,text=True,env=env)
 (root/(name+'.log')).write_text(result.stdout+result.stderr)
 return result
for dataset,directory in [('ka1',source),('ka2',slow)]:
 result=run(dataset,['--dataset',dataset,'--mock-source',str(directory.relative_to(R.HERE))])
 check(dataset+'_fit_unit_completes',result.returncode==0)
 obj=json.loads((root/dataset/'result.json').read_text())
 check(dataset+'_mock_identity_retained',obj['identity']['mock_manifest_sha256']==R.sha(directory/'mock_manifest.json') and obj['identity']['arguments']['dataset']==dataset)
 check(dataset+'_pilot_not_accepted',not obj['fit']['optimizer_accepted'] and obj['fit']['budget']==2)
for name,extra,error in [
 ('missing',['--dataset','ka1'],'Mock dataset requires'),
 ('wrong_foot',['--dataset','ka1','--foot','alt','--mock-source',str(source.relative_to(R.HERE))],'Mock preparation/footing/type mismatch'),
 ('wrong_type',['--dataset','ka1','--mock-source',str(slow.relative_to(R.HERE))],'Mock preparation/footing/type mismatch'),
 ('real_with_mock',['--mock-source',str(source.relative_to(R.HERE))],'Mock source supplied')]:
 result=run(name,extra);check(name+'_rejected',result.returncode!=0 and error in result.stderr)
original=json.loads((source/'mock_manifest.json').read_text())
stale=copy.deepcopy(original);name=next(iter(stale['identity']['source_hashes']));stale['identity']['source_hashes'][name]='0'*64
stale_dir=root/'stale_mock';stale_dir.mkdir();B.atomic(stale_dir/'mock_manifest.json',stale)
result=run('stale',['--dataset','ka1','--mock-source',str(stale_dir.relative_to(R.HERE))]);check('stale_mock_engine_rejected',result.returncode!=0 and 'Stale mock engine' in result.stderr)
tampered=copy.deepcopy(original);name=next(iter(tampered['stages']['signal']['outputs']));tampered['stages']['signal']['outputs'][name]='0'*64
tampered_dir=root/'tampered_mock';tampered_dir.mkdir();shutil.copyfile(source/name,tampered_dir/name);B.atomic(tampered_dir/'mock_manifest.json',tampered)
result=run('tampered',['--dataset','ka1','--mock-source',str(tampered_dir.relative_to(R.HERE))]);check('changed_mock_array_rejected',result.returncode!=0 and 'Changed mock array' in result.stderr)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in [Path(__file__),R.HERE/'fit_unit.py']},scope='Mock integrity and two-evaluation NA canonical free-model pilots only; no frozen KA1/KA2 acceptance or convergence verdict')
B.atomic(root/'checks.json',obj);print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
