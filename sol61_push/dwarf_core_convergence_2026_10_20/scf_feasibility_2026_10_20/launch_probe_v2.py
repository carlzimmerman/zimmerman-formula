"""One bounded, low-priority SCF diagnostic; no production inputs are edited."""
import argparse,json,subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--script',required=True);p.add_argument('--tag',required=True)
    p.add_argument('--extra-input',action='append',default=[]);p.add_argument('args',nargs=argparse.REMAINDER);args=p.parse_args()
    relative=HERE.relative_to(ROOT)
    inputs=[relative/'launch_probe_v2.py',relative/args.script,relative/'scf_backend.py',relative/'scf_diagonal.cpp',
        relative/'vendor/native_build_002/agama.so',relative/'vendor/diagonal_build_001/scf_diagonal.dylib']
    inputs += [Path(s) for s in args.extra_input]
    if args.script=='run_structural.py':inputs.append(relative/'test_scf_backend.py')
    c=dict(claim_id='SCF_'+args.tag,mathematics=dict(assertion_tested='Finite diagnostic declared by '+args.script,
        coefficient_domain='IEEE binary64; finite Newtonian Poisson Zhao basis with complete realharmonics',
        conventions='No evolution; fixedr0/eta/fullm. COMchainrule+selfexcluded convention where declared. Own energy differsfiniteepsilonPlummer.',
        inputs=[args.script,args.args],bounds=dict(wall_seconds=60,threads=2,nice=19),
        non_claims=['No productionadmission, profileconvergence or uniformerrorcertificate']),
        execution_artifacts=[str(f) for f in inputs],software=[dict(name='Python',version='3.9.6'),dict(name='NumPy',version='1.26.2'),dict(name='Agama',version='f302756b8af2b763db58e278e30478517dc8eea3'),dict(name='GSL',version='2.8')],randomness=dict(used=False,generator='',seed=None))
    # The script itself must declare a seed if it performs generated comparisons.
    if any(k in args.script for k in ('particle','performance','ellipsoid','weighted')):c['randomness']=dict(used=True,generator='NumPyPCG64',seed=522761 if 'weighted' in args.script else 20261022)
    contract=HERE/('contract_'+args.tag+'.json');contract.write_text(json.dumps(c,indent=2)+'\n');run=relative/args.tag
    cmd=['/usr/bin/python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(ROOT),'--contract',str(contract)]
    for f in inputs:cmd+=['--input',str(f)]
    cmd+=['--output',str(run),'--result',str(run/'results.json'),'--timeout','60','--max-cpu-seconds','55','--max-output-bytes','2000000','--max-threads','2','--','/usr/bin/nice','-n','19','/usr/bin/python3',str(relative/args.script),'--output',str(run/'results.json')]
    cmd += args.args[1:] if args.args and args.args[0]=='--' else args.args
    raise SystemExit(subprocess.call(cmd,cwd=ROOT))


if __name__=='__main__':main()
