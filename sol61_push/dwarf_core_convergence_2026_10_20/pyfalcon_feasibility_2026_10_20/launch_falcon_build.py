"""Create a bounded, hash-pinned build record below the new vendor tree."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    p=argparse.ArgumentParser();p.add_argument('--order',type=int,choices=(3,5,6),required=True)
    a=p.parse_args(); here=Path(__file__).resolve().parent
    root=here.parents[2]; source=here.parent/'vendor'/'pyfalcon_d2e2e05'
    paths=[here/'build_falcon.py',here/'falcon_cabi.cc',here/'falcon_native.py',here/'test_falcon_native.py']
    paths += sorted(f for f in source.rglob('*') if f.is_file() and '.git' not in f.relative_to(source).parts)
    relative=[str(f.relative_to(root)) for f in paths]
    output=here.parent/'vendor'/f'falcon_double_order{a.order}_build_001'
    reloutput=str(output.relative_to(root)); library=reloutput+'/libfalcon.dylib'
    contract=here/f'build_order{a.order}_contract.json'
    if contract.exists():raise RuntimeError('refuse to replace build contract')
    contract.write_text(json.dumps(dict(claim_id=f'FALCON_DOUBLE_P0_ORDER{a.order}_BUILD',
        mathematics=dict(assertion_tested='Build unmodified official source with native binary64 real and hardcodedP0Plummer C ABI',
            coefficient_domain='C++11 binary64 scalar full3D falcON',conventions='no float/defaultP1,no fastmath,no source changes',
            inputs=['official source commitd2e2e05acb377d21b9a87d94aa8b283f52f39fca'],
            bounds=dict(expansion_order=a.order,wall_seconds=600,cpu_seconds=540),
            non_claims=['Build success does not establish forceaccuracy,conservation,or trajectory convergence']),
        execution_artifacts=relative,
        software=[dict(name='computation Python',version='3.9.6'),dict(name='Apple clang',version='21.0.0 (clang-2100.1.1.101)')],
        randomness=dict(used=False,generator='none',seed=None)),indent=2)+'\n')
    skill=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
    command=[sys.executable,str(skill/'scripts'/'run_experiment.py'),'--root',str(root),
        '--contract',str(contract),'--output',reloutput,'--result',library,'--result',reloutput+'/libfalcon.json',
        '--timeout','600','--max-cpu-seconds','540','--max-threads','1','--max-output-bytes','1048576']
    for path in relative:command += ['--input',path]
    command += ['--',sys.executable,str(here/'build_falcon.py'),'--order',str(a.order),'--output',library]
    subprocess.run(command,cwd=root,check=True)


if __name__=='__main__':main()
