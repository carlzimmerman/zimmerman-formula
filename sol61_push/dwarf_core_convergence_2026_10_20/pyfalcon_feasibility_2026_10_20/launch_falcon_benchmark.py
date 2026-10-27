"""Record one<=60s native falcON full3D force/cost probe; no dynamics."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    p=argparse.ArgumentParser();p.add_argument('--order',type=int,choices=(3,5,6),required=True)
    a=p.parse_args();here=Path(__file__).resolve().parent;root=here.parents[2]
    library=here.parent/'vendor'/f'falcon_double_order{a.order}_build_001'/'libfalcon.dylib'
    paths=[here/'benchmark_falcon.py',here/'falcon_native.py',here/'falcon_cabi.cc',here/'test_falcon_native.py',
           here.parent/'fast_gravity.py',here.parent/'fast_gravity.c',here.parent/'fast_gravity.dylib',
           here.parent/'run_pilot_gpu8k_iso'/'final.npz',here.parent/'run_pilot_gpu8k_iso'/'results.json',library]
    relative=[str(f.relative_to(root)) for f in paths]
    contract=here/f'benchmark_order{a.order}_contract.json'
    if contract.exists():raise RuntimeError('refuse to replace benchmark contract')
    contract.write_text(json.dumps(dict(claim_id=f'FALCON_DOUBLE_P0_ORDER{a.order}_FEASIBILITY',
        mathematics=dict(assertion_tested='Compare full3D binary64 mutual-cell P0 Plummer force/phi to direct reference at three opening angles and two evolved/dynamic-range geometries, then sample128 direct targets atN65536 and262144; record full-system linear/vector-angular force defects and runtime.',
            coefficient_domain='IEEE754 binary64,approximate Cartesian Taylor tree with compiletimeorder',
            conventions='G=.004498638185693768 pc3/Msun/Myr2; P0Plummer epsilon10pc; allactive; no spherical symmetry or per-backend IC renormalization',
            inputs=['CompletedGPU8k1-Gyr final phase space','Synthetic full3D dense+far-tail geometry and distortedPlummer/tail timing sets'],
            bounds=dict(theta=[.3,.5,.7],synthetic_N=[65536,262144],largeN_reference_targets=128,
                initial_force_L2_target=1e-5,wall_cap_seconds=60,cpu_cap_seconds=55),
            non_claims=['No trajectory,profile,or remnant convergence','Theta is not a rigorousuniform tolerance',
                'LargeN references128 targets,not fullN or exactglobalenergy',
                'NativeFP64 reference roundoff and approximate-force errors are separate budgets']),
        execution_artifacts=relative,software=[dict(name='computation Python',version='3.9.6'),dict(name='numpy',version='1.26.2')],
        randomness=dict(used=True,generator='numpy.default_rng PCG64',seed=71504)),indent=2)+'\n')
    output=here/f'benchmark_order{a.order}_run_001';reloutput=str(output.relative_to(root))
    result=reloutput+'/results.json'
    skill=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
    command=[sys.executable,str(skill/'scripts'/'run_experiment.py'),'--root',str(root),'--contract',str(contract),
        '--output',reloutput,'--result',result,'--timeout','60','--max-cpu-seconds','55',
        '--max-threads','1','--max-output-bytes','1048576']
    for path in relative:command+=['--input',path]
    command+=['--',sys.executable,str(here/'benchmark_falcon.py'),'--library',str(library),'--output',result]
    subprocess.run(command,cwd=root,check=True)


if __name__=='__main__':main()
