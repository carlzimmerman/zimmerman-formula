"""Create a fresh audited run; does not accept commands from evidence files."""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy,scipy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')

def main():
    p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('--kind',choices=['benchmark','response','review'],default='response')
    p.add_argument('--state',default='baseline');p.add_argument('--level',type=int,default=0);p.add_argument('--krylov',type=int,default=256);p.add_argument('--bare',action='store_true')
    args=p.parse_args()
    if not args.label.replace('_','').replace('-','').isalnum():raise ValueError('simple label required')
    out=HERE/args.label;contract=HERE/(args.label+'_contract.json')
    if out.exists() or contract.exists():raise ValueError('fresh label required')
    files=[HERE/'CONTRACT.md',HERE/'THEORY.md',HERE/'reproduce.py']
    if args.kind=='benchmark':files+=[HERE/'benchmark.py',HERE/'orbits.py'];cmd=[sys.executable,str(HERE/'benchmark.py'),str(out)]
    elif args.kind=='review':files+=[HERE/'check_response.py',HERE/'response.py',HERE/'orbits.py'];cmd=[sys.executable,str(HERE/'check_response.py'),str(out)]
    else:
        files+=[HERE/name for name in ('response.py','background.py','orbits.py')]
        files+=sorted(x for x in (HERE/'inputs').rglob('*') if x.is_file() and '__pycache__' not in str(x))
        cmd=[sys.executable,str(HERE/'response.py'),str(out),'--state',args.state,'--level',str(args.level),'--krylov',str(args.krylov)]
        if args.bare:cmd+=['--bare']
    paths=[str(x.relative_to(ROOT)) for x in files]
    c=dict(claim_id='DR01_'+args.label,mathematics=dict(assertion_tested='Bounded '+args.kind+' as specified in CONTRACT.md; numerical tolerances are conditional.',
          coefficient_domain='IEEE float64 and complex128',conventions='FR01 dimensionless h_star,ell,t_star; normalized spherical harmonics; real part m=2',
          inputs=['FR01 pc=.2 eps=.01 '+args.state,'immutable source snapshots'],bounds=vars(args),non_claims=['No continuum stability proof','No finite-speed completion','No permanent core heating or galaxy/cluster law']),
          execution_artifacts=paths,software=[dict(name='Python',version=sys.version.split()[0]),dict(name='NumPy',version=numpy.__version__),dict(name='SciPy',version=scipy.__version__)],
          randomness=dict(used=False,generator='',seed=None))
    contract.write_text(json.dumps(c,indent=2)+'\n')
    argv=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(contract)]
    for f in paths:argv+=['--input',f]
    argv+=['--output',str(out.relative_to(ROOT)),'--result',str((out/'result.json').relative_to(ROOT))]
    if args.kind=='response':argv+=['--result',str((out/'response_series.npz').relative_to(ROOT))]
    argv+=['--timeout','1800','--max-output-bytes','2097152','--max-threads','1','--']+cmd
    raise SystemExit(subprocess.call(argv,cwd=ROOT))
if __name__=='__main__':main()
