"""Build separately pinned order5 vector-constructor fix, preserving upstream."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    here=Path(__file__).resolve().parent;source=here.parent/'vendor'/'pyfalcon_d2e2e05_order5fix'
    target=Path(a.output).resolve();target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():raise RuntimeError('refuse to replace compiled evidence')
    files=[source/'src'/'src'/name for name in ('exception.cc','numerics.cc','basic.cc','body.cc','gravity.cc','kernel.cc','tree.cc')]
    command=['clang++','-O3','-std=c++11','-ffp-contract=off','-fPIC','-dynamiclib',
        '-Wno-deprecated-register','-DfalcON_DOUBLE','-DfalcON_ORDER=5',
        '-I'+str(source/'src'/'inc'),'-I'+str(source/'src'/'inc'/'utils'),str(here/'falcon_cabi.cc'),
        *map(str,files),'-o',str(target)]
    start=time.monotonic();subprocess.run(command,check=True,timeout=540)
    result=dict(order=5,command=command,wall_seconds=time.monotonic()-start,
        upstream_commit='d2e2e05acb377d21b9a87d94aa8b283f52f39fca',
        patch_provenance=json.loads((source/'PATCH_PROVENANCE.json').read_text()),
        license='GPL-2.0-or-later',library=str(target),library_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    target.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
