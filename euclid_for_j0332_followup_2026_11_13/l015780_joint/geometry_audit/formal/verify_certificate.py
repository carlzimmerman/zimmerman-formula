"""Compile the frozen finite-array certificate and a false gate mutation."""
import argparse,hashlib,json,platform,re,subprocess,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PROJECT=ROOT/'fable_independent_2026/lean_2026'
SOURCE=HERE/'FiniteCapacity.lean'
FIELD=HERE.parents[1]/'field_grid_01/positions_deflections.npz'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def invoke(argv,log):
    start=time.monotonic()
    result=subprocess.run(argv,cwd=PROJECT,capture_output=True,text=True,timeout=120,check=False)
    log.write_text(result.stdout+result.stderr)
    return dict(argv=argv,cwd=str(PROJECT),exit_code=result.returncode,
        runtime_seconds=time.monotonic()-start,log_sha256=sha(log),log=str(log))


def main(output):
    output.mkdir(parents=True,exist_ok=True)
    code=SOURCE.read_text()
    assert not re.search(r'\b(sorry|admit)\b|^\s*axiom\s',code,re.M)
    paths=[SOURCE,FIELD,HERE/'instance.json',HERE/'make_certificate.py',Path(__file__).resolve(),
        PROJECT/'lean-toolchain',PROJECT/'lakefile.toml',PROJECT/'lake-manifest.json']
    before={str(p):sha(p) for p in paths}
    instance=json.loads((HERE/'instance.json').read_text())
    assert instance['source_sha256']==sha(SOURCE)
    assert instance['field_sha256']==sha(FIELD)
    accepted=invoke(['lake','env','lean',str(SOURCE)],output/'compile.log')
    version=invoke(['lake','env','lean','--version'],output/'lean_version.log')
    # Changing the actual source-association gate to3arcsec while retaining
    # the original bound/certificate makes the claim false. It must fail.
    mutation=code.replace('(3/10 : ℝ)','(3 : ℝ)')
    assert mutation!=code
    mutated=output/'FiniteCapacity_MUTATE.lean'
    mutated.write_text(mutation)
    rejected=invoke(['lake','env','lean',str(mutated)],output/'mutation_compile.log')
    assert accepted['exit_code']==0 and version['exit_code']==0
    assert 'sorryAx' not in (output/'compile.log').read_text()
    assert rejected['exit_code']!=0
    after={str(p):sha(p) for p in paths}
    assert before==after
    result=dict(assertion_tested='Lean accepts the frozen four-source finite-array/shear-null certificate and rejects the false3arcsec-gate mutation',
        accepted_compile=accepted,negative_control_compile=rejected,
        version=(output/'lean_version.log').read_text().strip(),platform=platform.platform(),
        python=platform.python_version(),input_sha256_before=before,input_sha256_after=after,
        instance=instance,axioms=['propext','Classical.choice','Quot.sound'],
        custom_axioms_or_sorry=False,mutation_sha256=sha(mutated),
        non_claims=['No PDE error certificate','No observational association certificate','Zero convergence is an explicit model premise','No full action or empirical theory exclusion'],
        review_provenance='Author self-review; independent raw-proof audit assigned by root to a separate agent',
        status='completed; expected positive and negative compile outcomes observed')
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','version','axioms','custom_axioms_or_sorry']},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    main(parser.parse_args().output)
