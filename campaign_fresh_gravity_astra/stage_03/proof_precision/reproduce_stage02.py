"""Reproduce published finite checks; explicitly not an independent implementation."""
import argparse
import contextlib
import importlib
import io
import json
import sys
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
stage=Path(__file__).resolve().parents[2]/'stage_02'
sys.path.insert(0,str(stage))
summary={}
for name in ['measurement','optimal_weights','rar_extension','audit_checks']:
    target=args.out/name;target.mkdir()
    sys.argv=[name,'--out',str(target)]
    module=importlib.import_module(name)
    with contextlib.redirect_stdout(io.StringIO()):module.main()
    result=json.loads((target/'results.json').read_text())
    summary[name]=result
(args.out/'results.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
print('Reproduced all four stage_02 numerical modules and their assertions.')
