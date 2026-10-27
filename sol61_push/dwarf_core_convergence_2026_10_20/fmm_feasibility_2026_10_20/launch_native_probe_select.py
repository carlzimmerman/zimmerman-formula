"""Record one explicitly bounded native FMM probe using the audit runner."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--shape',required=True)
    p.add_argument('--n',type=int,required=True);p.add_argument('--tag',required=True)
    p.add_argument('--tolerances',type=float,nargs='+',required=True)
    args=p.parse_args();relative=HERE.relative_to(ROOT)
    inputs=[relative/'launch_native_probe_select.py',relative/'native_probe_select.py',relative/'native_fmm.py',
            relative/'native_build_003/libfmm3d.dylib']
    if args.shape!='gaussian':inputs.append(relative.parent/'run_pilot_gpu8k_iso/final.npz')
    c=dict(claim_id='FMM_NATIVE_'+args.tag,mathematics=dict(
        assertion_tested='Finite native ARM OpenMP4 raw-Laplace timings, 64 source-target direct comparisons including central sources, whole-population momentum/torque residuals.',
        coefficient_domain='IEEE binary64; approximate FMM, independently summed ordered NumPy reference',
        conventions='Unsoftened isolated3D; source self excluded; G=.004498638185693768; requested tolerance is not a certified perparticle error.',
        inputs=[args.shape+' '+str(args.n)],bounds=dict(N=args.n,source_target_comparisons_at_most=64,tolerances=args.tolerances),
        non_claims=['No evolution or finiteepsilon kernel change','No uniform error bound or highN complete direct comparison','Synthetic resampled_saved geometry is not a highN evolved state']),
        execution_artifacts=[str(i) for i in inputs],software=[dict(name='Python',version='3.9.6'),dict(name='NumPy',version='1.26.2'),dict(name='FMM3Dnative',version='2.1.0 local GNU15.2 OpenMP4 FAST_KER')],randomness=dict(used=True,generator='NumPy PCG64',seed=20261021))
    contract=HERE/('contract_'+args.tag+'.json');contract.write_text(json.dumps(c,indent=2)+'\n')
    run=relative/('native_'+args.tag)
    command=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(ROOT),'--contract',str(contract)]
    for i in inputs:command+=['--input',str(i)]
    command+=['--output',str(run),'--result',str(run/'results.json'),'--timeout','60','--max-output-bytes','1000000','--max-cpu-seconds','55','--max-threads','4','--',sys.executable,str(relative/'native_probe_select.py'),'--shape',args.shape,'--n',str(args.n),'--output',str(run/'results.json')]
    command+=['--tolerances']+[str(t) for t in args.tolerances]
    raise SystemExit(subprocess.call(command,cwd=ROOT))


if __name__=='__main__':main()
