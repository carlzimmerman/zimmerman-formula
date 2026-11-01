"""Compile only the new adapter through the already installed cached toolchain."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys

ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
root=Path(__file__).resolve().parents[3]
adapter=Path(__file__).with_name('LawDictionary.lean')
cmd=['lake','env','lean',str(adapter)]
p=subprocess.run(cmd,cwd=root/'fable_independent_2026/lean_2026',text=True,capture_output=True,timeout=45)
print(p.stdout,end='');print(p.stderr,file=sys.stderr,end='')
result={'argv':cmd,'cwd':'fable_independent_2026/lean_2026','returncode':p.returncode,
        'checks':{'exit_zero':p.returncode==0,'no_sorryAx':'sorryAx' not in p.stdout+p.stderr},
        'scope':'Only TP01 LawDictionary.lean; no pre-existing certificate or entire library recompiled',
        'peak_child_RSS_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'stdout':p.stdout,'stderr':p.stderr}
result['checks']['observed_RSS_below_1GB']=result['peak_child_RSS_bytes']<1073741824
Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
assert all(result['checks'].values())
