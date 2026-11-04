"""Check scaling records without promoting retained semantic/numerical failures."""
import hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
VALIDATOR='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    records=[]
    for p in sorted(HERE.rglob('manifest.json')):
        result=subprocess.run([sys.executable,VALIDATOR,str(p),'--root',str(ROOT)],capture_output=True,text=True)
        records.append(dict(path=str(p.relative_to(HERE)),status=json.loads(p.read_text())['run']['status'],valid=result.returncode==0,
                            sha256=sha(p),validation=result.stdout.strip(),error=result.stderr.strip()))
    assert len(records)==5 and all(r['valid'] for r in records)
    assert Counter(r['status'] for r in records)=={'completed':4,'failed':1}
    for name in ['run_002','crossovers_001','refinement_002']:
        assert json.loads((HERE/name/'results.json').read_text())['all_checks_pass']
    paths=['PLAN.md','DERIVATION.md','README.md','PROVENANCE_NOTES.md','calculate_v2.py','crossovers.py','refine_decomposition_v2.py',
           'run_002/results.json','crossovers_001/results.json','refinement_002/results.json']
    out=dict(records=records,manifest_count=5,all_manifest_hash_checks_valid=True,
        accepted_results=['run_002','crossovers_001','refinement_002'],
        retained_semantic_defect='run_001 dimensional Solar Q2 outputs omitted the fixed3/2 conversion; dimensionless and dwarf outputs remain correct. Accepted run002 corrects and tests the conversion.',
        retained_failed_accuracy_run='refinement_001: original finite domains did not meet the new1e-5 individual-component gate. Expanded domains in refinement002 meet the same gate.',
        qualification='Proof derivations and finite numerical diagnostics have separate scope; numerical agreement does not supply microscopic dynamics or a universal observational model.',
        sha256={str(p):sha(HERE/p) for p in paths})
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(manifests=5,statuses=dict(Counter(r['status'] for r in records)),all_valid=True)))


if __name__=='__main__':main()
