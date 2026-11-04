#!/usr/bin/env python3
"""Full-hash preservation, build binding and repaired-scorer verification. No writes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
V = ROOT/'reviews/alma_readiness_2026_11_04/revision_v1_4'
A = ROOT/'rebuild_2026_10_22/AC1_alma_condor_predictions'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    checks = []
    def check(name, value):
        checks.append(bool(value))
        print(('PASS ' if value else 'FAIL ')+name)
    saved = json.loads((HERE/'PAPER66_preserved_inputs_v1_4.json').read_text())
    check(f'all {len(saved)} historical input hashes unchanged', all((ROOT/f).is_file() and sha(ROOT/f)==h for f,h in saved.items()))
    build = json.loads((HERE/'PAPER66_build_v1_4.json').read_text())
    check('PDF bound to current complete TeX inputs', all(sha(HERE/f)==h for f,h in build['source_sha256'].items()))
    check('PDF hash matches build manifest', sha(HERE/'PAPER66_alma_release_predictions_2026.pdf')==build['pdf_sha256'])
    proc = subprocess.run([sys.executable,'-B',str(A/'test_ac1_fit_checks.py')],capture_output=True,text=True)
    check('fit-gate, uncertainty and preservation regressions',proc.returncode==0)
    if proc.returncode: print(proc.stdout+proc.stderr)
    st = json.loads((V/'selftest/ac1_score_selftest_results.json').read_text())
    check('end-to-end selftest and velocity-axis mutation', all(bool(ok) for _,ok in st['checks']))
    for label, file in [('archive','power_archive/ac1_score_power_results.json'),('sister','power_sister/ac1_score_power_div2.54_condorbeam_results.json')]:
        d = json.loads((V/file).read_text())
        check(label+' power complete: six seeds in each of three classes',all(len(d['runs'][k])==6 for k in ('realistic','compact','noise')))
        check(label+' noise-only controls not detected',not any(x['det'] for x in d['runs']['noise']))
        tex = (HERE/'PAPER66_validation_v1_4.tex').read_text()
        oldname = 'ac1_score_power_results.json' if label=='archive' else 'ac1_score_power_div2.54_condorbeam_results.json'
        old = json.loads((A/oldname).read_text())
        lab = 'archive' if label=='archive' else 'sister-like'
        check(label+' revised table matches saved runs',all(
            f"{lab} & {kind.replace('realistic','smooth')} & {sum(r['det'] for r in rows)}/6 & {sum(r['valid'] for r in old['runs'][kind])}/6 & {sum(r['valid'] for r in rows)}/6" in tex
            for kind,rows in d['runs'].items()))
        accepted = [f for rows in d['runs'].values() for row in rows for f in row['fit_diagnostics'].values() if f['valid']]
        check(label+' every accepted branch has all three starts agreeing',bool(accepted) and all(all(len(t['speeds'])==3 and t['pass'] and t['spread']<=.15 for t in f['start_agreement'].values()) for f in accepted))
    run = json.loads((V/'run_sources.json').read_text())
    check('validation used current scorer and helper',all(sha(ROOT/f)==h for f,h in run['sources'].items() if f.endswith('.py')))
    if (V/'validation_summary.json').exists():
        summary=json.loads((V/'validation_summary.json').read_text())
        check('validation artifacts match summary hashes',all(sha(ROOT/f)==h for f,h in summary['artifact_sha256'].items()))
    else: check('validation summary exists',False)
    print(f'{sum(checks)}/{len(checks)} revision checks pass')
    return 0 if all(checks) else 1

if __name__ == '__main__':
    sys.exit(main())
